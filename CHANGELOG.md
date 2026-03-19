# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.5.1] - 2026-03-19

### Changed
- Updated architecture documentation and added gotchas section to CLAUDE.md
- Added claude-squad local data to gitignore
- CI now skips SQL translator tests that require PostgreSQL

## [0.5.0] - 2026-03-05

### Added
- Type annotations across the node class hierarchy and foundation layer
- `py.typed` marker for PEP 561 downstream type-checking support
- Comprehensive test coverage for dependency nodes, grammars, public API, operator sets, and utility functions
- `ConditionalJoinNode` base class for theta/outer join nodes
- Centralized `JOIN_OPERATORS` and `CONDITIONAL_JOIN_OPERATORS` frozensets
- CLAUDE.md project instructions

### Changed
- Consolidated `BinaryDependencyNode` hierarchy — `InclusionEquivalenceNode` and `InclusionSubsumptionNode` now inherit shared init and equality logic
- Moved `translate_condition` into `BaseTranslator` and consolidated QTree dependency methods
- Extracted inclusion node helper and dict-dispatch for MVD/FD in tree builder
- Moved schema mutation from `AssignNode` to `TreeBRD.build()` factory
- Renamed abbreviated identifiers in dependency grammar for clarity (`inc_eq` -> `inc_equiv`, `inc_subs` -> `inc_subset`)
- Renamed `param` to `operator_params` in tree builder for clarity
- Replaced `assert isinstance` with `TypeError` in `AttributeList.merge`
- Standardized pyparsing imports to use top-level `infixNotation`
- Improved dispatch comments and documentation in tree builder
- Replaced mutable default arguments and narrowed exception handling

### Fixed
- Added missing `__init__.py` to core_grammar test package
- Descriptive error messages replacing bare exceptions and cryptic abbreviations
