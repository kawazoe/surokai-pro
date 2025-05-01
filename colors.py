from abc import ABC, abstractmethod

import colorsys
import re
import math

class Color(ABC):
    @abstractmethod
    def humanize(self):
        pass

    def formatHex(self):
        return self.toRgb().formatHex()

    @abstractmethod
    def toHsl(self):
        pass

    @abstractmethod
    def toRgb(self):
        pass

    def rotate(self, deg):
        return self.toHsl().rotate(deg)

    def scale(self, sat, lum):
        return self.toHsl().scale(sat, lum)

    def blend(self, color, ratio):
        return self.toRgb().blend(color, ratio)

class HslColor(Color):
    parseRegExp = re.compile(
        "hsl\\("
            "(?P<h>\\d+(\\.\\d+)?), ?"
            "(?P<s>\\d+(\\.\\d+)?)%, ?"
            "(?P<l>\\d+(\\.\\d+)?)%"
        "\\)"
    )

    @staticmethod
    def parse(str):
        matches = HslColor.parseRegExp.search(str)
        hsl = matches.groupdict()

        return HslColor.fromHuman(
            max(0, min(360, float(hsl["h"]))),
            max(0, min(100, float(hsl["s"]))),
            max(0, min(100, float(hsl["l"])))
        )

    @staticmethod
    def fromNormalized(h, s, l):
        return HslColor((h, s, l))

    @staticmethod
    def fromHuman(h, s, l):
        return HslColor((h / 360, s / 100, l / 100))

    def __init__(self, hsl):
        super().__init__()
        self.hsl = hsl

    def __str__(self):
        (h, s, l) = self.humanize()
        return f"hsl({h}, {s}%, {l}%)"

    def humanize(self):
        (h, s, l) = self.hsl
        return (h * 360, s * 100, l * 100)

    def toHsl(self):
        return self

    def toRgb(self):
        (h, s, l) = self.hsl
        return RgbColor(colorsys.hls_to_rgb(h, l, s))

    def rotate(self, deg):
        (h, s, l) = self.hsl
        return HslColor((((h * 360 + deg) % 360) / 360, s, l))

    def scale(self, sat, lum):
        (h, s, l) = self.hsl
        fn = lambda v, s: v + ((1-v if s>=0 else v) * s)
        return HslColor((h, fn(s, sat), fn(l, lum)))

class RgbColor(Color):
    parseRegExp = re.compile(
        "rgb\\("
            "(?P<r>\\d+), ?"
            "(?P<g>\\d+), ?"
            "(?P<b>\\d+)"
        "\\)"
    )

    @staticmethod
    def parse(str):
        matches = RgbColor.parseRegExp.search(str)
        rgb = matches.groupdict()

        return RgbColor.fromHuman(
            max(0, min(255, int(hsl["r"]))),
            max(0, min(255, int(hsl["g"]))),
            max(0, min(255, int(hsl["b"])))
        )

    @staticmethod
    def fromNormalized(r, g, b):
        return RgbColor((r, g, b))

    @staticmethod
    def fromHuman(r, g, b):
        return RgbColor((r / 256, g / 256, b / 256))

    def __init__(self, rgb):
        super().__init__()
        self.rgb = rgb

    def __str__(self):
        (r, g, b) = self.humanize()
        return f"rgb({r}, {g}, {b})"

    def formatHex(self):
        (r, g, b) = self.humanize()
        fn = lambda v: "%0.2x" % v
        return f"#{fn(r)}{fn(g)}{fn(b)}"

    def humanize(self):
        (r, g, b) = self.rgb
        fn = lambda v: min(255, int(v * 256))
        return (fn(r), fn(g), fn(b))

    def toHsl(self):
        (h, l, s) = colorsys.rgb_to_hls(*self.rgb)
        return HslColor((h, s, l))

    def toRgb(self):
        return self

    def blend(self, color, ratio):
        (ar, ag, ab) = self.rgb
        (br, bg, bb) = color.toRgb().rgb

        fn = lambda a, b: math.sqrt(((1 - ratio) * (a ** 2)) + (ratio * b ** 2))

        return RgbColor.fromNormalized(
            fn(ar, br),
            fn(ag, bg),
            fn(ab, bb)
        )
