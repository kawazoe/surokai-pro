#!/usr/bin/env python3

import datetime
import os
import shutil

import glob
import yaml

import colors
import jinja2

print("Setup...")

# functional
def ident():
    return lambda c: c

def pipe(first, *args):
  for fn in args:
    first = fn(first)
  return first

def flow(*args):
    return lambda first: pipe(first, *args)

# colors
def rotate(deg):
    return lambda c: c.rotate(deg)

def scale(sat, lum):
    return lambda c: c.scale(sat, lum)

def blend(color, ratio):
    return lambda c: c.blend(color, ratio)

# io
def read(path):
    with open(path) as f:
        return yaml.safe_load(f.read())

def readTheme(path):
    data = read(path)
    return {
        **data,
        "colors": {
            k: colors.HslColor.parse(v) for k, v in data["colors"].items()
        }
    }

# data
shades = {
    "dark": readTheme("./themes/dark.yaml"),
    "light": readTheme("./themes/light.yaml")
}

grades = {
    "dark": {
        "name": "",
        "shade": shades["dark"],
        "tweaks": {}
    },
    "deep": {
        "name": "Deep",
        "shade": shades["dark"],
        "tweaks": {
            # accents
            "red":        flow(blend(colors.HslColor.parse("hsl(130, 48%, 66.0%)"), 0.1), scale(0, 0)),
            "orange":     flow(blend(colors.HslColor.parse("hsl(120, 48%, 66.0%)"), 0.1), scale(0.1, 0)),
            "yellow":     flow(blend(colors.HslColor.parse("hsl(110, 48%, 66.0%)"), 0.1), scale(0, 0)),
            "green":      flow(blend(colors.HslColor.parse("hsl(90, 48%, 66.0%)"), 0.2), scale(0, 0)),
            "blue":       flow(blend(colors.HslColor.parse("hsl(50, 48%, 66.0%)"), 0.4), scale(-0.1, 0.2)),
            "purple":     flow(blend(colors.HslColor.parse("hsl(20, 48%, 66.0%)"), 0.3), scale(-0.2, 0)),

            # high contrast accents
            "darkRed":    blend(colors.HslColor.parse("hsl(220, 68%, 16.0%)"), 0.09),
            "darkOrange": blend(colors.HslColor.parse("hsl(220, 68%, 16.0%)"), 0.09),
            "darkYellow": blend(colors.HslColor.parse("hsl(220, 68%, 16.0%)"), 0.09),
            "darkGreen":  blend(colors.HslColor.parse("hsl(220, 68%, 16.0%)"), 0.09),
            "darkBlue":   blend(colors.HslColor.parse("hsl(220, 68%, 16.0%)"), 0.09),
            "darkPurple": blend(colors.HslColor.parse("hsl(220, 68%, 16.0%)"), 0.09),

            # grays
            "bright2":    blend(colors.HslColor.parse("hsl(220, 26%, 96.0%)"), 0.5),
            "bright1":    blend(colors.HslColor.parse("hsl(220, 26%, 90.0%)"), 0.5),
            "normal":     blend(colors.HslColor.parse("hsl(220, 26%, 82.0%)"), 0.4),
            "dimmed1":    blend(colors.HslColor.parse("hsl(220, 32%, 68.0%)"), 0.4),
            "dimmed2":    blend(colors.HslColor.parse("hsl(220, 33%, 50.0%)"), 0.3),
            "dimmed3":    blend(colors.HslColor.parse("hsl(220, 42%, 30.0%)"), 0.3),
            "dimmed4":    blend(colors.HslColor.parse("hsl(220, 43%, 24.0%)"), 0.3),
            "background": blend(colors.HslColor.parse("hsl(220, 42%, 21.5%)"), 0.3),
            "darker1":    blend(colors.HslColor.parse("hsl(224, 38%, 18.0%)"), 0.25),
            "darker2":    blend(colors.HslColor.parse("hsl(224, 37%, 14.0%)"), 0.25),
            "darker3":    blend(colors.HslColor.parse("hsl(228, 36%, 11.2%)"), 0.2),
            "darker4":    blend(colors.HslColor.parse("hsl(228, 35%, 8.5%)"), 0.2),
            "black":      blend(colors.HslColor.parse("hsl(234, 35%, 5.6%)"), 0.2)
        }
    },
    "weathered": {
        "name": "Weathered",
        "shade": shades["dark"],
        "tweaks": {
            # accents
            "red":        flow(blend(colors.HslColor.parse("hsl(66, 64%, 38.0%)"), 0.1), scale(0.1, 0)),
            "orange":     flow(blend(colors.HslColor.parse("hsl(66, 64%, 38.0%)"), 0.1), scale(0.1, 0)),
            "yellow":     flow(blend(colors.HslColor.parse("hsl(66, 64%, 38.0%)"), 0.1), scale(0.1, 0)),
            "green":      flow(blend(colors.HslColor.parse("hsl(66, 64%, 38.0%)"), 0.1), scale(0.1, 0)),
            "blue":       flow(blend(colors.HslColor.parse("hsl(66, 64%, 38.0%)"), 0.1), scale(0.1, 0)),
            "purple":     flow(blend(colors.HslColor.parse("hsl(66, 64%, 38.0%)"), 0.1), scale(0.1, 0)),

            # high contrast accents
            "darkRed":    blend(colors.HslColor.parse("hsl(66, 76%, 8.0%)"), 0.25),
            "darkOrange": blend(colors.HslColor.parse("hsl(66, 76%, 8.0%)"), 0.25),
            "darkYellow": blend(colors.HslColor.parse("hsl(66, 76%, 8.0%)"), 0.25),
            "darkGreen":  blend(colors.HslColor.parse("hsl(66, 76%, 8.0%)"), 0.25),
            "darkBlue":   blend(colors.HslColor.parse("hsl(66, 76%, 8.0%)"), 0.25),
            "darkPurple": blend(colors.HslColor.parse("hsl(66, 76%, 8.0%)"), 0.25),

            # grays
            "bright2":    flow(scale(0, -0.1), blend(colors.HslColor.parse("hsl(59, 13%, 97.0%)"), 0.4)),
            "bright1":    flow(scale(0, -0.1), blend(colors.HslColor.parse("hsl(60, 12%, 92.0%)"), 0.4)),
            "normal":     flow(scale(0, -0.1), blend(colors.HslColor.parse("hsl(60, 11%, 82.0%)"), 0.4)),
            "dimmed1":    flow(scale(0, -0.1), blend(colors.HslColor.parse("hsl(61, 10%, 66.0%)"), 0.4)),
            "dimmed2":    flow(scale(0, -0.1), blend(colors.HslColor.parse("hsl(61, 10%, 37.0%)"), 0.4)),
            "dimmed3":    flow(scale(0, -0.12), blend(colors.HslColor.parse("hsl(63, 10%, 28.0%)"), 0.4)),
            "dimmed4":    flow(scale(0, -0.12), blend(colors.HslColor.parse("hsl(66, 10%, 21.0%)"), 0.4)),
            "background": flow(scale(0, -0.12), blend(colors.HslColor.parse("hsl(78, 11%, 14.5%)"), 0.4)),
            "darker1":    flow(scale(0, -0.1), blend(colors.HslColor.parse("hsl(84, 11%, 10.5%)"), 0.4)),
            "darker2":    flow(scale(0, -0.08), blend(colors.HslColor.parse("hsl(85, 11%, 8.5%)"), 0.3)),
            "darker3":    flow(scale(0, -0.06), blend(colors.HslColor.parse("hsl(86, 12%, 5.6%)"), 0.3)),
            "darker4":    flow(scale(0, -0.04), blend(colors.HslColor.parse("hsl(87, 13%, 4.3%)"), 0.3)),
            "black":      flow(scale(0, -0.02), blend(colors.HslColor.parse("hsl(87, 14%, 2.4%)"), 0.3))
        }
    },
    "rustic": {
        "name": "Rustic",
        "shade": shades["dark"],
        "tweaks": {
            # accents
            "red":        flow(blend(colors.HslColor.parse("hsl(10, 48%, 66.0%)"), 0.18), scale(0, 0)),
            "orange":     flow(blend(colors.HslColor.parse("hsl(10, 48%, 66.0%)"), 0.18), scale(0, 0)),
            "yellow":     flow(blend(colors.HslColor.parse("hsl(10, 48%, 66.0%)"), 0.18), scale(0, 0)),
            "green":      flow(blend(colors.HslColor.parse("hsl(10, 48%, 66.0%)"), 0.21), scale(-0.1, 0)),
            "blue":       flow(blend(colors.HslColor.parse("hsl(10, 48%, 66.0%)"), 0.25), scale(-0.12, 0)),
            "purple":     flow(blend(colors.HslColor.parse("hsl(10, 48%, 66.0%)"), 0.29), scale(-0.15, 0)),

            # high contrast accents
            "darkRed":    blend(colors.HslColor.parse("hsl(10, 68%, 14.0%)"), 0.12),
            "darkOrange": blend(colors.HslColor.parse("hsl(10, 68%, 14.0%)"), 0.12),
            "darkYellow": blend(colors.HslColor.parse("hsl(10, 68%, 14.0%)"), 0.12),
            "darkGreen":  blend(colors.HslColor.parse("hsl(10, 68%, 14.0%)"), 0.12),
            "darkBlue":   blend(colors.HslColor.parse("hsl(10, 68%, 14.0%)"), 0.12),
            "darkPurple": blend(colors.HslColor.parse("hsl(10, 68%, 14.0%)"), 0.12),

            # grays
            "bright2":    blend(colors.HslColor.parse("hsl(10, 23%, 98.0%)"), 0.4),
            "bright1":    blend(colors.HslColor.parse("hsl(10, 24%, 91.0%)"), 0.4),
            "normal":     blend(colors.HslColor.parse("hsl(10, 25%, 75.0%)"), 0.25),
            "dimmed1":    blend(colors.HslColor.parse("hsl(11, 26%, 62.0%)"), 0.25),
            "dimmed2":    blend(colors.HslColor.parse("hsl(12, 27%, 34.0%)"), 0.2),
            "dimmed3":    blend(colors.HslColor.parse("hsl(14, 27%, 26.0%)"), 0.2),
            "dimmed4":    blend(colors.HslColor.parse("hsl(15, 27%, 20.0%)"), 0.175),
            "background": blend(colors.HslColor.parse("hsl(16, 26%, 16.5%)"), 0.175),
            "darker1":    blend(colors.HslColor.parse("hsl(18, 26%, 14.0%)"), 0.175),
            "darker2":    blend(colors.HslColor.parse("hsl(19, 26%, 12.0%)"), 0.175),
            "darker3":    blend(colors.HslColor.parse("hsl(20, 25%, 11.2%)"), 0.15),
            "darker4":    blend(colors.HslColor.parse("hsl(22, 25%, 10.5%)"), 0.15),
            "black":      blend(colors.HslColor.parse("hsl(23, 24%, 8.6%)"), 0.15)
        }
    },
    "matrix": {
        "name": "Matrix",
        "shade": shades["dark"],
        "tweaks": {
            # accents
            "red":        flow(blend(colors.HslColor.parse("hsl(165, 84%, 48.0%)"), 0.1), scale(0.1, 0)),
            "orange":     flow(blend(colors.HslColor.parse("hsl(165, 84%, 48.0%)"), 0.1), scale(0.2, 0)),
            "yellow":     flow(blend(colors.HslColor.parse("hsl(165, 84%, 48.0%)"), 0.1), scale(0.2, 0)),
            "green":      flow(blend(colors.HslColor.parse("hsl(165, 84%, 48.0%)"), 0.2), scale(0, 0)),
            "blue":       flow(blend(colors.HslColor.parse("hsl(165, 84%, 48.0%)"), 0.2), scale(-0.2, 0)),
            "purple":     flow(blend(colors.HslColor.parse("hsl(165, 84%, 48.0%)"), 0.2), scale(-0.2, 0)),

            # high contrast accents
            "darkRed":    blend(colors.HslColor.parse("hsl(185, 76%, 14.0%)"), 0.18),
            "darkOrange": blend(colors.HslColor.parse("hsl(185, 76%, 14.0%)"), 0.18),
            "darkYellow": blend(colors.HslColor.parse("hsl(185, 76%, 14.0%)"), 0.18),
            "darkGreen":  blend(colors.HslColor.parse("hsl(185, 76%, 14.0%)"), 0.18),
            "darkBlue":   blend(colors.HslColor.parse("hsl(185, 76%, 14.0%)"), 0.18),
            "darkPurple": blend(colors.HslColor.parse("hsl(185, 76%, 14.0%)"), 0.18),

            # grays
            "bright2":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(210, 13%, 97.0%)"), 0.5)),
            "bright1":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(210, 14%, 92.0%)"), 0.5)),
            "normal":     flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(210, 15%, 82.0%)"), 0.5)),
            "dimmed1":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(210, 16%, 66.0%)"), 0.5)),
            "dimmed2":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(210, 17%, 51.0%)"), 0.5)),
            "dimmed3":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(205, 19%, 36.0%)"), 0.5)),
            "dimmed4":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(205, 22%, 26.0%)"), 0.5)),
            "background": flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(200, 24%, 21.5%)"), 0.5)),
            "darker1":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(195, 26%, 15.0%)"), 0.5)),
            "darker2":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(190, 27%, 11.5%)"), 0.5)),
            "darker3":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(185, 27%, 8.5%)"), 0.5)),
            "darker4":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(180, 28%, 6.5%)"), 0.5)),
            "black":      flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(175, 28%, 4.6%)"), 0.5))
        }
    },
    "classic": {
        "name": "Classic",
        "shade": shades["dark"],
        "tweaks": {
            # accents
            "red":        flow(blend(colors.HslColor.parse("hsl(0, 82%, 64.0%)"), 0.14), scale(-0.05, -0.1)),
            "orange":     flow(blend(colors.HslColor.parse("hsl(12, 88%, 64.0%)"), 0.14), scale(0, -0.05)),
            "yellow":     flow(blend(colors.HslColor.parse("hsl(38, 92%, 64.0%)"), 0.14), scale(0, 0)),
            "green":      flow(blend(colors.HslColor.parse("hsl(60, 84%, 64.0%)"), 0.14), scale(0, -0.05)),
            "blue":       flow(blend(colors.HslColor.parse("hsl(80, 84%, 64.0%)"), 0.14), scale(0, -0.1)),
            "purple":     flow(blend(colors.HslColor.parse("hsl(110, 84%, 64.0%)"), 0.14), scale(0, -0.1)),

            # high contrast accents
            "darkRed":    blend(colors.HslColor.parse("hsl(115, 76%, 9.0%)"), 0.28),
            "darkOrange": blend(colors.HslColor.parse("hsl(115, 76%, 9.0%)"), 0.28),
            "darkYellow": blend(colors.HslColor.parse("hsl(115, 76%, 9.0%)"), 0.28),
            "darkGreen":  blend(colors.HslColor.parse("hsl(115, 76%, 9.0%)"), 0.28),
            "darkBlue":   blend(colors.HslColor.parse("hsl(115, 76%, 9.0%)"), 0.28),
            "darkPurple": blend(colors.HslColor.parse("hsl(115, 76%, 9.0%)"), 0.28),

            # grays
            "bright2":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(110, 12%, 97.0%)"), 0.5)),
            "bright1":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(110, 12%, 87.0%)"), 0.5)),
            "normal":     flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(110, 12%, 73.0%)"), 0.5)),
            "dimmed1":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(110, 13%, 58.0%)"), 0.5)),
            "dimmed2":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(110, 14%, 41.0%)"), 0.5)),
            "dimmed3":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(105, 14%, 30.0%)"), 0.5)),
            "dimmed4":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(105, 15%, 22.0%)"), 0.5)),
            "background": flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(100, 15%, 16.5%)"), 0.45)),
            "darker1":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(95, 17%, 12.0%)"), 0.45)),
            "darker2":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(90, 18%, 10.5%)"), 0.4)),
            "darker3":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(85, 19%, 7.5%)"), 0.4)),
            "darker4":    flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(80, 21%, 5.5%)"), 0.4)),
            "black":      flow(scale(-0.5, 0), blend(colors.HslColor.parse("hsl(75, 23%, 3.6%)"), 0.4))
        }
    },
    "light": {
        "name": "",
        "shade": shades["light"],
        "tweaks": { }
    },
    "sun": {
        "name": "Sun",
        "shade": shades["light"],
        "tweaks": { }
    }
}

colors = {
    "%s-%s" % (grade["shade"]["id"], gk): {
        "id": "%s-%s" % (grade["shade"]["id"], gk),
        "name": "%s (%s grade)" % (grade["shade"]["name"], grade["name"]) if grade["name"] else grade["shade"]["name"],
        "dark": grade["shade"]["dark"],
        "sources": {
            tc: color.formatHex() for tc, color in grade["shade"]["colors"].items()
        },
        "grades": {
            tc: (
                grade["tweaks"][tc](color).formatHex()
                if tc in grade["tweaks"]
                else color.formatHex()
            ) for tc, color in grade["shade"]["colors"].items()
        }
    } for gk, grade in grades.items()
}

jinjaEnv = jinja2.Environment(loader=jinja2.FileSystemLoader("templates"))

print("Cleaning...")

shutil.rmtree("resources/schemes")
shutil.rmtree("resources/theme")

print("Generating...")

os.makedirs("resources/schemes")
os.makedirs("resources/theme")

now = datetime.datetime.now().isoformat()

def render(target, template, data={}):
    output = jinjaEnv.get_template(template).render(**data).strip()
    with open(target, 'w+') as f:
        f.write(output)

for theme in colors.values():
    # schemes
    render(f"resources/schemes/{theme['id']}.xml", "scheme.xml", {
        "date": now, "theme": theme, "italics": True
    })
    render(f"resources/schemes/{theme['id']}-no-italics.xml", "scheme.xml", {
        "date": now, "theme": theme, "italics": False
    })

    # themes
    render(f"resources/theme/{theme['id']}.theme.json", "theme.json", {
        "theme": theme, "dark": theme["dark"]
    })

print("Done")
