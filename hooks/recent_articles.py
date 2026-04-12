"""MkDocs hook to populate recent articles for sidebar display."""

import os
import yaml
from datetime import date
from mkdocs.structure.files import InclusionLevel

_all_articles = []


def on_env(env, config, files):
    """Add recent_articles and all_articles to Jinja environment."""
    global _all_articles
    docs_dir = config['docs_dir']
    articles = []

    for f in files:
        if not f.src_path.endswith('.md'):
            continue
        if not f.inclusion.is_in_nav():
            continue
        if f.src_path in ('index.md', 'articles.md'):
            continue

        filepath = os.path.join(docs_dir, f.src_path)
        try:
            with open(filepath, 'r') as fp:
                content = fp.read()
            if not content.startswith('---'):
                continue
            end = content.find('---', 3)
            if end == -1:
                continue
            front_matter = yaml.safe_load(content[3:end])
            if not front_matter or 'date' not in front_matter:
                continue
            d = front_matter['date']
            if isinstance(d, str):
                d = date.fromisoformat(d)

            description = front_matter.get('description') or front_matter.get('tagline') or ''

            articles.append({
                'title': front_matter.get('title', f.src_path),
                'url': f.dest_uri,
                'date': d,
                'description': description,
            })
        except Exception:
            continue

    articles.sort(key=lambda x: x['date'], reverse=True)
    _all_articles = articles
    env.globals['recent_articles'] = articles[:5]
    env.globals['all_articles'] = articles
    return env


def on_page_markdown(markdown, page, config, files, **kwargs):
    """Generate the articles index page content."""
    if page.file.src_path != 'articles.md':
        return markdown

    lines = ['# All Articles\n']
    for article in _all_articles:
        lines.append(f"- [{article['title']}]({article['url']}) — {article['date']}")
    return '\n'.join(lines)
