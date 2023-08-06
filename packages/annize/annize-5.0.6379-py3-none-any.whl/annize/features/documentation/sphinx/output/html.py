# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import html
import json
import os
import typing as t

import annize.aux
import annize.features.base
import annize.features.documentation.common
import annize.features.documentation.sphinx._utils
import annize.features.documentation.sphinx.output.common
import annize.fs
import annize.i18n


class HtmlOutputSpec(annize.features.documentation.common.HtmlOutputSpec):

    #TODO
    def __init__(self, *, is_homepage: bool = False, title: t.Optional[str] = None, short_title: t.Optional[str] = None,
                 short_desc: t.Optional[str] = None, theme: t.Optional[str] = None, masterlink: t.Optional[str] = None,
                 logo_image: t.Optional[annize.fs.FsEntry] = None,
                 background_image: t.Optional[annize.fs.FsEntry] = None):#TODO parameters useful here?
        """
        :param path: The output path.
        :param theme: The sphinx html theme name.
        :param homepagemode: If to render output for a homepage with slight different stylings and behaviors.
        :param title: The html title.
        :param short_title: The short html title.
        :param short_desc: The short description. Ignored by most themes.
        :param masterlink: Url that overrides the target of the main heading (which is also a link).
        """
        super().__init__(is_homepage=is_homepage, title=title)#TODO always just pass *args,**kwargs
        self.__short_title = short_title
        self.__short_desc = short_desc
        self.__theme = theme
        self.__masterlink = masterlink#TODO weg hier?!
        self.__logo_image = logo_image
        self.__background_image = background_image

    @property
    def short_title(self) -> t.Optional[str]:
        return self.__short_title

    @property
    def short_desc(self) -> t.Optional[str]:
        return self.__short_desc

    @property
    def theme(self) -> t.Optional[str]:
        return self.__theme

    @property
    def masterlink(self) -> t.Optional[str]:
        return self.__masterlink

    @property
    def logo_image(self) -> t.Optional[annize.fs.FsEntry]:
        return self.__logo_image

    @property
    def background_image(self) -> t.Optional[annize.fs.FsEntry]:
        return self.__background_image


@annize.features.documentation.sphinx.output.common.register_output_generator
class HtmlOutputGenerator(annize.features.documentation.sphinx.output.common.OutputGenerator):
    """
    HTML documentation output.
    """

    @classmethod
    def is_compatible_for(cls, outputspec):
        return isinstance(outputspec, annize.features.documentation.common.HtmlOutputSpec)

    def formatname(self):
        return "html"

    def prepare_generate(self, geninfo):#TODO geninfo.outdir weg?!
        geninfo.entry_path = f"{geninfo.configvalues['master_doc']}.html"
        title = str(self.outputspec.title)
        is_homepage = self.outputspec.is_homepage
        if isinstance(self.outputspec, HtmlOutputSpec):
            masterlink = self.outputspec.masterlink
            short_title = self.outputspec.short_title
            short_desc = self.outputspec.short_desc  # TODO i18n broken
            theme = self.outputspec.theme
            logo_image = self.outputspec.logo_image
            background_image = self.outputspec.background_image
        else:
            masterlink = None
            short_title = None  # TODO use
            short_desc = None  # TODO use
            theme = None  # TODO use .title
            logo_image = None
            background_image = None
        # TODO noh anis.framework.files.... copy_to: if not given a string argument, take .path() ?!
        short_desc = str(short_desc or "")
        theme = theme or "pimpinella_anisum"
        geninfo.configvalues["html_theme"] = theme
        htmlthemepaths = geninfo.configvalues["html_theme_path"] = geninfo.configvalues.get("html_theme_path", [])
        htmlthemepaths.append(annize.aux.data_path)
        ato = dict(sidebartreesmall=not is_homepage, menusectionindicator=not is_homepage, shortdesc=short_desc)
        if short_title or title:
            geninfo.configvalues["html_short_title"] = str(short_title or title)
        if title:
            geninfo.configvalues["html_title"] = title
        if masterlink:
            ato["masterlink"] = masterlink
        htmlstatpaths = geninfo.configvalues["html_static_path"] = geninfo.configvalues.get("html_static_path", [])
        if theme == "pimpinella_anisum":
            geninfo.configvalues["html_css_files"] = html_css_files = []
            basecolor = annize.features.base.brand_color()

            # TODO hacks
            background_image = annize.fs.fsentry_by_path(f"{annize.features.base.project_directory()}/_meta/background.png")  # TODO
            if not background_image.exists():
                background_image = background_image.parent().child_by_relative_path("background.jpg")
            for logo_image in annize.fs.fsentry_by_path(f"{annize.features.base.project_directory()}/_meta/media/logo").children():  # TODO
                if logo_image.basename().endswith(".64.png"):
                    break


            if background_image:
                bgimagename = f"_annize_bgimage.{background_image.basename()}"
                bgimagecssdirfs = geninfo.intstruct.child_by_relative_path(bgimagename)
                bgimagecssfs = bgimagecssdirfs.child_by_relative_path(bgimagename)
                background_image.copy_to(bgimagecssfs.path())
                htmlstatpaths.append(bgimagecssdirfs.readable_path())
                ato["bgimage"] = bgimagename  # TODO does that rlly work (on all dir levels)?!
            for bcaa in range(10):
                for bcab in range(10):
                    for bcac in range(20):
                        sbcac = "abcdefghijklmnopqrst"[bcac]
                        ncolor = basecolor.scalehue(brightness=(bcab+1)/10, saturation=(bcac+1)/10)
                        ato[f"brandingcolor_{sbcac}{bcaa}{bcab}"] = (  # TODO only some of them
                            f"rgb({ncolor.red * 255},{ncolor.green * 255},{ncolor.blue * 255},"
                            f"{(bcaa + 1) / 10})")
        if is_homepage:
            ato.update(sidebarhidelvl1=True, headhidelvl1=True, sidebarhidelvl3up=True, shorthtmltitle=True)
        # TODO weird
        htmlthemeopts = geninfo.configvalues["html_theme_options"] = geninfo.configvalues.get("html_theme_options", {})
        htmlthemeopts.update(ato)
        # TODO
        htmlstatpaths.append("/home/pino/projects/annize/src/annize/_static/icons/docrender")
        if logo_image:
            geninfo.configvalues["html_logo"] = logo_image.readable_path()

    def multilanguage_frame(self, document):
        result = super().multilanguage_frame(document)
        htmllinks = ""
        for language in result.languages:
            langname = annize.i18n.get_culture(language).english_lang_name
            langentrypath = result.entry_path_for_language(language)
            htmllinks += f"<a href='{html.escape(langentrypath)}'>{html.escape(langname)}</a><br/>"
        languageentrypoints = {language: result.entry_path_for_language(language) for language in result.languages}
        # TODO generate via sphinx instead?!
        result.file.owned(allow_clone=False).child_by_relative_path("index.html").write_file(
            f"<!DOCTYPE html>"
            f"<html>"
            f"<head>"
            f"<meta charset='utf-8'><title>{html.escape(str(self.outputspec.title))}</title>"
            f"<script>"
            f"var myLanguage = navigator.language;"
            f"var languageEntryPoints = {json.dumps(languageentrypoints)};"
            f"function trylang(c) {{"
            f"    var entrypoint = languageEntryPoints[c];"
            f"    if (entrypoint) {{"
            f"        document.location.href = entrypoint;"
            f"        return true;"
            f"    }}"
            f"}};"
            f"trylang(myLanguage) || trylang(myLanguage.substring(0,2)) || trylang('en') || trylang('?');"
            f"</script>"
            f"</head>"
            f"<body>"
            f"<h1>🗣 🌐 ❓</h1>"
            f"{htmllinks}"
            f"</body>"
            f"</html>")  # TODO what with language = "?" ?!
        result._set_entry_path("index.html")
        return result
