
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/assets/logo/tenderness-lockup-horizontal-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="docs/assets/logo/tenderness-lockup-horizontal-light.svg">
  <img alt="Fallback image description" src="docs/assets/logo/tenderness-lockup-horizontal-dark.svg">
</picture>

<p align="center">
  <a href="https://github.com/paperchase-labs/tenderness"><img src="https://img.shields.io/badge/source-GitHub-181717?logo=github&logoColor=white&style=flat" alt="Source Code"/></a>
  <a href="https://github.com/paperchase-labs/tenderness-examples"><img src="https://img.shields.io/badge/examples-GitHub-181717?logo=github&logoColor=white&style=flat" alt="Examples"/></a>
  <a href="https://paperchase-labs.github.io/tenderness/"><img src="https://img.shields.io/badge/docs-online-75528b?logo=github&logoColor=white&style=flat" alt="Documentation"/></a>
  <a href="https://pypi.org/project/tenderness"><img src="https://img.shields.io/pypi/v/tenderness?logo=python&logoColor=white&label=PyPI" alt="Python Package Index"/></a>
  <a href="https://pypi.org/project/tenderness"><img src="https://img.shields.io/pypi/pyversions/tenderness?logo=python&logoColor=white&style=flat" alt="Python versions"/></a>
</p>
<p align="center">
  <a href="https://github.com/astral-sh/ruff"><img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff"/></a>
  <a href="https://github.com/pre-commit/pre-commit"><img src="https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=flat" alt="pre-commit"/></a>
  <a href="https://numpydoc.readthedocs.io/en/latest/format.html"><img src="https://img.shields.io/badge/docstrings-NumPy-4DABCF?logo=numpy&logoColor=white&style=flat" alt="NumPy docstrings"/></a>
  <a href="https://github.com/jsh9/pydoclint"><img src="https://img.shields.io/badge/pydoclint-checked-4DABCF?logo=python&logoColor=white&style=flat" alt="pydoclint"/></a>
  <a href="https://mypy-lang.org/"><img src="https://img.shields.io/badge/type--checked-mypy-blue?logo=python&logoColor=white&style=flat" alt="mypy"/></a>
  <a href="https://github.com/paperchase-labs/tenderness/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-4caf50?logo=apache&logoColor=white&style=flat" alt="License: Apache-2.0"/></a>
</p>

**tenderness** is a fast library for *synthetic*, deterministic document rendering from text and images, powered by [Cairo](https://www.cairographics.org/) and [Pango](https://docs.gtk.org/Pango/index.html).


## Why tenderness?

Most document datasets don’t come from real structure — they come from reconstruction. Text is rendered, then reverse-engineered back into layout using OCR, heuristics, or fragile parsing pipelines. The result is noisy, incomplete, and not reproducible.

**tenderness** flips this entirely.

It renders text directly into documents producing images, SVGs, and PDFs with fully known layout from the start. Every character placement, line break, and block position is defined at render time — not inferred afterward.


## What this gives you

- Generate large-scale synthetic document datasets
- Provide precise structural supervision for vision-language models
- Build benchmarks for layout understanding systems
- Ground-truth layout across characters, clusters, runs, and lines

**No OCR. No heuristics. No reconstruction. No manual annotation.**

Just text in → fully structured document out.


## Main Features

 - **Multi-format output**: Render text and images into Image, SVG, PDF, or NumPy arrays.

 - **Composable content blocks**: Build documents from simple primitives: `TextBlock`, `ImageBlock`, and `TableBlock`.

 - **Minimal flexbox layout engine**: A lightweight system that automatically resolves positioning and flow.

 - **Exact bounding boxes (OBB + AABB, logical + ink)**: Extract multi-level data for text (character, cluster, run, line, layout) and blocks.

 - **Rich typography & text flow**: Custom fonts, hierarchical styling, Pango markup, automatic font fallback, and overflow-aware text continuation across blocks.

 - **Composable pipelines**: Use the built-in pipeline with pre-defined layouts, or build your own from scratch.


## Quick Start

```bash
pip install tenderness
```

```python
import pathlib

from tenderness.cairo_backend.color_patterns import SolidColorSpec
from tenderness.cairo_backend.surface_config_manager import SurfaceConfigManager
from tenderness.colors.color_selector import ColorSelector
from tenderness.pango_backend.font_description_interface import FontDescriptionInterfaceParameters
from tenderness.pipelines.document import (
    DocumentBlocksConfig,
    DocumentConfig,
    DocumentRenderPipeline,
    TextBlock,
    TextStyle,
)

# select colors
color_selector = ColorSelector()
white = SolidColorSpec(color=color_selector.by_names(["white"])[0])
black = SolidColorSpec(color=color_selector.by_names(["black"])[0])

# select surface (image, pdf, svg, etc.)
img_surface_config = SurfaceConfigManager().create_image_surface_config(
    width=400,
    height=100,
)

# create document config and blocks config
doc_config = DocumentConfig(surface_config=img_surface_config, background_spec=white)
doc_blocks_config = DocumentBlocksConfig(
    surface_config=img_surface_config,
    blocks=[
        TextBlock(
            text="Hello, world!",
            text_style=TextStyle(
                font_description_params=FontDescriptionInterfaceParameters(size=32),
                text_color_spec=black,
            ),
        ),
    ],
)

# create pipeline and render document
pipeline = DocumentRenderPipeline()
setup_result = pipeline.setup(config=doc_config)
render_result = pipeline.render(
    blocks_config=doc_blocks_config,
    setup_result=setup_result,
)

# save the rendered document to a file
pipeline.save_as_file(
    surface=setup_result.surface,
    surface_config=img_surface_config,
    output_file_path=pathlib.Path("hello_world"),
)

# The output file will be saved as `hello_world.png` in the current working directory.
```

You can find the runnable version at [`scripts/mini_example.py`](scripts/mini_example.py), and more examples over at [tenderness-examples](https://github.com/paperchase-labs/tenderness-examples). If you run into missing system libraries (Cairo, Pango, PyGObject), check the [install guide](https://paperchase-labs.github.io/tenderness/setup/install/).


## Citation

```bibtex
@software{tenderness,
  author  = {Stepachev, Pavel},
  title   = {tenderness: A fast library for synthetic, deterministic document and text rendering},
  url     = {https://github.com/paperchase-labs/tenderness},
  year    = {2026}
}
```