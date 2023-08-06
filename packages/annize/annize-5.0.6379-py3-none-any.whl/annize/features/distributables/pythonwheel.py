# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import dataclasses
import os
import subprocess
import typing as t

import annize.callconv
import annize.data
import annize.features.authors
import annize.features.base
import annize.features.licensing
import annize.fs.temp


class ExecutableLink:

    def __init__(self, *, linkname: str, modulename: str, methodname: str, is_gui: bool):
        self.__linkname = linkname
        self.__modulename = modulename
        self.__methodname = methodname
        self.__is_gui = is_gui

    @property
    def linkname(self) -> str:
        return self.__linkname

    @property
    def modulename(self) -> str:
        return self.__modulename

    @property
    def methodname(self) -> str:
        return self.__methodname

    @property
    def is_gui(self) -> bool:
        return self.__is_gui


class Package(annize.fs.AdHocFsEntry):

    @annize.callconv.parameter_from_childnodes("source")
    @annize.callconv.parameter_from_childnodes("executable_links")
    @annize.callconv.parameter_from_childnodes("version")
    @annize.callconv.parameter_from_childnodes("license")
    @annize.callconv.parameter_from_childnodes("author")
    def __init__(self, *, source: annize.fs.FsEntry, executable_links: t.List[ExecutableLink],
                 packagename: t.Optional[str] = None, description: t.Optional[str] = None,
                 homepage_url: t.Optional[str] = None, long_description: t.Optional[str] = None,
                 version: annize.data.Version = None, keywords: annize.features.base.Keywords = None,
                 license: annize.features.licensing.License = None,
                 author: annize.features.authors.Author = None,):
        super().__init__()
        self.__source = source
        self.__executable_links = executable_links
        self.__packagename = packagename
        self.__description = description
        self.__homepage_url = homepage_url
        self.__long_description = long_description
        self.__version = version
        self.__keywords = keywords
        self.__license = license
        self.__author = author

    def _initialize(self):
        buildname = self.__packagename or annize.features.base.project_name()
        author = self.__author
        if not author:  # TODO dedup
            projauthors = annize.features.authors.default_project_authors()
            if len(projauthors) > 0:
                author = projauthors[0]  # TODO only 1st?!
            else:
                author = annize.features.authors.Author(fullname=f"The {buildname} Team")
        license = self.__license
        if not license:
            projlics = annize.features.licensing.project_licenses()
            if len(projlics) > 0:
                license = projlics[0]  # TODO only 1st?!
            else:
                license = object()#TODO
        return self._mkpackage(self._BuildInfo(
            source=self.__source,
            long_description=self.__long_description or annize.features.base.long_description(),
            homepage=self.__homepage_url or annize.features.base.homepage_url(),
            description=self.__description or annize.features.base.summary(),
            keywords=self.__keywords or annize.features.base.project_keywords(),
            name=buildname,
            author=author,
            license=license,
            executable_links=self.__executable_links,
            version=self.__version))

    @dataclasses.dataclass()
    class _BuildInfo:
        source: annize.fs.FsEntry
        description: str
        long_description: str
        keywords: annize.features.base.Keywords
        name: str
        version: annize.data.Version
        homepage: str
        author: annize.features.authors.Author
        license: annize.features.licensing.License
        executable_links: t.List[ExecutableLink]
        pkgrootpath: str = None
        pkgpath_setuppy: str = None
        setuppy_conf: t.Dict[str, t.Optional[t.Any]] = None
        result: annize.fs.FsEntry = None

    @classmethod
    def _mkpackage_prepareinfos(cls, build: _BuildInfo, tmpdir: str) -> None:
        build.pkgrootpath = f"{tmpdir}/wheelpkg"
        build.source.owned().move_to(build.pkgrootpath)
        build.setuppy_conf = {}
        build.pkgpath_setuppy = f"{build.pkgrootpath}/setup.py"
        if os.path.exists(build.pkgpath_setuppy):
            raise Exception("TODO There must be no setup.py in the project root.")

    @classmethod
    def _mkpackage_setuppyconf_prepare(cls, build: _BuildInfo) -> None:
        build.setuppy_conf["name"] = build.name
        build.setuppy_conf["version"] = str(build.version)
        build.setuppy_conf["description"] = str(build.description)
        build.setuppy_conf["long_description"] = str(build.long_description)
        build.setuppy_conf["description_content_type"] = "text/plain"
        build.setuppy_conf["long_description_content_type"] = "text/plain"
        build.setuppy_conf["url"] = str(build.homepage)
        build.setuppy_conf["author"] = str(build.author.fullname)
        build.setuppy_conf["author_email"] = str(build.author.email)
        build.setuppy_conf["license"] = str(build.license.name)
        build.setuppy_conf["include_package_data"] = True
        if build.keywords.keywords:
            build.setuppy_conf["keywords"] = " ".join([str(kwd) for kwd in build.keywords.keywords])

    @classmethod
    def _mkpackage_setuppyconf_install_requires(cls, build: _BuildInfo) -> None:
        build.setuppy_conf["install_requires"] = [] # TODO

    @classmethod
    def _mkpackage_setuppyconf_classifiers(cls, build: _BuildInfo) -> None:
        build.setuppy_conf["classifiers"] = [] # TODO
        #TODO license classifier

    @classmethod
    def _mkpackage_mkexeclinks(cls, build: _BuildInfo) -> None:
        console_scripts = []
        gui_scripts = []
        for executable_link in build.executable_links:
            lst = gui_scripts if executable_link.is_gui else console_scripts
            lst.append(f"{executable_link.linkname}={executable_link.modulename}:{executable_link.methodname}")
        build.setuppy_conf["entry_points"] = {
            "console_scripts": console_scripts,
            "gui_scripts": gui_scripts
        }

    @classmethod
    def _mkpackage_mksetuppyconf(cls, build: _BuildInfo) -> None:
        setuppyconfcode = ""
        for confkey, value in build.setuppy_conf.items():
            setuppyconfcode += f"{confkey}={repr(value)},"
        with open(build.pkgpath_setuppy, "w") as f:
            f.write(f"import setuptools\n"
                    f"setuptools.setup(\n"
                    f"    {setuppyconfcode}\n"
                    f"    packages=setuptools.find_packages()+setuptools.find_namespace_packages()\n"
                    f")\n")

    @classmethod
    def _mkpackage_bdist_wheel(cls, build: _BuildInfo) -> None:
        subprocess.check_call(["python3", "setup.py", "bdist_wheel", "--python-tag", "py3"], cwd=build.pkgrootpath)
        distfs = annize.fs.fsentry_by_path(build.pkgrootpath).child_by_relative_path("dist")
        build.result = distfs.children()[0]

    @classmethod
    def _mkpackage_mkmanifestin(cls, build: _BuildInfo) -> None:
        with open(f"{build.pkgrootpath}/MANIFEST.in", "w") as f:
            f.write("graft **\n"
                    "global-exclude *.py[cod]\n")

    @classmethod
    def _mkpackage(cls, build: _BuildInfo) -> annize.fs.FsEntry:
        with annize.fs.temp.fresh_temp_dir() as tmpdir:
            # TODO review impl
            """
            TODO
            for src, dst in [("README", f"/usr/share/doc/{universe.name}/README"),
                             ("README.pdf", f"/usr/share/doc/{universe.name}/README.pdf")]:
            """        """#TODO
            if .utils.basic.call("fakeroot -v", shell=True)[0] != 0:
                raise .framework.exceptions.RequirementsMissingError("'fakeroot' seems to be unavailable")
            if .utils.basic.call("dpkg --version", shell=True)[0] != 0:
                raise .framework.exceptions.RequirementsMissingError("'dpkg' seems to be unavailable")
            """
            cls._mkpackage_prepareinfos(build, tmpdir.owned().path())
            cls._mkpackage_setuppyconf_prepare(build)
            cls._mkpackage_setuppyconf_install_requires(build)
            cls._mkpackage_setuppyconf_classifiers(build)
            cls._mkpackage_mkexeclinks(build)
            cls._mkpackage_mksetuppyconf(build)
            cls._mkpackage_mkmanifestin(build)
            cls._mkpackage_bdist_wheel(build)
            return build.result.temp_clone()


"""TODO
try:
    import setuptools as _foo_test_setuptools
except ImportError as exc:
    raise .framework.exceptions.RequirementsMissingError("'setuptools' seem to be unavailable", exc)
if .utils.basic.call("wheel version", shell=True)[0] != 0:
    raise .framework.exceptions.RequirementsMissingError("'wheel' seems to be unavailable")
    """
