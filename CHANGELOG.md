# Changelog

All notable changes to `tenderness` will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
-

### Changed
-

### Fixed
-

## [0.2.1] - 2026-06-22

### Fixed
- `[text_bounding_box_extractor]` Fix incorrect `byte_index` for the `\n` in `\r\n` line breaks during character bounding-box extraction. Pango visits `\r\n` as two characters but reports the same `byte_index` (the `\r`'s) for both, which caused the `\n` entry's index and text lookup to be wrong. The extractor now detects this stall and offsets `\n` to its correct position.

### Added
- `[docs]` Clarify per-level line-break behavior in the text bounding box docs (`CHAR`, `CLUSTER`, `RUN`, `LINE`, `LAYOUT`), including the `U+2028` (LINE SEPARATOR) exception, which is treated as whitespace rather than excluded.
- `[tests]` Add coverage across all extraction levels for `\r`, `\r\n`, `U+2028`, `U+2029`, tabs, and RTL (Hebrew) text combined with each line-break type.


## [0.2.0] - 2026-06-11

### Added
- Add `tenderness.pipelines.document` pipeline replacing the standard render pipeline, with a more composable API and dedicated helpers for text blocks, table blocks, image blocks, and bounding-box drawing. See the [document pipeline examples](https://paperchase-labs.github.io/tenderness/examples/document-pipeline-examples/).
- Add `to_dict()` on related bounding-box classes.
- Add flexbox layout templates for documents, tables, and flow layouts.
- `[tests]` Add tox configuration for local and CI testing.

### Changed
- Resolution handling for font maps in `FontSetup` and `LayoutContextInterface`.
- Refactored drawing utilities.
- Updated project metadata, classifiers, and docstrings.


### Removed
- Removed `tenderness.pipelines.render` pipeline, which is now replaced by the new `tenderness.pipelines.document` pipeline.



## [0.1.0] - 2026-04-30

### Added
- Initial public release

[Unreleased]: https://github.com/paperchase-labs/tenderness/compare/v0.2.1...HEAD
[0.2.1]: https://github.com/paperchase-labs/tenderness/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/paperchase-labs/tenderness/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/paperchase-labs/tenderness/releases/tag/v0.1.0
