# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import os
import subprocess

import annize.features.documentation.sphinx.output.common


@annize.features.documentation.sphinx.output.common.register_output_generator
class PdfOutputGenerator(annize.features.documentation.sphinx.output.common.OutputGenerator):
    """
    PDF documentation output.
    """

    @classmethod
    def is_compatible_for(cls, outputspec):
        return isinstance(outputspec, annize.features.documentation.common.PdfOutputSpec)

    def formatname(self):
        return "latex"

    def postproc(self, preresult):
        preresult = preresult.owned()
        subprocess.check_call(["make"], cwd=preresult.path())
        for potresult in preresult.children():
            if potresult.basename().endswith(".pdf"):
                return potresult.disowned()
        raise Exception("TODO")

    def resultpath(self, projectname, buildpath):#TODO
        for f in os.listdir(f"{buildpath}/latex"):
            if f.endswith(".pdf"):
                return f"latex/{f}"
        raise annize.framework.exceptions.InternalError("No pdf found in build output.")
