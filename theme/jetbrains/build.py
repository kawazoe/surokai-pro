import sublate as sub

print("[+] JetBrains")

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

sub.rm("templates")
sub.rm("build.py")
