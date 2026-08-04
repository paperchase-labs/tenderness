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

from tenderness.core.geometry import Rectangle
from tenderness.layout_engines.minimal_flexbox.minimal_flexbox import MinimalFlexBox

_CONTENT_RECT: Rectangle = Rectangle(x=0, y=0, width=300, height=100)


@pytest.fixture
def flexbox_engine() -> MinimalFlexBox:
    return MinimalFlexBox()


@pytest.fixture
def content_rect() -> Rectangle:
    return _CONTENT_RECT
