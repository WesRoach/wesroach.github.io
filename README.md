# wesroach.github.io

[wesroach.dev](https://www.wesroach.dev)

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [just](https://just.systems) — `winget install Casey.Just`
- [lychee](https://lychee.cli.rs/) — `winget install lycheeverse.lychee` (required for `make lint`)

## Setup

```bash
uv sync
```

## Common tasks

| Command | Description |
|---------|-------------|
| `just serve` | Start local dev server with live reload |
| `just build` | Build static site to `./site` |
| `just lint` | Build then check for broken links |
| `just test` | Run test suite |
| `just deploy` | Build and deploy to GitHub Pages |
