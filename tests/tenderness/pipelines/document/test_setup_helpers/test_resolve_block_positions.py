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

import pytest

from tenderness.cairo_backend.pixel_formats import PixelFormat
from tenderness.cairo_backend.surface_configuration import ImageSurfaceConfig
from tenderness.core.color_models import ColorModel
from tenderness.core.geometry import Rectangle
from tenderness.core.image_formats import ImageFormat
from tenderness.core.sentinel import _UNSET_PARAM
from tenderness.image_backend.image_backends import ImageBackend
from tenderness.layout_engines.minimal_flexbox.flex_container_properties import FlexContainerProperties
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexBox, MinimalFlexNode
from tenderness.pipelines.document.pipeline_schema import DocumentConfig
from tenderness.pipelines.document.setup_helpers import BlockPosition, DocumentSetupHelpers


def _make_surface_config() -> ImageSurfaceConfig:
    return ImageSurfaceConfig(
        width=300,
        height=100,
        color_model=ColorModel.RGB,
        image_format=ImageFormat.PNG,
        image_backend=ImageBackend.CAIRO,
        pixel_format=PixelFormat.RGB24,
    )


def make_config(*, block_spec: object = _UNSET_PARAM) -> DocumentConfig:
    return DocumentConfig(surface_config=_make_surface_config(), block_spec=block_spec)  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# block_spec unset (_UNSET_PARAM)
# ---------------------------------------------------------------------------
class TestUnsetBlockSpec:
    def test_default_returns_single_named_main_block(
        self,
        flexbox_engine: MinimalFlexBox,
        content_rect: Rectangle,
    ) -> None:
        config = make_config()

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert positions == [BlockPosition(name="main", rect=content_rect)]

    def test_explicit_sentinel_matches_omitted_default(
        self,
        flexbox_engine: MinimalFlexBox,
        content_rect: Rectangle,
    ) -> None:
        """Passing ``_UNSET_PARAM`` explicitly must behave identically to omitting block_spec."""
        config = make_config(block_spec=_UNSET_PARAM)

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert positions == [BlockPosition(name="main", rect=content_rect)]

    def test_zero_area_content_rect_still_returns_main_block(self, flexbox_engine: MinimalFlexBox) -> None:
        zero_rect = Rectangle(x=10, y=10, width=0, height=0)
        config = make_config()

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=zero_rect,
        )

        assert positions == [BlockPosition(name="main", rect=zero_rect)]

    def test_negative_dimensions_passed_through_verbatim(self, flexbox_engine: MinimalFlexBox) -> None:
        """content_rect is never normalized/clamped — negative width/height survive as-is."""
        negative_rect = Rectangle(x=0, y=0, width=-50, height=-25)
        config = make_config()

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=negative_rect,
        )

        assert positions[0].rect.width == -50
        assert positions[0].rect.height == -25


# ---------------------------------------------------------------------------
# block_spec = MinimalFlexNode (flexbox engine path)
# ---------------------------------------------------------------------------
class TestFlexNodeBlockSpec:
    def test_flat_leaves_resolved_in_source_order(
        self,
        flexbox_engine: MinimalFlexBox,
        content_rect: Rectangle,
    ) -> None:
        root = MinimalFlexNode(
            size=(300, 100),
            container_props=FlexContainerProperties(),
            children=[
                MinimalFlexNode(size=(150, 100), name="left"),
                MinimalFlexNode(size=(150, 100), name="right"),
            ],
        )
        config = make_config(block_spec=root)

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert [p.name for p in positions] == ["left", "right"]
        assert positions[0].rect.x == pytest.approx(0)
        assert positions[1].rect.x == pytest.approx(150)

    def test_nested_containers_flatten_to_leaves_only(
        self,
        flexbox_engine: MinimalFlexBox,
        content_rect: Rectangle,
    ) -> None:
        """Intermediate container nodes must never surface as a BlockPosition — only leaves."""
        root = MinimalFlexNode(
            size=(300, 100),
            container_props=FlexContainerProperties(),
            children=[
                MinimalFlexNode(size=(100, 100), name="sidebar"),
                MinimalFlexNode(
                    size=(200, 100),
                    name="nested_container",
                    container_props=FlexContainerProperties(),
                    children=[
                        MinimalFlexNode(size=(200, 50), name="header"),
                        MinimalFlexNode(size=(200, 50), name="footer"),
                    ],
                ),
            ],
        )
        config = make_config(block_spec=root)

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert [p.name for p in positions] == ["sidebar", "header", "footer"]
        assert "nested_container" not in [p.name for p in positions]

    def test_unnamed_leaf_yields_none_name(
        self,
        flexbox_engine: MinimalFlexBox,
        content_rect: Rectangle,
    ) -> None:
        root = MinimalFlexNode(
            size=(300, 100),
            container_props=FlexContainerProperties(),
            children=[MinimalFlexNode(size=(300, 100))],
        )
        config = make_config(block_spec=root)

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert positions == [BlockPosition(name=None, rect=Rectangle(x=0, y=0, width=300, height=100))]

    def test_leaf_root_without_container_props_raises_value_error(
        self,
        flexbox_engine: MinimalFlexBox,
        content_rect: Rectangle,
    ) -> None:
        """A leaf node (container_props=None) is not a valid root — must not be silently accepted."""
        leaf_root = MinimalFlexNode(size=(300, 100))
        config = make_config(block_spec=leaf_root)

        with pytest.raises(ValueError, match="resolve_tree requires a container node"):
            DocumentSetupHelpers.resolve_block_positions(
                minimal_flexbox_engine=flexbox_engine,
                config=config,
                content_rect=content_rect,
            )

    def test_container_with_no_children_returns_empty_list(
        self,
        flexbox_engine: MinimalFlexBox,
        content_rect: Rectangle,
    ) -> None:
        root = MinimalFlexNode(size=(300, 100), container_props=FlexContainerProperties(), children=[])
        config = make_config(block_spec=root)

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert positions == []


# ---------------------------------------------------------------------------
# block_spec = list[BlockPosition] (explicit positions, bypasses the engine)
# ---------------------------------------------------------------------------
class TestExplicitListBlockSpec:
    def test_used_verbatim_by_identity(self, flexbox_engine: MinimalFlexBox, content_rect: Rectangle) -> None:
        explicit_positions = [
            BlockPosition(name="header", rect=Rectangle(x=0, y=0, width=300, height=20)),
            BlockPosition(name="body", rect=Rectangle(x=0, y=20, width=300, height=80)),
        ]
        config = make_config(block_spec=explicit_positions)

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert positions is explicit_positions
        assert positions[0] is explicit_positions[0]
        assert positions[1] is explicit_positions[1]

    def test_empty_list_returns_no_blocks(self, flexbox_engine: MinimalFlexBox, content_rect: Rectangle) -> None:
        config = make_config(block_spec=[])

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert positions == []

    def test_single_block_position(self, flexbox_engine: MinimalFlexBox, content_rect: Rectangle) -> None:
        only_block = BlockPosition(name="solo", rect=Rectangle(x=5, y=5, width=10, height=10))
        config = make_config(block_spec=[only_block])

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert positions == [only_block]

    def test_duplicate_names_are_not_deduplicated(
        self,
        flexbox_engine: MinimalFlexBox,
        content_rect: Rectangle,
    ) -> None:
        duplicated = [
            BlockPosition(name="dup", rect=Rectangle(x=0, y=0, width=10, height=10)),
            BlockPosition(name="dup", rect=Rectangle(x=10, y=10, width=10, height=10)),
        ]
        config = make_config(block_spec=duplicated)

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert [p.name for p in positions] == ["dup", "dup"]
        assert positions[0].rect != positions[1].rect

    def test_unnamed_entries_preserved(self, flexbox_engine: MinimalFlexBox, content_rect: Rectangle) -> None:
        mixed = [
            BlockPosition(name=None, rect=Rectangle(x=0, y=0, width=10, height=10)),
            BlockPosition(name="named", rect=Rectangle(x=10, y=10, width=10, height=10)),
        ]
        config = make_config(block_spec=mixed)

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=content_rect,
        )

        assert [p.name for p in positions] == [None, "named"]

    def test_content_rect_is_not_consulted(self, flexbox_engine: MinimalFlexBox) -> None:
        """Explicit positions bypass the engine entirely — a wildly different content_rect changes nothing."""
        explicit_positions = [BlockPosition(name="fixed", rect=Rectangle(x=0, y=0, width=10, height=10))]
        config = make_config(block_spec=explicit_positions)
        unrelated_content_rect = Rectangle(x=9999, y=9999, width=1, height=1)

        positions = DocumentSetupHelpers.resolve_block_positions(
            minimal_flexbox_engine=flexbox_engine,
            config=config,
            content_rect=unrelated_content_rect,
        )

        assert positions == explicit_positions
        assert positions[0].rect == Rectangle(x=0, y=0, width=10, height=10)
