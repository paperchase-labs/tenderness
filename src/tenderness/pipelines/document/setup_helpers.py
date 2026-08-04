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

"""Document setup helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from tenderness.core.geometry import Rectangle
from tenderness.core.sentinel import _UNSET_PARAM
from tenderness.layout_engines.position_helpers import PositionHelpers

if TYPE_CHECKING:
    import cairo

    from tenderness.cairo_backend.surface_configuration import SurfaceRect
    from tenderness.core.geometry import Margin, Rectangle
    from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexBox
    from tenderness.pipelines.document.pipeline_schema import DocumentConfig
    from tenderness.pipelines.renderer_configurator import RendererConfigurator


@dataclass(slots=True)
class BlockPosition:
    """Named block with its resolved rectangle.

    Attributes
    ----------
    name
        Block identifier, or ``None`` if unnamed.
    rect
        Block's bounding rectangle in document coordinates.
    """

    name: str | None
    rect: Rectangle


class DocumentSetupHelpers:
    """Static helpers for the document setup phase."""

    @staticmethod
    def apply_background_color(
        renderer_configurator: RendererConfigurator,
        config: DocumentConfig,
        cairo_context: cairo.Context[cairo.Surface],
    ) -> None:
        """Fill the surface background if ``config.background_spec`` is set.

        Parameters
        ----------
        renderer_configurator
            Renderer used to apply the background.
        config
            Document configuration.
        cairo_context
            Target Cairo context.
        """
        if config.background_spec is not _UNSET_PARAM:
            renderer_configurator.background_selector.add_background_color(
                cairo_context=cairo_context,
                surface_config=config.surface_config,
                background_color_spec=config.background_spec,
            )

    @staticmethod
    def apply_global_margin(
        config: DocumentConfig,
        surface_rect: SurfaceRect,
    ) -> tuple[Rectangle, Margin]:
        """Compute content rect and margin from the surface rect and ``config.global_margin``.

        Parameters
        ----------
        config
            Document configuration.
        surface_rect
            Full surface rectangle.

        Returns
        -------
        tuple[Rectangle, Margin]
            Content rectangle and applied margin.
        """
        if config.global_margin is not _UNSET_PARAM:
            content_rect, canvas_margin = PositionHelpers.inset_rect(
                rect=surface_rect,
                margin=config.global_margin,
            )
        else:
            content_rect, canvas_margin = PositionHelpers.inset_rect(
                rect=surface_rect,
            )

        return content_rect, canvas_margin

    @staticmethod
    def resolve_block_positions(
        minimal_flexbox_engine: MinimalFlexBox,
        config: DocumentConfig,
        content_rect: Rectangle,
    ) -> list[BlockPosition]:
        """Resolve block positions from ``config.block_spec`` within ``content_rect``.

        If ``config.block_spec`` is a ``list[BlockPosition]``, it is used as-is,
        bypassing the flexbox engine.

        Parameters
        ----------
        minimal_flexbox_engine
            Engine used to resolve the layout tree.
        config
            Document configuration.
        content_rect
            Available content area.

        Returns
        -------
        list[BlockPosition]
            Computed positions for each block.
        """
        if isinstance(config.block_spec, list):
            block_positions = config.block_spec
        elif config.block_spec is not _UNSET_PARAM:
            result_tree = minimal_flexbox_engine.resolve_tree(
                container=content_rect,
                node=config.block_spec,
            )
            block_positions = [BlockPosition(name=node.name, rect=rect) for node, rect in result_tree]
        else:
            block_positions = [BlockPosition(name="main", rect=content_rect)]

        return block_positions
