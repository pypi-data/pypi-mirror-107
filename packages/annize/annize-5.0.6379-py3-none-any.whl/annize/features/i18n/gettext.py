# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import os
import subprocess

import annize.callconv
import annize.features.base
import annize.fs.temp


class UpdatePOs:

    @annize.callconv.parameter_from_childnodes("po_directory")
    def __init__(self, *, po_directory: annize.fs.FsEntry):
        self.__po_directory = po_directory

    def __call__(self, *args, **kwargs):
        #TODO zz
        podir = self.__po_directory.readable_path()  # TODO weird
        srcdir = annize.features.base.project_directory()
        allfiles = []
        for dirtup in os.walk(srcdir):
            for f in dirtup[2]:
                ff = f"{dirtup[0]}/{f}"
                if [suf for suf in [".py", ".ui", ".xml"] if ff.endswith(suf)]:
                    allfiles.append(ff)  # TODO  arg list gets very long
        with annize.fs.temp.fresh_temp_dir() as tmpdir:
            potfile = tmpdir.owned().child_by_relative_path("pot.pot").path()
            subprocess.check_call(["xgettext", "--keyword=tr", "--add-comments", "--from-code", "utf-8", "--sort-output", "-o", potfile, *allfiles])
            for fpofile in os.listdir(podir):  # TODO zz only *.po ?!
                subprocess.check_call(["msgmerge", "--no-fuzzy-matching", "--backup=none", "--update", f"{podir}/{fpofile}", potfile])


class GenerateMOs:

    def __init__(self, *, po_directory: annize.fs.FsEntry, mo_directory: annize.fs.FsEntry):
        self.__po_directory = po_directory
        self.__mo_directory = mo_directory

    def __call__(self, *args, **kwargs):
        # TODO zz
        podir = self.__po_directory.readable_path()  # TODO weird
        mosdir = self.__mo_directory.readable_path()  # TODO weird
        for pofile in os.listdir(podir):
            outdir = f"{mosdir}/{pofile[:-3]}/LC_MESSAGES"
            os.makedirs(outdir, exist_ok=True)
            subprocess.check_call(["msgfmt", f"--output-file={outdir}/annize.mo", f"{podir}/{pofile}"])  # TODO zz hardcoded annize.mo
