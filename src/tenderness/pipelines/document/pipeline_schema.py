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

"""Document pipeline schema."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tenderness.core.geometry import Margin
from tenderness.core.sentinel import _UNSET_PARAM, Settable

if TYPE_CHECKING:
    import io

    import cairo

    from tenderness.cairo_backend.color_patterns import PatternColorSpec
    from tenderness.cairo_backend.surface_configuration import SurfaceConfig, SurfaceRect
    from tenderness.core.geometry import Margin, Rectangle
    from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexNode
    from tenderness.pipelines.document.image_block_helpers import ImageBlock, ImageBlockResult
    from tenderness.pipelines.document.setup_helpers import BlockPosition
    from tenderness.pipelines.document.table_block_helpers import TableBlock, TableBlockResult
    from tenderness.pipelines.document.text_block_helpers import TextBlock, TextBlockResult, TextStyle


@dataclass(slots=True, kw_only=True)
class BaseBlock:
    """Base class for document block configurations.

    Attributes
    ----------
    block_name
        Block identifier, or ``None`` if unnamed.
    """

    block_name: str | None = None


@dataclass(slots=True)
class DocumentConfig:
    """Configuration for the document setup phase.

    Attributes
    ----------
    surface_config
        Surface dimensions and output settings.
    global_margin
        Margin applied around the content area.
    block_spec
        Block arrangement specification; resolves to block positions. Either a :class:`MinimalFlexNode` tree resolved by the flexbox engine, or a ``list[BlockPosition]`` of pre-computed positions used as-is. Positions are absolute document coordinates, same as a resolved flex tree's - they are not offset by ``global_margin``.
    background_spec
        Background fill pattern.
    """

    surface_config: SurfaceConfig
    global_margin: Settable[Margin] = _UNSET_PARAM
    block_spec: Settable[MinimalFlexNode | list[BlockPosition]] = _UNSET_PARAM
    background_spec: Settable[PatternColorSpec] = _UNSET_PARAM


@dataclass(slots=True)
class DocumentBlocksConfig:
    """Configuration for the document render phase.

    Attributes
    ----------
    surface_config
        Surface dimensions and output settings.
    blocks
        Content blocks to render.
    base_text_style
        Default text style applied to all text blocks.
    """

    surface_config: SurfaceConfig
    blocks: list[TextBlock | ImageBlock | TableBlock]
    base_text_style: Settable[TextStyle] = (
        _UNSET_PARAM  # Base text style applied to all TextBlocks (can be overridden by block-level styles)
    )


@dataclass(slots=True)
class DocumentSetupResult:
    """Output of the document setup phase.

    Attributes
    ----------
    surface_rect
        Full surface rectangle.
    content_rect
        Content area after applying the document margin.
    document_margin
        Applied document margin.
    block_positions
        Computed position and size for each block.
    surface
        Cairo surface.
    stream
        Output byte stream, or ``None`` for file-backed surfaces.
    cairo_context
        Cairo drawing context.
    surface_config
        Surface configuration used during setup.
    """

    surface_rect: SurfaceRect
    content_rect: Rectangle
    document_margin: Margin
    block_positions: list[BlockPosition]
    surface: cairo.Surface
    stream: io.BytesIO | None
    cairo_context: cairo.Context[cairo.Surface]
    surface_config: SurfaceConfig


@dataclass(slots=True)
class DocumentRenderResult:
    """Output of the document render phase.

    Attributes
    ----------
    rendered_blocks
        Results for each rendered block.
    """

    rendered_blocks: list[TextBlockResult | ImageBlockResult | TableBlockResult]
