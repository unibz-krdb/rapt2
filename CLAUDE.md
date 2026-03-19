# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

RAPTv2 — Relational Algebra Parsing Tools. Parses relational algebra expressions and transforms them into SQL, LaTeX QTree, and parse tree representations. Python 3.13+, built with `uv`.

Fork of [pyrapt/rapt](https://github.com/pyrapt/rapt).

## Commands

```bash
uv sync --all-groups    # Install all dependencies (including dev)
pytest                  # Run all tests
pytest tests/treebrd/   # Run a test subdirectory
pytest tests/treebrd/test_node.py -k test_name  # Run a single test
ruff check .            # Lint
ruff format .           # Format
```

## Architecture

Three-layer pipeline: **Grammar/Parser → AST → Translators**

### Layer 1: Grammar & Parsing (`src/rapt2/treebrd/grammars/`)
- Syntax hierarchy: `BaseSyntax` → `ConditionSyntax` → `CoreSyntax` → `ExtendedSyntax` → `DependencySyntax` (alias: `Syntax`) — configurable operator symbols and tokens
- Grammar hierarchy: `ProtoGrammar` → `ConditionGrammar` → `CoreGrammar` → `ExtendedGrammar` → `DependencyGrammar`
- Each grammar level adds operators (conditions → core RA → joins/set ops → dependency constraints)
- Uses `pyparsing` to produce `ParseResults`

### Layer 2: AST (`src/rapt2/treebrd/`)
- `TreeBRD` — factory that builds syntax trees from parse results
- Node hierarchy: `Node` → `RelationNode`, `UnaryNode` (Select, Project, Rename, Assign), `BinaryNode` (joins, set ops), `DependencyNode` → `UnaryDependencyNode` (PK, MVD, FD), `BinaryDependencyNode` (InclusionEquivalence, InclusionSubsumption)
- `Schema` — manages relation definitions; passed through parsing for attribute validation
- `AttributeList` — tracks attributes with relation prefixes for disambiguation
- `ConditionNode` — represents WHERE-style conditions

### Layer 3: Translators (`src/rapt2/transformers/`)
- `BaseTranslator` — visitor-pattern base class
- `SQLTranslator` — RA to SQL (supports set/bag semantics)
- `QTreeTranslator` — RA to LaTeX QTree format

### Public API (`src/rapt2/rapt.py`)
`Rapt` class is the entry point. Methods: `to_syntax_tree()`, `to_sql()`, `to_sql_sequence()`, `to_qtree()`. Accepts optional grammar/syntax config (see `config/default.json`).

## Testing

Tests use `unittest.TestCase`. Test files mirror source structure under `tests/`. Common pattern: `setUpClass` creates a shared `Schema` and `TreeBRD` builder, then tests parse expressions and assert on the resulting node trees or translated output.

## Gotchas

- **SQL translator tests need PostgreSQL** — `tests/transformers/sql_translator/test_translator.py` requires a running PostgreSQL instance (`setup_db.sql`/`teardown_db.sql`). CI skips this file via `--ignore`.
- **`psycopg2-binary` dependency** — requires PostgreSQL client libraries on the host.
- **Broken CLI entry point** — `pyproject.toml` defines `rapt = "rapt2.rapt:main"` but `main()` does not exist in `rapt.py`.
