import os
import tempfile
from unittest.mock import MagicMock

import jinja2
import pytest
from mkdocs.structure.files import InclusionLevel

from hooks.recent_articles import on_env


def _make_file(src_path, inclusion):
    f = MagicMock()
    f.src_path = src_path
    f.inclusion = inclusion
    f.dest_uri = src_path.replace('.md', '.html')
    return f


def _write_article(docs_dir, filename, date="2025-01-01", title="Test"):
    path = os.path.join(docs_dir, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as fp:
        fp.write(f"---\ndate: {date}\ntitle: {title}\n---\n# {title}\n")


def _run_hook(docs_dir, files):
    config = {"docs_dir": docs_dir}
    env = jinja2.Environment()
    return on_env(env, config, files)


def test_nav_article_appears_in_recent():
    with tempfile.TemporaryDirectory() as docs_dir:
        _write_article(docs_dir, "article.md", date="2025-01-01", title="My Article")
        files = [_make_file("article.md", InclusionLevel.INCLUDED)]
        env = _run_hook(docs_dir, files)
        assert any(a["title"] == "My Article" for a in env.globals["all_articles"])


def test_excluded_article_does_not_appear():
    with tempfile.TemporaryDirectory() as docs_dir:
        _write_article(docs_dir, "old.md", date="2025-06-01", title="Old Article")
        files = [_make_file("old.md", InclusionLevel.EXCLUDED)]
        env = _run_hook(docs_dir, files)
        assert env.globals["all_articles"] == []


def test_not_in_nav_article_does_not_appear():
    with tempfile.TemporaryDirectory() as docs_dir:
        _write_article(docs_dir, "draft.md", date="2025-03-01", title="Draft Article")
        files = [_make_file("draft.md", InclusionLevel.NOT_IN_NAV)]
        env = _run_hook(docs_dir, files)
        assert env.globals["all_articles"] == []


def test_only_nav_articles_appear_among_mixed_files():
    with tempfile.TemporaryDirectory() as docs_dir:
        _write_article(docs_dir, "published.md", date="2025-05-01", title="Published")
        _write_article(docs_dir, "old.md", date="2019-01-01", title="Old")
        _write_article(docs_dir, "draft.md", date="2025-06-01", title="Draft")
        files = [
            _make_file("published.md", InclusionLevel.INCLUDED),
            _make_file("old.md", InclusionLevel.EXCLUDED),
            _make_file("draft.md", InclusionLevel.NOT_IN_NAV),
        ]
        env = _run_hook(docs_dir, files)
        titles = [a["title"] for a in env.globals["all_articles"]]
        assert titles == ["Published"]


def test_index_md_excluded_regardless_of_inclusion():
    with tempfile.TemporaryDirectory() as docs_dir:
        _write_article(docs_dir, "index.md", date="2025-01-01", title="Home")
        files = [_make_file("index.md", InclusionLevel.INCLUDED)]
        env = _run_hook(docs_dir, files)
        assert env.globals["all_articles"] == []


def test_url_uses_dest_uri():
    with tempfile.TemporaryDirectory() as docs_dir:
        _write_article(docs_dir, "workstation/shell-setup/index.md", date="2025-01-01", title="Shell Setup")
        files = [_make_file("workstation/shell-setup/index.md", InclusionLevel.INCLUDED)]
        env = _run_hook(docs_dir, files)
        assert env.globals["all_articles"][0]["url"] == "workstation/shell-setup/index.html"


def test_recent_articles_capped_at_five():
    with tempfile.TemporaryDirectory() as docs_dir:
        files = []
        for i in range(7):
            name = f"article{i}.md"
            _write_article(docs_dir, name, date=f"2025-0{i+1}-01", title=f"Article {i}")
            files.append(_make_file(name, InclusionLevel.INCLUDED))
        env = _run_hook(docs_dir, files)
        assert len(env.globals["recent_articles"]) == 5
        assert len(env.globals["all_articles"]) == 7
