# GED-HTML

Converting GED files to static web pages.

Example:

[https://genealogie.vanveen.io](https://genealogie.vanveen.io)

Usage:

```bash
python -m gedhtml tests/data/kennedies.ged -o tests/output/kennedies -t "Kennedy Genealogy" -d "Genealogy of the Kennedy family." -l EN
```

For help:

```bash
python -m gedhtml --help
```

CSS layout taken from:

[Pure CSS](https://github.com/pure-css/pure/tree/master/site/static/layouts/side-menu)
