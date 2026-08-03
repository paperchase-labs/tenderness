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

"""Font description interface."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, ClassVar, Self

import gi

from tenderness.core.base_interface import BaseInterface, BaseInterfaceParameters
from tenderness.core.sentinel import _UNSET_PARAM, Settable, SettableOrNone
from tenderness.pango_backend.pango_enum_coerce import (
    FontColorStr,
    GravityStr,
    PangoEnumCoerce,
    PangoEnumMap,
    StretchStr,
    StyleStr,
    VariantStr,
    WeightStr,
)

gi.require_version("Pango", "1.0")


from gi.repository import Pango  # noqa: E402

if TYPE_CHECKING:
    from tenderness.pango_backend.layout_interface import LayoutInterface


@dataclass(slots=True, frozen=True)
class FontDescriptionInterfaceParameters(BaseInterfaceParameters):
    """Configuration parameters for FontDescriptionInterface.

    Attributes
    ----------
    family
        Font family name.
    features
        OpenType feature string; ``None`` clears the setting.
    gravity
        Glyph gravity.
    stretch
        Font stretch width.
    style
        Font style.
    variant
        Font variant.
    variations
        OpenType variations string; ``None`` clears the setting.
    weight
        Font weight.
    size_device_units
        Font size in device units; mutually exclusive with ``size``.
    size
        Font size in points; mutually exclusive with ``size_device_units``.
    color
        Font color.
    """

    _COERCE_DISPATCH: ClassVar[dict[str, Any]] = {
        "gravity": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Gravity, v),
        "stretch": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Stretch, v),
        "style": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Style, v),
        "variant": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Variant, v),
        "weight": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.Weight, v),
        "color": lambda v: PangoEnumCoerce.coerce(PangoEnumMap.FontColor, v),
    }

    _CONFLICTING_PAIRS: ClassVar[tuple[tuple[str, str], ...]] = (("size", "size_device_units"),)

    family: Settable[str] = field(default=_UNSET_PARAM)
    features: SettableOrNone[str] = field(default=_UNSET_PARAM)
    gravity: Settable[Pango.Gravity | GravityStr] = field(default=_UNSET_PARAM)
    stretch: Settable[Pango.Stretch | StretchStr] = field(default=_UNSET_PARAM)
    style: Settable[Pango.Style | StyleStr] = field(default=_UNSET_PARAM)
    variant: Settable[Pango.Variant | VariantStr] = field(default=_UNSET_PARAM)
    variations: SettableOrNone[str] = field(default=_UNSET_PARAM)
    weight: Settable[Pango.Weight | WeightStr] = field(default=_UNSET_PARAM)

    size_device_units: Settable[float] = field(default=_UNSET_PARAM)
    size: Settable[float] = field(default=_UNSET_PARAM)

    color: Settable[Pango.FontColor | FontColorStr] = field(default=_UNSET_PARAM)

    def _validate(self, proposed: dict[str, Any]) -> None:
        for pango_field, device_field in self._CONFLICTING_PAIRS:
            if pango_field in proposed and device_field in proposed:
                msg = f"Cannot set both '{pango_field}' (Pango units) and '{device_field}' (device units) at the same time."
                raise ValueError(msg)

    def __post_init__(self) -> None:
        """Coerce values and validate parameters after initialization."""
        BaseInterfaceParameters.__post_init__(self)


class FontDescriptionInterface(BaseInterface):
    """Interface for font description.

    Attributes
    ----------
    PANGO_SCALE
        Scale between Pango distances and device units (``Pango.SCALE``, currently 1024).

    Notes
    -----
    See https://docs.gtk.org/Pango/struct.FontDescription.html

    1. Create with ``from_new()`` or ``from_string()``.
    2. Update with ``update_with_parameters()`` or through properties.
    3. Apply with ``apply_to_layout()`` or ``apply_to_layout_interface()``.
    """

    PANGO_SCALE: int = Pango.SCALE

    def __init__(self, font_description: Pango.FontDescription, name: str = "") -> None:
        """Initialize the font description interface.

        Parameters
        ----------
        font_description
            Underlying Pango font description object.
        name
            Optional label for the interface instance.
        """
        super().__init__(name=name)
        self.font_description = font_description

    @classmethod
    def from_new(cls, name: str = "") -> Self:
        """Create a new font description with all fields unset.

        Parameters
        ----------
        name
            Optional label for the interface instance.

        Returns
        -------
        Self
            ``FontDescriptionInterface`` backed by a new empty font description.
        """
        return cls(font_description=Pango.FontDescription(), name=name)  # type: ignore[no-untyped-call]

    @classmethod
    def from_string(cls, font_desc_str: str, name: str = "") -> Self:
        """Create from a Pango font-description string.

        Parameters
        ----------
        font_desc_str
            Pango font description string to parse.
        name
            Optional label for the interface instance.

        Returns
        -------
        Self
            ``FontDescriptionInterface`` backed by the parsed font description.

        Notes
        -----
        See https://docs.gtk.org/Pango/type_func.FontDescription.from_string.html
        """
        return cls(font_description=Pango.FontDescription.from_string(font_desc_str), name=name)

    def apply_to_layout(self, layout: Pango.Layout) -> None:
        """Apply this font description to a Pango layout.

        Parameters
        ----------
        layout
            Pango layout to apply the font description to.
        """
        layout.set_font_description(self.font_description)

    def apply_to_layout_interface(self, layout_interface: LayoutInterface) -> None:
        """Apply this font description to a layout interface.

        Parameters
        ----------
        layout_interface
            Layout interface to apply the font description to.
        """
        layout_interface.font_description = self.font_description

    # ------------------------------------------------------------------
    # Properties with getters and setters
    # ------------------------------------------------------------------
    @property
    def color(self) -> Pango.FontColor:
        """Font color.

        Returns
        -------
        Pango.FontColor
            Current font color.

        Notes
        -----
        Controls matching against fonts with or without color glyphs.
        """
        return self.font_description.get_color()

    @color.setter
    def color(self, color: Pango.FontColor) -> None:
        """Set the font color.

        Parameters
        ----------
        color
            Color to apply.
        """
        self.font_description.set_color(color)

    @property
    def family(self) -> str | None:
        """Font family name.

        Returns
        -------
        str | None
            Current font family name, or ``None`` if not set.
        """
        return self.font_description.get_family()

    @family.setter
    def family(self, family: str) -> None:
        """Set the font family name.

        Parameters
        ----------
        family
            Font family name to apply.

        Notes
        -----
        Accepts a comma-separated list of family names.
        """
        self.font_description.set_family(family)

    @property
    def features(self) -> str | None:
        """OpenType feature string.

        Returns
        -------
        str | None
            Current OpenType feature string, or ``None`` if not set.
        """
        return self.font_description.get_features()

    @features.setter
    def features(self, features: str | None) -> None:
        """Set the OpenType feature string.

        Parameters
        ----------
        features
            Feature string to apply, or ``None`` to clear.

        Notes
        -----
        Format is ``FEATURE=n,...`` where each feature is a 4-character OpenType tag. The
        intended use case is character variations (cv01-cv99) and style sets (ss01-ss20); features
        apply to the entire text using this font description. Unknown features are ignored.
        """
        self.font_description.set_features(features)

    @property
    def gravity(self) -> Pango.Gravity:
        """Glyph gravity.

        Returns
        -------
        Pango.Gravity
            Current glyph gravity.
        """
        return self.font_description.get_gravity()

    @gravity.setter
    def gravity(self, gravity: Pango.Gravity) -> None:
        """Set the glyph gravity.

        Parameters
        ----------
        gravity
            Gravity to apply.

        Notes
        -----
        ``AUTO`` unsets the gravity mask. Gravity should normally be set on the context,
        not on the font description.
        """
        self.font_description.set_gravity(gravity)

    @property
    def stretch(self) -> Pango.Stretch:
        """Font stretch width.

        Returns
        -------
        Pango.Stretch
            Current font stretch width.
        """
        return self.font_description.get_stretch()

    @stretch.setter
    def stretch(self, stretch: Pango.Stretch) -> None:
        """Set the font stretch width.

        Parameters
        ----------
        stretch
            Stretch value to apply.
        """
        self.font_description.set_stretch(stretch)

    @property
    def style(self) -> Pango.Style:
        """Font style.

        Returns
        -------
        Pango.Style
            Current font style.
        """
        return self.font_description.get_style()

    @style.setter
    def style(self, style: Pango.Style) -> None:
        """Set the font style.

        Parameters
        ----------
        style
            Style to apply.

        Notes
        -----
        Italic and oblique are treated as approximate matches when no exact match is found.
        """
        self.font_description.set_style(style)

    @property
    def variant(self) -> Pango.Variant:
        """Font variant (normal or small caps).

        Returns
        -------
        Pango.Variant
            Current font variant.
        """
        return self.font_description.get_variant()

    @variant.setter
    def variant(self, variant: Pango.Variant) -> None:
        """Set the font variant.

        Parameters
        ----------
        variant
            Variant to apply.
        """
        self.font_description.set_variant(variant)

    @property
    def variations(self) -> str | None:
        """OpenType variations string.

        Returns
        -------
        str | None
            Current OpenType variations string, or ``None`` if not set.
        """
        return self.font_description.get_variations()

    @variations.setter
    def variations(self, variations: str | None) -> None:
        """Set the OpenType variations string.

        Parameters
        ----------
        variations
            Variations string to apply, or ``None`` to clear.

        Notes
        -----
        Format is ``AXIS1=VALUE,AXIS2=VALUE...`` where each axis is a 4-character OpenType tag.
        Unknown axes are ignored and values are clamped to their allowed range.
        """
        self.font_description.set_variations(variations)

    @property
    def weight(self) -> Pango.Weight:
        """Font weight.

        Returns
        -------
        Pango.Weight
            Current font weight.
        """
        return self.font_description.get_weight()

    @weight.setter
    def weight(self, weight: Pango.Weight) -> None:
        """Set the font weight.

        Parameters
        ----------
        weight
            Weight to apply.
        """
        self.font_description.set_weight(weight)

    # ------------------------------------------------------------------
    # Properties with only getters
    # ------------------------------------------------------------------
    @property
    def size_is_absolute(self) -> bool:
        """True when the font size was set as an absolute device-unit value.

        Returns
        -------
        bool
            ``True`` if the size is absolute (device units), ``False`` if in Pango units.
        """
        return self.font_description.get_size_is_absolute()

    @property
    def hash(self) -> int:
        """Hash value for the font description.

        Returns
        -------
        int
            Hash value of the font description.

        Notes
        -----
        The hash value is independent of the field mask.
        """
        return self.font_description.hash()

    @property
    def to_filename(self) -> str | None:
        """Font description as a filename-compatible string.

        Returns
        -------
        str | None
            Filename-compatible representation, or ``None`` if not representable.
        """
        return self.font_description.to_filename()

    @property
    def to_string(self) -> str:
        """Font description as a Pango string representation.

        Returns
        -------
        str
            Pango string representation of the font description.
        """
        return self.font_description.to_string()

    # ------------------------------------------------------------------
    # Methods
    # ------------------------------------------------------------------
    def better_match(self, old_match: Pango.FontDescription | None, new_match: Pango.FontDescription) -> bool:
        """Return True if new_match is a closer match to this description than old_match.

        Parameters
        ----------
        old_match
            Previous best match, or ``None`` if there is no prior match.
        new_match
            Candidate font description to compare.

        Returns
        -------
        bool
            ``True`` if ``new_match`` is a better match than ``old_match``.

        Notes
        -----
        Weight and style are matched approximately; all other attributes must match exactly.
        Oblique and italic are considered equivalent but not as good a match as identical styles.
        ``old_match`` must itself match this description.
        """
        return self.font_description.better_match(old_match, new_match)

    def copy(self) -> Pango.FontDescription | None:
        """Return a copy of the underlying Pango.FontDescription.

        Returns
        -------
        Pango.FontDescription | None
            Copy of the font description.
        """
        return self.font_description.copy()

    def copy_static(self) -> Pango.FontDescription | None:
        """Return a shallow copy of the font description.

        Returns
        -------
        Pango.FontDescription | None
            Shallow copy of the font description.
        """
        return self.font_description.copy_static()

    def equal(self, desc2: Pango.FontDescription) -> bool:
        """Return True if desc2 has the same attributes as this description.

        Parameters
        ----------
        desc2
            Font description to compare against.

        Returns
        -------
        bool
            ``True`` if both descriptions are equal.

        Notes
        -----
        Masks do not need to match; only the values of set fields are compared.
        """
        return self.font_description.equal(desc2)

    def free(self) -> None:
        """Release the underlying Pango.FontDescription.

        Notes
        -----
        Rarely needed in Python; GObject reference counting handles cleanup automatically.
        """
        self.font_description.free()

    def get_set_fields(self) -> Pango.FontMask:
        """Return a bitmask of the fields that have been explicitly set.

        Returns
        -------
        Pango.FontMask
            Bitmask of explicitly set fields.
        """
        return self.font_description.get_set_fields()

    def merge(self, desc_to_merge: Pango.FontDescription | None, *, replace_existing: bool) -> None:
        """Merge desc_to_merge into this description.

        Parameters
        ----------
        desc_to_merge
            Description to merge in; ``None`` is a no-op.
        replace_existing
            When ``True``, fields already set in this description are overwritten.
        """
        self.font_description.merge(desc_to_merge, replace_existing)

    def merge_static(self, desc_to_merge: Pango.FontDescription, *, replace_existing: bool) -> None:
        """Merge desc_to_merge into this description without deep-copying string fields.

        Parameters
        ----------
        desc_to_merge
            Description to merge in.
        replace_existing
            When ``True``, fields already set in this description are overwritten.
        """
        self.font_description.merge_static(desc_to_merge, replace_existing)

    def set_family_static(self, family: str) -> None:
        """Set the font family name via the static C variant.

        Parameters
        ----------
        family
            Font family name to apply.
        """
        self.font_description.set_family_static(family)

    def set_features_static(self, features: str) -> None:
        """Set the OpenType feature string via the static C variant.

        Parameters
        ----------
        features
            OpenType feature string to apply.
        """
        self.font_description.set_features_static(features)

    def set_variations_static(self, variations: str) -> None:
        """Set the OpenType variations string via the static C variant.

        Parameters
        ----------
        variations
            OpenType variations string to apply.
        """
        self.font_description.set_variations_static(variations)

    def unset_fields(self, fields: Pango.FontMask) -> None:
        """Unset the specified fields, reverting them to their default values.

        Parameters
        ----------
        fields
            Bitmask of fields to unset.
        """
        self.font_description.unset_fields(fields)

    # ------------------------------------------------------------------
    # Size
    # ------------------------------------------------------------------
    @property
    def size(self) -> float | None:
        """Font size in points; ``None`` when an absolute device size is set.

        Returns
        -------
        float | None
            Font size in points, or ``None`` if an absolute device size is active.
        """
        if self.size_is_absolute:
            return None
        return Pango.units_to_double(self.font_description.get_size())

    @size.setter
    def size(self, size: int) -> None:
        """Set the font size in points.

        Parameters
        ----------
        size
            Font size in points.
        """
        self.font_description.set_size(Pango.units_from_double(size))

    @property
    def size_device_units(self) -> float | None:
        """Font size in device units; ``None`` when a Pango-unit size is set.

        Returns
        -------
        float | None
            Font size in device units, or ``None`` if a Pango-unit size is active.
        """
        if not self.size_is_absolute:
            return None
        return Pango.units_to_double(self.font_description.get_size())

    @size_device_units.setter
    def size_device_units(self, size: float) -> None:
        """Set the font size in device units.

        Parameters
        ----------
        size
            Font size in device units.
        """
        self.font_description.set_absolute_size(Pango.units_from_double(size))
