# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

"""
Definitions of Annize projects.
"""

import copy
import enum
import typing as t


class ProjectDefinition:
    """
    A data structure that holds an in-memory representation of the project description.
    It is not the in-memory representation of the live universe object state.
    It is like the file structure of the project description file, but not exactly the same.
    There is a parser and a generator for translating between a project description file and an ProjectDefinition.
    """

    def __init__(self, *nodes: "FileNode"):
        self.__nodes = nodes

    def __str__(self):
        return "".join([c.get_description() for c in self.nodes])

    @property
    def nodes(self) -> t.Iterable["FileNode"]:
        return tuple(self.__nodes)

    @staticmethod
    def from_files(path: str) -> "ProjectDefinition":
        from annize.project import parser
        return ProjectDefinition(*parser.parse(path))


class Node:

    def __init__(self):
        self.__parent = None
        self.__children = []

    @property
    def parent(self) -> "Node":
        return self.__parent

    @property
    def children(self) -> t.Iterable["Node"]:
        return tuple(self.__children)

    def insert_child(self, i: int, node: "Node"):
        if node.__parent:
            raise BadStructureError("Tried to add a child node that already has a parent")
        for allowedchildtype in self._allowed_child_types():
            if isinstance(node, allowedchildtype):
                break
        else:
            raise BadStructureError(f"Unexpected node {node}")
        node.__parent = self
        self.__children.insert(i, node)

    def append_child(self, node: "Node"):
        self.insert_child(len(self.__children), node)

    def remove_child(self, node: "Node"):
        self.__children.remove(node)
        node.__parent = None

    @classmethod
    def _allowed_child_types(cls) -> t.Iterable[t.Type["Node"]]:
        return [BlockNode]

    def clone(self, with_children: bool = True) -> "Node":
        result = copy.copy(self)
        result.__parent = None
        result.__children = []
        if with_children:
            for child in self.children:
                result.append_child(child.clone())
        return result

    def get_description(self, *, with_children: bool = True, multiline: bool = True) -> str:
        return self.__get_description(0, with_children, multiline)

    def __get_description(self, indent: int, with_children: bool, multiline: bool) -> str:
        linesep = "\n" if multiline else "; "
        indentstr = indent * "  "
        details = self._str_helper()
        result = f"{indentstr}- {type(self).__name__}: {details[0] if details else ''}{linesep}"
        for detail in details[1:]:
            result += f"{indentstr}  {detail}{linesep}"
        if with_children:
            for child in self.children:
                result += child.__get_description(indent+1, with_children, multiline)
        return result

    def __str__(self):
        return self.get_description(with_children=False, multiline=False)

    def _str_helper(self):
        return []


class FileNode(Node):

    def __init__(self, path: str):
        super().__init__()
        self.__path = path

    @property
    def path(self) -> str:
        return self.__path

    def _str_helper(self):
        return [self.path, *super()._str_helper()]

    @classmethod
    def _allowed_child_types(cls):
        return [CallableNode, *super()._allowed_child_types()]


class ArgumentNode(Node):

    def __init__(self):
        super().__init__()
        self.arg_name = None
        self.name = None
        self.append_to = None

    @property
    def name(self) -> t.Optional[str]:
        return self.__name

    @name.setter
    def name(self, value: t.Optional[str]):
        self.__name = value

    @property
    def append_to(self) -> t.Optional[str]:
        return self.__append_to

    @append_to.setter
    def append_to(self, value: t.Optional[str]):
        self.__append_to = value

    @property
    def arg_name(self) -> t.Optional[str]:
        return self.__arg_name

    @arg_name.setter
    def arg_name(self, value: t.Optional[str]):
        self.__arg_name = value or None

    def _str_helper(self):
        return ([f"arg_name: {self.arg_name}"] if self.arg_name else []) + \
               ([f"append_to: {self.append_to}"] if self.append_to else []) + super()._str_helper()


class CallableNode(ArgumentNode):

    def __init__(self):
        super().__init__()
        self.callee = None
        self.feature = None

    @property
    def callee(self) -> str:
        return self.__callee

    @callee.setter
    def callee(self, value: str):
        self.__callee = value

    @property
    def feature(self) -> str:
        return self.__feature

    @feature.setter
    def feature(self, value: str):
        self.__feature = value

    def _str_helper(self):
        return [f"{self.feature} :: {self.callee}", *super()._str_helper()]

    @classmethod
    def _allowed_child_types(cls):
        return [ArgumentNode, *super()._allowed_child_types()]


class ScalarValueNode(ArgumentNode):

    def __init__(self):
        super().__init__()
        self.value = None

    @property
    def value(self) -> str:
        return self.__value

    @value.setter
    def value(self, value: str):
        self.__value = value

    def _str_helper(self):
        return [self.__shorten(self.value), *super()._str_helper()]

    @staticmethod
    def __shorten(obj: t.Any, maxlen: int = 100) -> str:
        result = str(obj).replace("\r", "").replace("\n", "\u21b5")
        if len(result) > maxlen:
            result = result[:maxlen-1] + "\u1801"
        return result


class ReferenceNode(ArgumentNode):

    class OnUnresolvableAction(enum.Enum):
        FAIL = "fail"
        SKIP = "skip"

    def __init__(self):
        super().__init__()
        self.reference_key = None
        self.on_unresolvable = None

    @property
    def reference_key(self) -> str:
        return self.__reference_key

    @reference_key.setter
    def reference_key(self, value: str):
        self.__reference_key = value

    @property
    def on_unresolvable(self) -> OnUnresolvableAction:
        return self.OnUnresolvableAction(self.__on_unresolvable or self.OnUnresolvableAction.FAIL.value)

    @on_unresolvable.setter
    def on_unresolvable(self, value: OnUnresolvableAction):
        self.__on_unresolvable = getattr(value, "value", value)
        str(self.on_unresolvable)  # checks if valid

    def _str_helper(self):
        return [f"name {self.reference_key}", *super()._str_helper()]

    @classmethod
    def _allowed_child_types(cls):
        return []


class BlockNode(Node):

    @classmethod
    def _allowed_child_types(cls):
        return [Node]


class ScopableBlockNode(BlockNode):

    class Scope(enum.Enum):
        BLOCK = "block"
        FILE = "file"
        PROJECT = "project"

    def __init__(self):
        super().__init__()
        self.scope = None

    def _str_helper(self):
        return [f"{self.scope.value} scope", *super()._str_helper()]

    @property
    def scope(self) -> Scope:
        return self.Scope(self.__scope or self.Scope.BLOCK.value)

    @scope.setter
    def scope(self, value: Scope):
        self.__scope = getattr(value, "value", value)
        str(self.scope)  # checks if valid


class OnFeatureUnavailableNode(ScopableBlockNode):

    class Action(enum.Enum):
        FAIL = "fail"
        SKIP_BLOCK = "skip_block"
        SKIP_NODE = "skip_node"

    def __init__(self):
        super().__init__()
        self.feature = None
        self.do = None

    def _str_helper(self):
        return [f"{self.do.value} for feature {self.feature}", *super()._str_helper()]

    @property
    def feature(self) -> "str":
        return self.__feature or "*"

    @feature.setter
    def feature(self, value: "str"):
        self.__feature = value

    @property
    def do(self) -> Action:
        return self.Action(self.__do or self.Action.SKIP_BLOCK.value)

    @do.setter
    def do(self, value: Action):
        self.__do = getattr(value, "value", value)
        str(self.do)  # checks if valid


class FeatureUnavailableError(ModuleNotFoundError):

    def __init__(self, featurename: str):
        super().__init__(f"No Annize feature named '{featurename}'")
        self.featurename = featurename


class BadStructureError(ValueError):

    def __init__(self, message: str):
        super().__init__(f"Bad project structure: {message}")


class MaterializerError(TypeError):

    def __init__(self, message: str):
        super().__init__(f"Unable to materialize project structure: {message}")


class ParserError(ValueError):
    """
    Parsing error like bad input xml.
    """

    def __init__(self, message: str):
        super().__init__(f"Unable to parse project definition: {message}")


class UnresolvableReferenceError(MaterializerError):

    def __init__(self, refname: str):
        super().__init__(f"Reference '{refname}' is unresolvable")
        self.refname = refname
        self.retry_can_help = True
