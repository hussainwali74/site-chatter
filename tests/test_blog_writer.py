import sys
import os
import pytest
from unittest.mock import MagicMock

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.blog_writer import validate_markdown_structure, BlogWriter

def test_valid_markdown():
    markdown_content = "# Title\n## Subtitle 1\n### Subsubtitle\n## Subtitle 2\n### Subsubtitle 2"
    assert validate_markdown_structure(markdown_content) == True

def test_missing_h1():
    markdown_content = "## Subtitle 1\n### Subsubtitle\n## Subtitle 2\n### Subsubtitle 2"
    assert validate_markdown_structure(markdown_content) == False

def test_write_blog_from_titles():
    mock_llm = MagicMock()
    mock_llm.generate_text.return_value = (
        "## Title One\nContent for title one.\n\n"
        "## Title Two\nContent for title two.\n\n"
        "## Title Three\nContent for title three.\n"
    )
    blog_writer = BlogWriter(llm=mock_llm)
    titles = ["Title One", "Title Two", "Title Three"]

    blog_content = blog_writer.write_blog_from_titles(titles)
    expected_content = (
        "## Title One\nContent for title one.\n\n"
        "## Title Two\nContent for title two.\n\n"
        "## Title Three\nContent for title three.\n"
    )
    assert blog_content == expected_content
    mock_llm.generate_text.assert_called_once()