# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import abc
import datetime
import subprocess
import typing as t

import annize.aux
import annize.callconv
import annize.context
import annize.data
import annize.features.base
import annize.features.dependencies.common
import annize.features.documentation.common
import annize.features.documentation.sphinx.output.common
import annize.features.documentation.sphinx.output.html as _  # TODO
import annize.features.documentation.sphinx.output.pdf as _  # TODO
import annize.features.documentation.sphinx.output.plaintext as _  # TODO
import annize.features.documentation.sphinx.rst
import annize.features.licensing
import annize.features.version
import annize.fs
import annize.fs.temp
import annize.i18n


class Document(annize.features.documentation.common.Document):

    class GenerateInfo:

        def __init__(self, intstruct: annize.fs.FsEntry, outdir: annize.fs.FsEntry, confdir: annize.fs.FsEntry,
                     language: str, *,
                     configvalues: t.Optional[t.Dict] = None, configlines: t.Optional[t.List] = None,
                     entry_path: str = ""):
            self.__intstruct = intstruct
            self.__outdir = outdir
            self.__confdir = confdir
            self.__language = language
            self.__configvalues = {} if (configvalues is None) else configvalues
            self.__configlines = [] if (configlines is None) else configlines
            self.__entry_path = entry_path

        def _to_dict(self):
            return {key: getattr(self, key) for key in dir(self) if not key.startswith("_")}

        @property
        def intstruct(self) -> annize.fs.FsEntry:
            return self.__intstruct

        @property
        def outdir(self) -> annize.fs.FsEntry:
            return self.__outdir

        @property
        def confdir(self) -> annize.fs.FsEntry:
            return self.__confdir

        @property
        def language(self) -> str:
            return self.__language

        @property
        def configvalues(self) -> t.Dict[str, t.Optional[t.Any]]:
            return self.__configvalues

        @property
        def configlines(self) -> t.List[str]:
            return self.__configlines

        @property
        def entry_path(self) -> str:
            return self.__entry_path

        @entry_path.setter
        def entry_path(self, v: str):
            self.__entry_path = v

    def __init__(self, *, projectname: t.Optional[str] = None, authors: t.Optional[str] = None,
                 version: t.Optional[str] = None, release: t.Optional[str] = None):
        self.__projectname = projectname
        self.__authors = authors
        self.__version = version
        self.__release = release

    def _prepare_generate(self, geninfo: "Document.GenerateInfo") -> None:
        pass

    @abc.abstractmethod
    def _generate_master_doc(self, geninfo: "Document.GenerateInfo") -> str:
        raise NotImplementedError()

    @property
    def _projectname(self):
        return self.__projectname or "TODO zz a"

    @property
    def _authors(self):
        return self.__authors or "TODO zz a"

    @property
    def _version(self):
        return self.__version or "TODO zz a"

    @property
    def _release(self):
        return self.__release or "TODO zz a"

    def generate_all_languages(self, outputspec):
        generator = annize.features.documentation.sphinx.output.common.find_output_generator_for_outputspec(outputspec)
        return generator.multilanguage_frame(self)

    def generate(self, outputspec, *, language="?"):
        with annize.i18n.get_culture(language):
            generator = annize.features.documentation.sphinx.output.common.find_output_generator_for_outputspec(
                outputspec)
            # .utils.basic.verify_tool_installed("sphinx-build")  # TODO anders
            shortsnippets = {}  # TODO
            # TODO media dirs
            annizeiconssrcfs = annize.fs.fsentry_by_path(f"{annize.aux.data_path}/icons")
            psubstitutions = "\n".join([f".. |{k}| replace:: {v}" for k, v in shortsnippets.items()])
            annizeicons = [annizeiconfs.basename()[:-4] for annizeiconfs in annizeiconssrcfs.children()]
            pannizeicons = "\n".join([f".. |annizeicon_{icon}| image:: /annizeicons/{icon}.png" for icon in annizeicons])
            with annize.fs.temp.fresh_temp_dir().owned() as confdir:
                with annize.fs.temp.fresh_temp_dir().owned() as intstruct:
                    outdir = annize.fs.temp.fresh_temp_dir()
                    geninfo = Document.GenerateInfo(intstruct, outdir, confdir, language)
                    dname = self._generate_master_doc(geninfo)
                    annizeiconssrcfs.copy_to(f"{intstruct.path()}/annizeicons")# TODO
                    geninfo.configvalues.update({
                        "project": self._projectname,
                        "version": self._version,
                        "release": self._release or self._version,
                        "master_doc": dname,
                        "rst_epilog": f"{psubstitutions}\n{pannizeicons}",
                        "nitpicky": True,
                        "extensions": ["sphinx.ext.autosummary", "sphinx.ext.inheritance_diagram"],
                        "autoclass_content": "both",
                        "autodoc_typehints": "description",
                        "html_show_sphinx": False,
                        "html_static_path": [],
                        "html_theme_options": dict(),
                        "html_sidebars": {"**": ["globaltoc.html", "searchbox.html"]},
                        "latex_elements": {"preamble": "\\usepackage{enumitem}\\setlistdepth{99}"}
                    })
                    if language != "?":
                        geninfo.configvalues["language"] = language
                    if self.__authors:
                        geninfo.configvalues["copyright"] = f"{datetime.datetime.now().year}, {self.__authors}"
                    self._prepare_generate(geninfo)
                    generator.prepare_generate(geninfo)
                    confpycontent = ""
                    for confkey, value in geninfo.configvalues.items():
                        confpycontent += f"{confkey} = {repr(value)}\n"
                    for confline in geninfo.configlines:
                        confpycontent += confline + "\n"
                    with open(f"{confdir.path()}/conf.py", "w") as f:
                        f.write(f"import base64, json\n"
                                f"{confpycontent}\n"
                                f"template_ = ''\n")  # TODO template_ ?!
                    # TODO error handling
                    subprocess.check_call(["sphinx-build", "-c", confdir.path(), "-b", generator.formatname(),
                                           intstruct.path(), outdir.owned().path()], stderr=subprocess.STDOUT)
            outdir = generator.postproc(outdir)
            return annize.features.documentation.common._DocumentGenerateResult(outdir, geninfo.entry_path)


class CompositeDocument(Document):  # TODO documentation on homepage incomplete and broken

    @annize.callconv.parameter_from_childnodes("documents")
    def __init__(self, *, projectname: t.Optional[str] = None, authors: t.Optional[str] = None,
                 version: t.Optional[str] = None, release: t.Optional[str] = None, documents: t.Iterable[Document]):
        super().__init__(projectname=projectname, authors=authors, version=version, release=release)
        self.__documents = documents

    def __get_inner_generateinfo(self, geninfo: Document.GenerateInfo, innerdoc: Document):
        kwa = geninfo._to_dict()
        kwa["intstruct"] = geninfo.intstruct.child_by_relative_path(annize.context.object_name(innerdoc))
        return Document.GenerateInfo(**kwa)

    def _generate_master_doc(self, geninfo):
        toctree = (".. toctree::\n"
                   "    :glob:\n"
                   "\n")
        for document in self.__documents:
            igeninfo = self.__get_inner_generateinfo(geninfo, document)
            igeninfo.intstruct.mkdir(exist_ok=False)
            dname = document._generate_master_doc(igeninfo)
            toctree += f"    {annize.context.object_name(document)}/{dname}\n"
        name = annize.context.object_name(self)
        with open(f"{geninfo.intstruct.path()}/{name}.rst", "w") as f:
            f.write(toctree)
        return name

    def _prepare_generate(self, geninfo):
        for document in self.__documents:
            document._prepare_generate(self.__get_inner_generateinfo(geninfo, document))


class ApiReferenceLanguage(abc.ABC):
    """
    Base class for a programming language in api references. See :py:class:`ApiReferencePiece`.
    """

    class ApiReferenceGenerateInfo(Document.GenerateInfo):

        def __init__(self, geninfo: Document.GenerateInfo, source: annize.fs.FsEntry, heading: str):
            super().__init__(**geninfo._to_dict())
            self.__source = source
            self.__heading = heading

        @property
        def source(self) -> annize.fs.FsEntry:
            return self.__source

        @property
        def heading(self) -> str:
            return self.__heading

    @abc.abstractmethod
    def prepare_generate(self, rgeninfo: "ApiReferenceLanguage.ApiReferenceGenerateInfo") -> None:
        pass

    @abc.abstractmethod
    def generate_master_doc(self, rgeninfo: "ApiReferenceLanguage.ApiReferenceGenerateInfo") -> str:
        pass


class ApiReferenceDocument(Document):
    """
    An api reference.
    """

    @annize.callconv.parameter_from_childnodes("language")
    @annize.callconv.parameter_from_childnodes("source")
    def __init__(self, *, language: ApiReferenceLanguage, heading: t.Optional[str] = None,
                 source: annize.fs.FsEntry = None):
        super().__init__()
        self.__language = language
        self.__heading = heading or annize.i18n.TrStr.tr("an_Doc_APIRefTitle")
        self.__source = source

    def available_languages(self) -> t.List[str]:
        return ["en", "de"]  # TODO

    def __get_refgeninfo(self, geninfo: Document.GenerateInfo):
        return ApiReferenceLanguage.ApiReferenceGenerateInfo(geninfo, self.__source.temp_clone().owned(),
                                                             self.__heading)
        # TODO temp_clone ?!

    def _generate_master_doc(self, geninfo):
        return self.__language.generate_master_doc(self.__get_refgeninfo(geninfo))

    def _prepare_generate(self, geninfo):
        self.__language.prepare_generate(self.__get_refgeninfo(geninfo))


class ArgparseCommandLineInterfaceDocument(Document):

    @annize.callconv.parameter_from_childnodes("language")
    @annize.callconv.parameter_from_childnodes("source")
    def __init__(self, *, parserfactory: str, programname: str, heading: t.Optional[str] = None,
                 source: annize.fs.FsEntry = None):
        super().__init__()
        self.__parserfactory = parserfactory
        self.__programname = programname
        self.__heading = heading or annize.i18n.TrStr.tr("an_Doc_CLIRefTitle")
        self.__source = source

    def available_languages(self) -> t.List[str]:
        return ["en", "de"]  # TODO

    def _generate_master_doc(self, geninfo):
        toctree = (f".. argparse::\n"
                   f"    :ref: {self.__parserfactory}\n"
                   f"    :prog: {self.__programname}\n")
        name = annize.context.object_name(self)
        with open(f"{geninfo.intstruct.path()}/{name}.rst", "w") as f:
            f.write(annize.features.documentation.sphinx.rst.RstGenerator.heading(self.__heading))#TODO
            f.write(toctree)
        return name

    def _prepare_generate(self, geninfo):
        geninfo.configvalues["extensions"].append("sphinxarg.ext")
        intdst = geninfo.intstruct.child_by_relative_path("TODO zz cliref")
        self.__source.owned().move_to(intdst.path())


class RstDocumentVariant:

    @annize.callconv.parameter_from_childnodes("source")
    def __init__(self, *, language: str = "?", source: annize.fs.FsEntry):  # TODO language="?" ?!
        self.__language = language
        self.__source = source

    @property
    def language(self) -> str:
        return self.__language

    @property
    def source(self) -> annize.fs.FsEntry:
        return self.__source


class RstDocument(Document):
    """
    A reStructuredText formatted file or a directory of such files.
    """

    def available_languages(self):
        return list(sorted(list(set(v.language for v in self.__variants))))

    @annize.callconv.parameter_from_childnodes("variants")
    def __init__(self, *, variants: t.List[RstDocumentVariant], **kwargs):
        super().__init__(**kwargs)
        self.__variants = variants

    def __get_variant(self, language: str) -> t.Optional[RstDocumentVariant]:
        for variant in self.__variants:
            if variant.language == language:
                return variant
        return None

    def _generate_master_doc(self, geninfo):  # TODO cache it, so we can potentially remove source?!
        source = self.__get_variant(geninfo.language).source.owned()
        basename = source.basename()
        if not basename.lower().endswith(".rst"):
            basename += ".rst"
        source.copy_to(geninfo.intstruct.child_by_relative_path(basename).path())
        return basename[:-4]


class AboutProjectDocument(Document):

    @annize.callconv.parameter_from_childnodes("dependencies")
    def __init__(self, *, projectname: t.Optional[str] = None, authors: t.Optional[str] = None,
                 version: t.Optional[str] = None, release: t.Optional[str] = None,
                 dependencies: t.List[annize.features.dependencies.common.Dependency],
                 project_version: annize.data.Version = None):  # TODO noh more optionals : projectname, license, version, dependencies
        super().__init__(projectname=projectname, authors=authors, version=version, release=release)
        self.__dependencies = dependencies
        self.__project_version = project_version

    def available_languages(self) -> t.List[str]:
        return ["en", "de"]  # TODO

    def _generate_master_doc(self, geninfo):  # TODO review
        readmefs = geninfo.intstruct.child_by_relative_path("readme.rst")
        head_about = annize.i18n.tr("an_Doc_ReadmeHeadAbout")
        head_license = annize.i18n.tr("an_Doc_ReadmeHeadLicense")
        head_uptodate = annize.i18n.tr("an_Doc_ReadmeHeadUpToDate")
        head_dependencies = annize.i18n.tr("an_Doc_ReadmeHeadDependencies")
        content_about = annize.features.base.long_description()
        licenses = annize.features.licensing.project_licenses()
        project_version = self.__project_version
        if not project_version:
            project_versions = annize.features.version.project_versions()
            project_version = project_versions[0]  # TODO
        dependencies = self.__dependencies or []  # TODO
        content = (f"{annize.features.documentation.sphinx.rst.RstGenerator.heading(head_about, sub=True)}"
                   f"{content_about}")
        projectname = annize.features.base.pretty_project_name() or "This project"  # TODO i18n  # TODO or self.projectname?!
        if len(licenses) > 0:
            licnames = [lic.name for lic in licenses]
            licdesc = ", ".join(licnames[:-1]) + (" and " if len(licnames) > 1 else "") + licnames[-1]  # TODO noh i18n  # TODO dedup (homepage.sections.license)
            content_license = annize.i18n.tr("an_HP_Lic_Text").format(**locals())
            content += (f"{annize.features.documentation.sphinx.rst.RstGenerator.heading(head_license)}"
                        f"{content_license}")
        content_uptodate = annize.i18n.tr("an_Doc_ReadmeUpToDate")
        if project_version:
            content_uptodate += " " + annize.i18n.tr("an_Doc_ReadmeUpToDateCurrentVersion").format(**locals())
        content += (f"{annize.features.documentation.sphinx.rst.RstGenerator.heading(head_uptodate)}"
                    f"{content_uptodate}")
        if len(dependencies) > 0:
            content_dependencies = annize.i18n.tr("an_HP_DL_Uses3rdParty").format(**locals())
            content_dependencies += "\n\n" + annize.features.dependencies.common.dependencies_to_rst_text(dependencies)
            content += (f"{annize.features.documentation.sphinx.rst.RstGenerator.heading(head_dependencies)}"
                        f"{content_dependencies}")
        readmefs.write_file(content)
        return "readme"


class ReadmeDocument(CompositeDocument):  # TODO noh maturity flags?!  # TODO is the web url to readme stable?
    """
    A reStructuredText formatted file or a directory of such files.
    """

    @annize.callconv.parameter_from_childnodes("dependencies")
    def __init__(self, *, projectname: t.Optional[str] = None, authors: t.Optional[str] = None,
                 version: t.Optional[str] = None, release: t.Optional[str] = None, documents: t.Iterable[Document],
                 title: t.Optional[str] = None,
                 dependencies: t.List[annize.features.dependencies.common.Dependency],
                 project_version: annize.data.Version = None):
        #TODO version vs project_version confusion
        super().__init__(projectname=projectname, authors=authors, version=version, release=release,
                         documents=[AboutProjectDocument(dependencies=dependencies, project_version=project_version),
                                    *documents])
        self.__title = title

    def available_languages(self) -> t.List[str]:
        return ["en", "de"]  # TODO

    @property
    def title(self) -> str:  # TODO move to a superclass?!
        projectname = annize.features.base.pretty_project_name()
        #TODO generalize those .format(**locals()) tricks. this implicit way is broken!
        return (self.__title or annize.i18n.TrStr.tr("an_Doc_ReadmeTitle")).format(**locals())


"""TODO
https://docutils.sourceforge.io/docs/user/config.html
https://www.sphinx-doc.org/en/master/usage/advanced/intl.html
understand localtoc vs globaltoc
manpage
sphinx.builders.changes.ChangesBuilder
https://www.sphinx-doc.org/en/master/usage/extensions/autosummary.html#module-sphinx.ext.autosummary
https://www.sphinx-doc.org/en/master/usage/extensions/doctest.html
https://www.sphinx-doc.org/en/master/usage/extensions/graphviz.html
https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html


nothere
setup.py
""".upper().lower()

# TODO noh: fix all docstrings in documentation.* (some are old)
# TODO woanders      f"exclude_patterns = ['.directory', 'Thumbs.db', '.DS_Store', '.git', '.svn', '.piget', '.idea']\n"

# TODO switch sphinx (and other things) to the current culture
