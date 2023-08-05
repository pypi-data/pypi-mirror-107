import pathlib
import re

import frontmatter

from slipy_assets import Template, Slide


def update_build_context(data, src_dir="src"):
    src_dir = pathlib.Path(src_dir)
    index = src_dir / "index.html"
    with open(index) as f:
        data["index"] = f.read()
