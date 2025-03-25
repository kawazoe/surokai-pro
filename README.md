# Surokai Pro

The unofficial Monokai Pro theme, adapted by [Subtheme](https://subtheme.dev) and now maintained by [kawazoe](https://github.com/kawazoe/surokai-pro). This repository includes the default theme, classic theme, and four filters: Machine, Octagon, Ristretto, and Spectrum. Credit goes to the original creator: [https://monokai.pro](https://monokai.pro).

Download the latest build from [Releases](https://github.com/subtheme-dev/monokai-pro/releases).

Supported apps:
- [iTerm](theme/iterm)
- [JetBrains](theme/jetbrains)
- [Lapce](theme/lapce)
- [Terminal](theme/terminal)

## Building the theme

We recommend running pythong in a virtual environment:

```
$ python3 -m venv main
$ source ./main/bin/activate
```

To build, first install [sublate](https://github.com/espositocode/sublate):

```
$ pip install sublate
```

Then, run the build script:

```
$ ./build.py
```
