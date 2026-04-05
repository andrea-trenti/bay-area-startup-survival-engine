# Data Layer

This repository separates public analytical work from institution-owned source data. The `data/` directory is therefore a non-versioned acquisition and transformation workspace rather than a redistribution channel.

## Structure

- `raw/` — externally acquired source files downloaded from official public institutions. These files are not tracked in Git.
- `processed/` — rebuildable intermediate outputs generated from the source-acquisition layer. These files are also excluded from Git.

## Rule

Do not upload raw statistical files to the public repository unless the issuing institution explicitly authorizes redistribution under the intended terms of use. Users remain responsible for checking institutional release notes, licensing language, and redistribution conditions.
