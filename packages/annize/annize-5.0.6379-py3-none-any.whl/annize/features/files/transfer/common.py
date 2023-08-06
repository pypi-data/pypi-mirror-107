# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import contextlib
import shlex
import tarfile
import typing as t

import annize.callconv
import annize.data
import annize.fs.temp


class Endpoint:

    def access_filesystem(self, rootpath: str) -> t.ContextManager[annize.fs.FsEntry]:
        raise NotImplementedError()


class FsEndpoint(Endpoint):

    @annize.callconv.parameter_from_childnodes("fsentry")
    def __init__(self, *, fsentry: annize.fs.FsEntry = None, path: str = None):#TODO path ?!
        super().__init__()
        self.__fs = fsentry or annize.fs.fsentry_by_path(path, is_ownable=True)

    @contextlib.contextmanager
    def access_filesystem(self, rootpath: str) -> t.ContextManager[annize.fs.FsEntry]:
        yield self.__fs.child_by_relative_path(rootpath)


class Upload:

    @annize.callconv.parameter_from_childnodes("destination_endpoint")
    @annize.callconv.parameter_from_childnodes("source")
    def __init__(self, *, source: annize.fs.FsEntry, destination_endpoint: Endpoint, destination_path: str):
        self.__source = source
        self.__destination_endpoint = destination_endpoint
        self.__destination_path = "/" + destination_path.lstrip("/")#TODO dedup

    def __call__(self) -> None:
        """TODO
        umask = os.umask(0)
        os.umask(umask)
        def _chmod(_p):
            for x in os.listdir(_p):
                px = _p+"/"+x
                os.chmod(px, (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) & ~umask)
                if os.path.isdir(px):
                    _chmod(px)
        _chmod(hp.path)
        sshtgt = f"{self.__connection.username}@{self.__connection.host}:{self.__destination_path}"
        """
        fdestination = annize.fs.fsentry_by_path(self.__destination_path, is_ownable=True).child_by_relative_path(self.__source.basename()).owned()
        if getattr(self.__destination_endpoint, "has_shell_access", False):
            self.__destination_endpoint.exec(f"mkdir -p {shlex.quote(self.__destination_path)}")
            with annize.fs.temp.fresh_temp_dir() as tmpdir:  # TODO fresh_temp_dir(owned=True) ?!
                xfertarfs = tmpdir.child_by_relative_path("x.tgz").owned()
                with tarfile.open(xfertarfs.path(), "w:gz") as tar:
                    tar.add(self.__source.readable_path(), arcname=self.__source.basename())
                with self.__destination_endpoint.access_filesystem(self.__destination_path) as destfs:
                    xfertarfsdest = destfs.child_by_relative_path(f"{annize.data.UniqueId().long_str}.tgz").owned()
                    xfertarfs.move_to(xfertarfsdest.path())
            self.__destination_endpoint.exec(f"rm -rf {shlex.quote(fdestination.path())};"
                                             f"cd {shlex.quote(self.__destination_path)};"
                                             f"tar xfz {shlex.quote(xfertarfsdest.basename())};"
                                             f"rm {shlex.quote(xfertarfsdest.basename())}")
        else:
            with self.__destination_endpoint.access_filesystem(self.__destination_path) as destfs:
                self.__source.copy_to(destfs.child_by_relative_path(self.__source.basename()).owned().path(), overwrite=True)
