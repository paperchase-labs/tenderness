# Copyright 2026 Pavel Stepachev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import annotations

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


def main() -> None:

    # select colors
    color_selector = ColorSelector()
    white = SolidColorSpec(color=color_selector.by_names(["white"])[0])
    black = SolidColorSpec(color=color_selector.by_names(["black"])[0])

    # select surface (image, pdf, svg, etc.)
    img_surface_config = SurfaceConfigManager().create_image_surface_config(width=400, height=100)

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
    render_result = pipeline.render(blocks_config=doc_blocks_config, setup_result=setup_result)  # noqa: F841

    # save the rendered document to a file
    pipeline.save_as_file(
        surface=setup_result.surface,
        surface_config=img_surface_config,
        output_file_path=pathlib.Path("hello_world"),
    )


if __name__ == "__main__":
    main()
