# SPDX-FileCopyrightText: © 2021 Josef Hahn
# SPDX-License-Identifier: AGPL-3.0-only

import colorsys
import typing as t


class Color:

    def __init__(self, *, red: float, green: float, blue: float):
        self.__red = min(max(0.0, red), 1.0)
        self.__green = min(max(0.0, green), 1.0)
        self.__blue = min(max(0.0, blue), 1.0)

    @property
    def red(self) -> float:
        return self.__red

    @property
    def green(self) -> float:
        return self.__green

    @property
    def blue(self) -> float:
        return self.__blue

    @property
    def html_color_spec(self) -> str:
        def htmlcolorpart(v):
            return ("0" + hex(v)[2:])[-2:]
        larger, largeg, largeb = (round(x * 255) for x in (self.red, self.green, self.blue))
        return f"#{htmlcolorpart(larger)}{htmlcolorpart(largeg)}{htmlcolorpart(largeb)}"

    def scalehue(self, *, brightness: float, saturation: t.Optional[float] = None) -> "Color":
        # pylint: disable=unused-variable, invalid-name
        h, l, s = colorsys.rgb_to_hls(self.red, self.green, self.blue)
        if saturation is not None:
            s *= saturation
            if s > 1:
                s = 1.0
        r, g, b = colorsys.hls_to_rgb(h, brightness, s)
        return Color(red=r, green=g, blue=b)

    def transformed(self, *, brightness: t.Optional[float] = None, saturation: t.Optional[float] = None) -> "Color":
        # pylint: disable=unused-variable, invalid-name
        resh, resl, ress = colorsys.rgb_to_hls(self.red, self.green, self.blue)
        resl = resl if (brightness is None) else brightness
        ress = ress if (saturation is None) else saturation
        r, g, b = colorsys.hls_to_rgb(resh, resl, ress)
        return Color(red=r, green=g, blue=b)

# TODO nicer api
