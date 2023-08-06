# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import dataclasses
import os
import subprocess
import typing as t

import annize.callconv
import annize.features.base
import annize.features.distributables.common
import annize.fs.temp
import annize.i18n


class MenuEntry:

    def __init__(self, *, name: str, title: str, category: t.Tuple, command: str, gui: bool, icon: annize.fs.FsEntry):
        self.name = name
        self.title = title
        self.category = category
        self.command = command
        self.gui = gui
        self.icon = icon


class Filesystem:

    def __init__(self, **b):
        pass  # TODO


class Share:

    def __init__(self, **b):
        pass  # TODO


class EnvironmentVariable:

    def __init__(self, **b):
        pass  # TODO


class Repository:

    def __init__(self, *, public_url: str, friendly_name_suggestion: str = None):
        self.__public_url = public_url
        self.__friendly_name_suggestion = friendly_name_suggestion

    def upload(self, source: annize.fs.FsEntry):
        pass  # TODO implement or abstract?!

    @property
    def public_url(self) -> str:
        return self.__public_url

    @property
    def friendly_name_suggestion(self) -> str:
        return self.__friendly_name_suggestion or os.path.basename(self.public_url)


class LocalRepository(Repository):
    #TODO refactor to sth like "FsEntryRepository" (or put it just to repository)

    @annize.callconv.parameter_from_childnodes("upload_fsentry")
    def __init__(self, *, public_url: str, friendly_name_suggestion: str = None, upload_path: str = None,
                 upload_fsentry: annize.fs.FsEntry = None):
        super().__init__(public_url=public_url, friendly_name_suggestion=friendly_name_suggestion)
        self.__public_url = public_url
        self.__friendly_name_suggestion = friendly_name_suggestion
        self.__upload_path = upload_path or upload_fsentry.readable_path()  # TODO .readable_path() is weird

    def upload(self, source: annize.fs.FsEntry):
        source.copy_to(self.__upload_path, overwrite=True)


class Group(annize.features.distributables.common.Group):

    @annize.callconv.parameter_from_childnodes("source")
    @annize.callconv.parameter_from_childnodes("repository")
    def __init__(self, *, source: annize.fs.FsEntry, title: str, repository: Repository, package_name: str,
                 project_short_hint_name: str = None, package_short_name: str = None):
        flatpakreffile = FlatpakrefFile(refname=package_short_name, package_name=package_name,
                                        title=project_short_hint_name, repository=repository)
        gpgfile = GpgFile(refname=package_short_name, gpgkey=b"TODO abc")
        super().__init__(title=title, files=[flatpakreffile, gpgfile])
        self.__repository = repository
        self.__source = source
        self.__package_name = package_name
        self.__project_short_hint_name = project_short_hint_name
        self.__package_short_name = package_short_name
        self.__flatpak_built = False

    def get_files(self):
        if not self.__flatpak_built:
            self.__repository.upload(FlatpakImage(source=self.__source, package_name=self.__package_name))
            self.__flatpak_built = True
        return super().get_files()

    @property
    def description(self):
        distrihowtos = ""
        project_short_hint_name = self.__project_short_hint_name or annize.features.base.pretty_project_name()
        repository_friendly_name = self.__repository.friendly_name_suggestion
        repository_public_url = self.__repository.public_url
        package_name = self.__package_name
        for distriname, distrihowto in {  # TODO howto list still up to date?
            "archlinux": annize.i18n.TrStr.tr("an_Dist_FlatpakDesc_distrihowto_archlinux"),
            "centos": annize.i18n.TrStr.tr("an_Dist_FlatpakDesc_distrihowto_centos"),
            "debian": annize.i18n.TrStr.tr("an_Dist_FlatpakDesc_distrihowto_debian"),
            "fedora": annize.i18n.TrStr.tr("an_Dist_FlatpakDesc_distrihowto_fedora"),
            "gentoo": annize.i18n.TrStr.tr("an_Dist_FlatpakDesc_distrihowto_gentoo"),
            "opensuse": annize.i18n.TrStr.tr("an_Dist_FlatpakDesc_distrihowto_opensuse"),
            "redhat": annize.i18n.TrStr.tr("an_Dist_FlatpakDesc_distrihowto_redhat"),
            "ubuntu": annize.i18n.TrStr.tr("an_Dist_FlatpakDesc_distrihowto_ubuntu")
        }.items():
            distrihowtos += (f".. container:: annizedoc-infobutton\n\n"
                             f"  .. image:: annizeicons/{distriname}.png\n\n"
                             f"  .. hint:: \n    {distrihowto}\n\n")
        intro = annize.i18n.TrStr.tr("an_Dist_FlatpakDesc").format(**locals())
        outrotxt = annize.i18n.TrStr.tr("an_Dist_FlatpakDescOutro")
        outroposttxt = annize.i18n.TrStr.tr("an_Dist_FlatpakDescOutroPost")
        outro = annize.i18n.TODO(
            ".. rst-class:: annizedoc-infobutton-stop\n\n"
            "{outrotxt}\n\n"
            ".. code-block:: sh\n\n"
            "  $ flatpak remote-add --user --no-gpg-verify {repository_friendly_name} {repository_public_url}\n"
            "  $ flatpak install --user {repository_friendly_name} {package_name}\n"
            "  $ flatpak run {package_name}\n\n"
            "{outroposttxt}").format(**locals())
        return annize.i18n.TODO("{intro}\n\n{distrihowtos}\n\n{outro}").format(**locals())
"""TODO zz (maybe this should be even mentioned first?!)
or install it with just:

$ flatpak install --user --from https://pseudopolis.eu/wiki/pino/projs/foo/foo.flatpakref
"""


class FlatpakrefFile(annize.fs.AdHocFsEntry):

    def __init__(self, *, refname: str = None, package_name: str, title: str = None, branch: str = "master",
                 runtime_repository_url: str = None, gpgkey: bytes = None, repository: Repository):
        super().__init__()
        self.__refname = refname
        self.__package_name = package_name
        self.__title = title
        self.__branch = branch
        self.__runtime_repository_url = runtime_repository_url
        self.__gpgkey = gpgkey
        self.__repository = repository

    def _initialize(self):
        refname = self.__refname or annize.features.base.project_name()
        title = self.__title or refname
        res = {"Title": title, "Name": self.__package_name, "Branch": self.__branch,
               "Url": self.__repository.public_url, "IsRuntime": "False"}
        if self.__gpgkey:
            res["GPGKey"] = self.__gpgkey.decode()
        if self.__runtime_repository_url:  # TODO
            res["RuntimeRepo"] = self.__runtime_repository_url
        flatpakrefcont = "\n".join([f"{x}={res[x]}" for x in res])
        return annize.fs.temp.TempFileByContent(content=f"[Flatpak Ref]\n{flatpakrefcont}\n",
                                                filename=f"{refname}.flatpakref")


class GpgFile(annize.fs.AdHocFsEntry):

    def _initialize(self):
        refname = self.__refname or annize.features.base.project_name()
        return annize.fs.temp.TempFileByContent(content="TODO zz fritten.gpg",
                                                filename=f"{refname}.gpg")

    def __init__(self, *, refname: str = None, gpgkey: bytes = None):
        super().__init__()
        self.__refname = refname
        self.__gpgkey = gpgkey


class FlatpakImage(annize.fs.AdHocFsEntry):

    @annize.callconv.parameter_from_childnodes("source")
    def __init__(self, *, source: annize.fs.FsEntry, package_name: str, sockets: t.Iterable[str] = ("x11",),
                 filesystems: t.Iterable[str] = ("home",), shares: t.Iterable[str] = ("network",)):
        super().__init__()
        self.__source = source
        self.__package_name = package_name
        self.__sockets = sockets
        self.__filesystems = filesystems
        self.__shares = shares

    def _initialize(self):
        return self._mkpackage(self._BuildInfo(source=self.__source,  name=self.__package_name, sdk="org.freedesktop.Sdk", platform="org.freedesktop.Platform", kitversion="19.08",
                                               command=None,
                                               sockets=self.__sockets,
                                               filesystems=self.__filesystems,
                                               shares=self.__shares,
                                               menu_entries=[],
                                               environment={}))

    @dataclasses.dataclass()
    class _BuildInfo:
        source: annize.fs.FsEntry
        name: str
        sdk: str
        platform: str
        kitversion: t.Optional[str]
        command: t.Optional[str] #TODO
        sockets: t.Iterable[str]
        filesystems: t.Iterable[str]
        shares: t.Iterable[str]
        menu_entries: t.Iterable[MenuEntry]
        environment: t.Dict[str, str]  # TODO
        pkgrootpath: str = None
        pkgpath_share: str = None
        pkgpath_share_applications: str = None
        pkgpath_share_icons: str = None
        result: annize.fs.FsEntry = None

    @classmethod
    def _mkpackage_prepareinfos(cls, build: _BuildInfo, tmpdir: str) -> None:
        build.pkgrootpath = f"{tmpdir}/pkg"
        build.pkgpath_share = f"{build.pkgrootpath}/export/share"
        build.pkgpath_share_applications = f"{build.pkgpath_share}/applications"
        build.pkgpath_share_icons = f"{build.pkgpath_share}/icons"
        for pkgpath in [build.pkgpath_share_applications, build.pkgpath_share_icons]:
            os.makedirs(f"{build.pkgrootpath}/{pkgpath}", exist_ok=True)

    @classmethod
    def _mkpackage_flatpak_build_init(cls, build: _BuildInfo) -> None:
        kitversionopts = [build.kitversion] if build.kitversion else []
        subprocess.check_call(["flatpak", "build-init", build.pkgrootpath, build.name, build.sdk, build.platform,
                               *kitversionopts])

    @classmethod
    def _mkpackage_applysource(cls, build: _BuildInfo) -> None:
        build.source.owned().move_to(build.pkgrootpath, path_is_parent=True, merge=True)

    @classmethod
    def _mkpackage_flatpak_build_finish(cls, build: _BuildInfo) -> None:
        opts = []
        if build.command:
            opts.append(f"--command={build.command}")
        for s in build.sockets:
            opts.append(f"--socket={s}")
        for s in build.filesystems:
            opts.append(f"--filesystem={s}")
        for s in build.shares:
            opts.append(f"--share={s}")
        for envk, envv in build.environment.items():
            opts.append(f"--env={envk}={envv}")
        subprocess.check_call(["flatpak", "build-finish", build.pkgrootpath])

    @classmethod
    def _mkpackage_share(cls, build: _BuildInfo) -> None:
        for menuentry in build.menu_entries:
            iconfname = f"{build.name}.{menuentry.name}.png"
            menuentry.icon.copy_to(f"{build.pkgpath_share_icons}/{iconfname}")
            with open(f"{build.pkgpath_share_applications}/{build.name}.{menuentry.name}.desktop", "w") as f:
                f.write(f"[Desktop Entry]\n"
                        f"Name={menuentry.title}\n"
                        f"Exec={menuentry.command}\n"
                        f"Terminal={'false' if menuentry.gui else 'true'}\n"
                        f"Type=Application\n"
                        f"Categories={menuentry.category[1]};\n"
                        f"Icon={iconfname}\n")

    @classmethod
    def _mkpackage_flatpak_build_export(cls, build: _BuildInfo) -> None:
        build.result = annize.fs.temp.fresh_temp_dir()
        respath = build.result.owned().path()
        opts = [] # TODO zz gpg stoff
        subprocess.check_call(["flatpak", "build-export", *opts, respath, build.pkgrootpath])
        subprocess.check_call(["flatpak", "build-update-repo", *opts, respath])

    @classmethod
    def _mkpackage(cls, build: _BuildInfo) -> annize.fs.FsEntry:
        with annize.fs.temp.fresh_temp_dir() as tmpdir:
            # TODO review impl
            cls._mkpackage_prepareinfos(build, tmpdir.owned().path())
            cls._mkpackage_flatpak_build_init(build)
            cls._mkpackage_applysource(build)
            cls._mkpackage_flatpak_build_finish(build)
            cls._mkpackage_flatpak_build_export(build)
            return build.result

"""
TODO
            if milieu.call("flatpak", "--version", inside_sandbox=False)[0] != 0:
                raise .framework.exceptions.RequirementsMissingError("'flatpak' seems to be unavailable")
"""
