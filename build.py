#!/usr/bin/env python3
import sublate as sub

print("Loading colors...")

sub.data.update({
    "date": sub.date_iso(),
    "colors": sub.read("colors/*.yaml").values(),
})

print("Cleaning...")

sub.rm("resources/schemes")
sub.rm("resources/theme")

print("Generating...")

sub.mkdir("resources/schemes")
sub.mkdir("resources/theme")

for theme in sub.data["colors"]:
    # schemes
    sub.render(f"resources/schemes/{theme['id']}.xml", "templates/scheme.xml", {
        "theme": theme, "italics": True
    })
    sub.render(f"resources/schemes/{theme['id']}-no-italics.xml", "templates/scheme.xml", {
        "theme": theme, "italics": False
    })

    # themes
    sub.render(f"resources/theme/{theme['id']}.theme.json", "templates/theme.json", {
        "theme": theme
    })

print("Done")
