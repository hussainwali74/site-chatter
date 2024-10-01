import logging
from typing import List
from datetime import datetime

def generate_meta_description(blog_content: str, focus_keyphrase: str, llm_instance) -> str:
    """
    Generates an SEO-friendly meta description using the focus keyphrase.
    """
    try:
        prompt = (
            "Create a concise SEO meta description for the following blog content. "
            f"Include the focus keyphrase '{focus_keyphrase}' in the description.\n\n"
            f"{blog_content}"
        )
        meta_description = llm_instance.generate_text(prompt).strip()
        logger.info(f"Generated meta description: {meta_description}")
        return meta_description
    except Exception as e:
        logger.error(f"Error generating meta description: {e}")
        return ""

def add_meta_description(markdown_content: str, meta_description: str) -> str:
    """
    Inserts the meta description into the markdown content.
    """
    try:
        lines = markdown_content.split('\n')
        # Insert meta description after the first line (assumed to be the title)
        if lines:
            lines.insert(1, f"SEO Meta Description: {meta_description}\n")
        return '\n'.join(lines)
    except Exception as e:
        logger.error(f"Error adding meta description: {e}")
        return markdown_content