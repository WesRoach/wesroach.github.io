# wesroach.github.io

[wesroach.dev](https://www.wesroach.dev)

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [make](https://gnuwin32.sourceforge.net/packages/make.htm) — `winget install ezwinports.make`
- [lychee](https://lychee.cli.rs/) — `winget install lycheeverse.lychee` (required for `make lint`)

## Setup

```bash
uv sync
```

## Common tasks

| Command | Description |
|---------|-------------|
| `make serve` | Start local dev server with live reload |
| `make build` | Build static site to `./site` |
| `make lint` | Build then check for broken links |
| `make test` | Run test suite |
| `make deploy` | Build and deploy to GitHub Pages |
