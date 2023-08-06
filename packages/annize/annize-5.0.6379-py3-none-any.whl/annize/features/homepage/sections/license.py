# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import annize.context
import annize.features.base
import annize.features.homepage.common
import annize.features.licensing
import annize.i18n


class Section(annize.features.homepage.common.HomepageSection):

    def __init__(self, *, head=annize.i18n.TrStr.tr("an_HP_Head_License"), sortindex=20_000):
        super().__init__(head=head, sortindex=sortindex)  # TODO i18n

    def _generate(self, info):
        licenses = annize.features.licensing.project_licenses()
        if len(licenses) > 0:
            projectname = annize.features.base.pretty_project_name() or "This project"#TODO i18n
            licdescs = []
            for ilic, lic in enumerate(licenses):
                if lic.text:
                    licfilename = f"_license_{ilic}.txt"
                    info.document_variant_directory.child_by_relative_path(licfilename).write_file(str(lic.text))
                    licdescs.append(f"`{lic.name} <{info.document_variant_url}{licfilename}>`_")
                else:
                    licdescs.append(lic.name)
            licdesc = ", ".join(licdescs[:-1]) + (" and " if len(licenses) > 1 else "") + licdescs[-1]
            return annize.i18n.tr("an_HP_Lic_Text").format(**locals())
        return None
