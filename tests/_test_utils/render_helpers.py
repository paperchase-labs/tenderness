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

from typing import TYPE_CHECKING

import cairo
import gi

if TYPE_CHECKING:
    import pathlib
    from collections.abc import Sequence

    from tenderness.bounding_boxes.bounding_boxes_schema import BoundingBox, BoundingBoxWithInk, Quadrilateral

from tenderness.cairo_backend.color_patterns import SolidColorSpec
from tenderness.colors.color_selector import ColorSelector
from tenderness.font_setup.font_setup import FontSetup
from tenderness.font_setup.fontconfig_managers import FontconfigMode
from tests._test_utils.paths_test import TEST_FONTS_DIR

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
from gi.repository import Pango, PangoCairo  # noqa: E402

_TESTUTIL_COLOR_SELECTOR = ColorSelector()
_TESTUTIL_SOLID_COLOR_WHITE = SolidColorSpec(color=_TESTUTIL_COLOR_SELECTOR.by_names(["white"])[0])
_TESTUTIL_SOLID_COLOR_BLACK = SolidColorSpec(color=_TESTUTIL_COLOR_SELECTOR.by_names(["black"])[0])


def _testutil_setup_fonts(fontconfig_destination_dir: pathlib.Path) -> pathlib.Path:
    """Set up fonts for testing and return the path to the generated fontconfig file."""
    fontconfig_destination_dir.mkdir(parents=True, exist_ok=True)
    font_setup = FontSetup()
    fontconfig_file_path = font_setup.setup_font(
        mode=FontconfigMode.TEMPLATE_MINIMAL,
        font_dir=TEST_FONTS_DIR,
        fontconfig_destination_dir=fontconfig_destination_dir,
    )
    return fontconfig_file_path  # noqa: RET504


def _testutil_assert_no_quadrilateral_overlap(
    quads: list[Quadrilateral],
    *,
    label: str = "bbox",
    tolerance: float = 0.5,
) -> None:
    """Assert that no two quadrilaterals overlap by more than *tolerance* pixels.

    Adjacent boxes that merely share an edge are not considered overlapping.
    *tolerance* absorbs sub-pixel floating-point rounding.
    """
    rects: list[tuple[float, float, float, float]] = []
    for q in quads:
        xs = (q.top_left[0], q.top_right[0], q.bottom_right[0], q.bottom_left[0])
        ys = (q.top_left[1], q.top_right[1], q.bottom_right[1], q.bottom_left[1])
        rects.append((min(xs), min(ys), max(xs), max(ys)))

    for i in range(len(rects)):
        for j in range(i + 1, len(rects)):
            x1_min, y1_min, x1_max, y1_max = rects[i]
            x2_min, y2_min, x2_max, y2_max = rects[j]
            overlap_x = min(x1_max, x2_max) - max(x1_min, x2_min)
            overlap_y = min(y1_max, y2_max) - max(y1_min, y2_min)
            assert not (overlap_x > tolerance and overlap_y > tolerance), (
                f"{label}[{i}] and {label}[{j}] overlap by ({overlap_x:.2f} px, {overlap_y:.2f} px)"
            )


def _testutil_assert_no_logical_bbox_overlap(
    bboxes: Sequence[BoundingBox],
    *,
    tolerance: float = 0.5,
) -> None:
    """Assert no two logical_bboxes overlap. Not safe for CHAR level (ZWJ/VS-16 may share space)."""
    _testutil_assert_no_quadrilateral_overlap(
        [b.logical_bbox for b in bboxes], label="logical_bbox", tolerance=tolerance
    )


def _testutil_assert_no_ink_bbox_overlap(
    bboxes: Sequence[BoundingBoxWithInk],
    *,
    tolerance: float = 0.5,
) -> None:
    """Assert no two ink_bboxes overlap. Not safe for CHAR level (ZWJ/VS-16 may share space)."""
    _testutil_assert_no_quadrilateral_overlap([b.ink_bbox for b in bboxes], label="ink_bbox", tolerance=tolerance)


def _testutil_simple_text(
    text: str,
    family_name: str,
    font_size: int,
    height: int = 400,
    width: int = 400,
) -> tuple[cairo.ImageSurface, cairo.Context[cairo.ImageSurface], Pango.Layout]:

    surface = cairo.ImageSurface(cairo.Format.RGB24, width, height)
    cairo_context = cairo.Context(surface)

    # color white background
    cairo_context.set_source_rgb(*_TESTUTIL_SOLID_COLOR_WHITE.color.rgb)
    cairo_context.paint()

    layout = PangoCairo.create_layout(cairo_context)
    layout.set_text(text, -1)

    layout.set_height(Pango.units_from_double(height))
    layout.set_width(Pango.units_from_double(width))

    # color black text
    cairo_context.set_source_rgb(*_TESTUTIL_SOLID_COLOR_BLACK.color.rgb)

    font_desc = Pango.FontDescription()  # type: ignore[no-untyped-call]
    font_desc.set_family(family_name)
    font_desc.set_size(Pango.units_from_double(font_size))
    layout.set_font_description(font_desc)

    return surface, cairo_context, layout
