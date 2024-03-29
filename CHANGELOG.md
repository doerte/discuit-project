# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).




## [Unreleased]

## [0.4.1] - 2023-09-20

### Changed
- fixed some errors in the readme

## [0.4.0] - 2023-08-05

### Changed
- used dataclass for generating the output
- dataclass is used to write from commandline but also accessible from outside

## [0.3.0] - 2023-08-01

### Changed
- splitted script into different modules.
- made functions accessible when importing the package.
### Fixed
- fixed a bug that occurred when no 'absolute' variable was determined.


## [0.2.1] - 2023-04-18

### Fixed
- removed faulty check for silhouette score

## [0.2.0] - 2023-04-18
### Added
- provided example file
- handling missing data in input
- statistics for "absolute" variable are calculated

### Changed
- Yates correction for Chi^2 only if expected values < 5

### Fixed
- Corrected instructions in Readme.md

## [0.1.0] - 2023-02-23

### Added
First release as alfa-version



[Unreleased]: https://github.com/doerte/discuit-project/compare/v0.4.1...main
[0.4.0]: https://github.com/doerte/discuit-project/compare/v0.4.0...v0.4.1
[0.4.0]: https://github.com/doerte/discuit-project/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/doerte/discuit-project/compare/v0.2.1...v0.3.0
[0.2.1]: https://github.com/doerte/discuit-project/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/doerte/discuit-project/compare/v0.1.0-alpha...v0.2.0
[0.1.0]: https://github.com/doerte/discuit-project/releases/tag/v0.1.0-alpha

