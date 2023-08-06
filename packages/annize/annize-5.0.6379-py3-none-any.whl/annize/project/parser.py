# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Reading, processing and writing of Annize projects.
"""

import contextlib
import os
import xml.etree.ElementTree
import typing as t

import annize.project


def parse(path: str) -> t.List[annize.project.FileNode]:
    parser = _XmlParser()
    path = os.path.abspath(path)
    parentpath, basename = os.path.split(path)
    basenamesuffixidx = basename.rfind(".")
    if basenamesuffixidx > -1:
        filestoparse = []
        for ancname in os.listdir(parentpath):
            if ancname.startswith(basename[:basenamesuffixidx + 1]) and ancname.endswith(basename[basenamesuffixidx:]):
                filestoparse.append(f"{parentpath}/{ancname}")
    else:
        filestoparse = [path]
    return [parser.parse_file(f) for f in sorted(filestoparse)]


class _XmlParser:

    class _Context:

        def __init__(self):
            self.__path = None
            self.__xnode = None
            self.__consumed_in_errorreport = False

        @staticmethod
        def __nodeshort(xnode: xml.etree.ElementTree.Element, maxlen=100):
            result = xml.etree.ElementTree.tostring(xnode).decode().strip()
            result = result.replace("\r", "").replace("\n", "\u21b5")
            if len(result) > maxlen:
                result = result[maxlen-1] + "\u1801"
            return result

        def __str__(self):
            if self.__path:
                result = f"in {self.__path}"
                if self.__xnode is not None:
                    result += f" (around: {self.__nodeshort(self.__xnode)})"
            else:
                result = "in global scope"
            return result

        @contextlib.contextmanager
        def in_file(self, fpath):
            self.__path = fpath
            self.__xnode = None
            try:
                yield
            finally:
                self.__path = None
                self.__xnode = None

        @contextlib.contextmanager
        def in_node(self, xnode):
            xoldnode = self.__xnode
            self.__xnode = xnode
            try:
                yield
            except Exception as ex:
                if not self.__consumed_in_errorreport:
                    self.__consumed_in_errorreport = True
                    raise annize.project.ParserError(f"Reading project definition failed {self}: {ex}") from ex
                raise
            finally:
                self.__xnode = xoldnode

    class _TagParts:

        def __init__(self, name, namespace: str = ""):
            if name.startswith("{"):
                if namespace:
                    raise annize.project.BadStructureError("Namespace is specified via argument and inside the name,"
                                                           " which is conflicting")
                namespaceendidx = name.find("}")
                self.namespace, self.tagname = name[1:namespaceendidx], name[namespaceendidx + 1:]
            else:
                self.namespace, self.tagname = namespace, name

    def __init__(self):
        self.__context = self._Context()

    ATTRIBUTE_COMMAND_START = "~"
    ATTRIBUTE_COMMAND_END = "~"

    @classmethod
    def escape_attribute_string(cls, txt: str) -> str:
        if txt.startswith(cls.ATTRIBUTE_COMMAND_START) and txt.endswith(cls.ATTRIBUTE_COMMAND_END):
            return f"{cls.ATTRIBUTE_COMMAND_START}{txt}{cls.ATTRIBUTE_COMMAND_END}"

    @classmethod
    def __interpret_attribute_string(cls, txt: str) -> t.Tuple[bool, str]:
        is_command = False
        if txt.startswith(cls.ATTRIBUTE_COMMAND_START) and txt.endswith(cls.ATTRIBUTE_COMMAND_END):
            txt = txt[1:-1]
            if not txt.startswith(cls.ATTRIBUTE_COMMAND_START):
                is_command = True
        return is_command, txt

    @classmethod
    def __parse_attrib(cls, key: str, value: str) -> annize.project.Node:
        value_is_command, value = cls.__interpret_attribute_string(value)
        if value_is_command:
            if value == "False":
                value = False
            elif value == "True":
                value = True
            elif value.startswith("Reference "):  # TODO or lower cased (as <a:reference...) ?!
                result = annize.project.ReferenceNode()
                result.reference_key = value[10:]
                result.arg_name = key
                return result
            else:
                raise Exception("TODO")
        result = annize.project.ScalarValueNode()
        result.value = value
        result.arg_name = key
        return result

    def __parse_tag(self, node: annize.project.Node, argname, callname, feature, xnode):
        xresult = xnode
        if isinstance(node, annize.project.CallableNode) and node.callee == callname:
            if len(xnode) > 0:
                resultnode, xresult = self.__parse_child(node, xnode[0])
            else:
                resultnode = annize.project.ScalarValueNode()
                resultnode.value = xnode.text
            resultnode.arg_name = argname
        else:
            resultnode = annize.project.CallableNode()
            resultnode.feature, resultnode.callee = feature, callname
            cnode, xresult = self.__parse_child(resultnode, xnode)
            resultnode.append_child(cnode)
        return resultnode, xresult

    def __parse_child(
            self, node: annize.project.Node,
            xnode: xml.etree.ElementTree.Element) -> t.Tuple[annize.project.Node, xml.etree.ElementTree.Element]:
        xresult = xnode
        with self.__context.in_node(xnode):
            tagparts = self._TagParts(xnode.tag)
            namespace = tagparts.namespace or ""
            if namespace == "annize":
                if tagparts.tagname == "if_unavailable":
                    resultnode = annize.project.OnFeatureUnavailableNode()
                    resultnode.feature = xnode.attrib.get("feature", None)
                    resultnode.scope = xnode.attrib.get("scope", None)
                    resultnode.do = xnode.attrib.get("do", None)
                elif tagparts.tagname == "reference":
                    resultnode = annize.project.ReferenceNode()
                    resultnode.reference_key = xnode.attrib["name"]
                    resultnode.on_unresolvable = xnode.attrib.get("on_unresolvable", None)  # TODO test
                else:
                    raise annize.project.ParserError(f"Invalid tag: '{tagparts.tagname}'.")
            elif namespace.startswith("annize:"):
                feature = namespace[7:]
                tagnamesegments = tagparts.tagname.split(".")
                if len(tagnamesegments) == 1:
                    resultnode = annize.project.CallableNode()
                    resultnode.feature, resultnode.callee = feature, tagnamesegments[0]
                elif len(tagnamesegments) == 2:
                    callname, argname = tagnamesegments
                    resultnode, xresult = self.__parse_tag(node, argname, callname, feature, xnode)
                else:
                    raise annize.project.BadStructureError(f"Invalid argument '{tagparts.tagname}'")
                for attribkey, attribvalue in xnode.attrib.items():
                    if attribkey == "{annize}name":
                        resultnode.name = attribvalue
                    elif attribkey == "{annize}append_to":
                        resultnode.append_to = attribvalue
                    else:
                        resultnode.append_child(self.__parse_attrib(attribkey, attribvalue))
            else:
                raise annize.project.BadStructureError(f"Invalid namespace '{namespace}'" if namespace
                                                       else "Missing namespace")
            return resultnode, xresult

    def __parse_children(self, node: annize.project.Node, xparent: xml.etree.ElementTree.Element):
        for xnode in xparent:
            childnode, xchildinnernode = self.__parse_child(node, xnode)
            if childnode:
                node.append_child(childnode)
                self.__parse_children(childnode, xchildinnernode)

    def parse_file(self, fpath: str) -> annize.project.FileNode:
        with self.__context.in_file(fpath):
            result = annize.project.FileNode(fpath)
            with open(fpath, "r") as f:
                xroot = xml.etree.ElementTree.fromstring(f.read())
            with self.__context.in_node(xroot):
                self.__parse_children(result, xroot)
            return result


# TODO raise errors on unexpected attributes in <a:...> tags
