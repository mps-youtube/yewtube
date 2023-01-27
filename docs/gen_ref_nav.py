#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Generate the code reference pages and navigation."""

from pathlib import Path

import mkdocs_gen_files

nav = mkdocs_gen_files.Nav()

skip_files = [
    (Path("mps_youtube") / "config.py"),
    (Path("mps_youtube") / "mpris.py"),
]
skip_files.extend((Path("mps_youtube") / "test").glob("*.py"))
for path in sorted(Path("mps_youtube").glob("**/*.py")):
    if path in skip_files:
        continue
    module_path = path.with_suffix("")
    doc_path = path.relative_to("mps_youtube").with_suffix(".md")
    full_doc_path = Path("reference", doc_path)

    parts = list(module_path.parts)
    parts[-1] = f"{parts[-1]}.py"
    nav[parts] = doc_path

    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        ident = ".".join(module_path.parts)
        print("::: " + ident, file=fd)

    mkdocs_gen_files.set_edit_path(full_doc_path, path)

with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
