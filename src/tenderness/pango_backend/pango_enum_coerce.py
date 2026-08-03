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

"""Pango enum coercion utilities and string type aliases."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import gi

if TYPE_CHECKING:
    from collections.abc import Mapping

gi.require_version("Pango", "1.0")


from gi.repository import GObject, Pango  # noqa: E402


class PangoEnumCoerce:
    """Utilities for building lowercase string-to-enum maps and coercing values for Pango enums."""

    @staticmethod
    def build_map[T: GObject.GEnum](enum_type: type[T], exclude: frozenset[str] = frozenset()) -> dict[str, T]:
        """Build a lowercase name-to-value map from a Pango enum type, excluding specified members.

        Parameters
        ----------
        enum_type
            Pango enum class to introspect; non-public and non-integer attributes are excluded.
        exclude
            Set of member names to exclude from the map, by default frozenset().

        Returns
        -------
        dict[str, T]
            Mapping of lowercase member name to enum value.
        """
        result = {}
        for member in enum_type:
            nick = member.value_nick.lower()
            if nick not in exclude:
                result[nick] = member
        return result

    @staticmethod
    def coerce[T](mapping: Mapping[str, object], value: T | str) -> T:
        """Coerce a string value to its enum counterpart using a mapping.

        Parameters
        ----------
        mapping
            Lowercase name-to-value map, produced by ``build_map``.
        value
            Value to coerce; returned unchanged if not a string.

        Returns
        -------
        T
            The original value if not a string, or the mapped enum value.

        Raises
        ------
        ValueError
            If ``value`` is a string not present in ``mapping``.
        """
        if not isinstance(value, str):
            return value

        result = mapping.get(value)
        if result is None:
            valid = list(mapping.keys())
            msg = f"Unknown value: {value!r}. Valid: {valid}"
            raise ValueError(msg)

        return result  # type: ignore[return-value]


class PangoEnumMap:
    """Pre-built lowercase string-to-value maps for Pango enums.

    Attributes
    ----------
    WrapMode
        Map for ``Pango.WrapMode``.
    EllipsizeMode
        Map for ``Pango.EllipsizeMode``.
    Alignment
        Map for ``Pango.Alignment``.
    Gravity
        Map for ``Pango.Gravity``.
    Stretch
        Map for ``Pango.Stretch``.
    Style
        Map for ``Pango.Style``.
    Variant
        Map for ``Pango.Variant``.
    Weight
        Map for ``Pango.Weight``.
    FontColor
        Map for ``Pango.FontColor``.
    Direction
        Map for ``Pango.Direction``.
    GravityHint
        Map for ``Pango.GravityHint``.
    TabAlign
        Map for ``Pango.TabAlign``.
    """

    # Pango.Layout
    WrapMode = PangoEnumCoerce.build_map(enum_type=Pango.WrapMode)
    EllipsizeMode = PangoEnumCoerce.build_map(enum_type=Pango.EllipsizeMode)
    Alignment = PangoEnumCoerce.build_map(enum_type=Pango.Alignment)

    # Pango.FontDescription
    Gravity = PangoEnumCoerce.build_map(enum_type=Pango.Gravity)
    Stretch = PangoEnumCoerce.build_map(enum_type=Pango.Stretch)
    Style = PangoEnumCoerce.build_map(enum_type=Pango.Style)
    Variant = PangoEnumCoerce.build_map(enum_type=Pango.Variant)
    Weight = PangoEnumCoerce.build_map(enum_type=Pango.Weight)
    FontColor = PangoEnumCoerce.build_map(enum_type=Pango.FontColor)

    # Pango.Context
    Direction = PangoEnumCoerce.build_map(
        enum_type=Pango.Direction,
        exclude=frozenset({"ttb-ltr", "ttb-rtl"}),
    )
    # Gravity (same as Pango.FontDescription)
    GravityHint = PangoEnumCoerce.build_map(enum_type=Pango.GravityHint)

    # Pango.TabAlign
    TabAlign = PangoEnumCoerce.build_map(enum_type=Pango.TabAlign)


# Pango.Layout
WrapModeStr = Literal["word", "char", "word-char", "none"]
EllipsizeModeStr = Literal["none", "start", "middle", "end"]
AlignmentStr = Literal["left", "center", "right"]

# Pango.FontDescription
GravityStr = Literal["south", "east", "north", "west", "auto"]
StretchStr = Literal[
    "ultra-condensed",
    "extra-condensed",
    "condensed",
    "semi-condensed",
    "normal",
    "semi-expanded",
    "expanded",
    "extra-expanded",
    "ultra-expanded",
]
StyleStr = Literal["normal", "oblique", "italic"]
VariantStr = Literal[
    "normal", "small-caps", "all-small-caps", "petite-caps", "all-petite-caps", "unicase", "title-caps"
]
WeightStr = Literal[
    "thin",
    "ultralight",
    "light",
    "semilight",
    "book",
    "normal",
    "medium",
    "semibold",
    "bold",
    "ultrabold",
    "heavy",
    "ultraheavy",
]
FontColorStr = Literal["forbidden", "required", "dont-care"]

# Pango.Context
DirectionStr = Literal["ltr", "rtl", "weak-ltr", "weak-rtl", "neutral"]
GravityHintStr = Literal["natural", "strong", "line"]

# Pango.TabAlign
TabAlignStr = Literal["left", "right", "center", "decimal"]
