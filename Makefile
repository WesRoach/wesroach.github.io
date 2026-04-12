# MSYSTEM is set by Git Bash (MINGW64/MINGW32/MSYS); use 8.3 short path to
# avoid the space in "C:/Program Files" which breaks Windows CreateProcess.
ifdef MSYSTEM
    SHELL := C:/PROGRA~1/Git/bin/bash.exe
else
    SHELL := /bin/bash
endif

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
