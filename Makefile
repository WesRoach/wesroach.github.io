.PHONY: build serve deploy lint test

build:
	uv run mkdocs build

serve:
	uv run mkdocs serve --livereload

deploy:
	uv run mkdocs gh-deploy

lint: build
	lychee --config .lychee.toml --cache --max-cache-age 1d --no-progress ./site

test:
	uv run pytest
