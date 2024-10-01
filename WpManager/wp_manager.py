import re
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime

import markdown
from bs4 import BeautifulSoup
from bing_image_downloader import downloader

from WpManager.post_manager import media_creator, media_details_adder, post_creator
from AI.llm import LLM
from SocialMediaManager.social_media_manager import SocialMediaManager

# Configure logging with detailed format and multiple handlers
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG to capture all levels of logs

# Create formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Console handler for INFO and above
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# File handler for DEBUG and above
file_handler = logging.FileHandler('wp_manager.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Constants
BLOG_DIR = 'Blogs'
MAX_TOPICS = 3
ILLEGAL_CHARS_PATTERN = r'[,.:"/\\|?*]'

# Initialize LLM
llm = LLM()

def get_blog_files(directory: str) -> List[str]:
    """
    Retrieve all markdown files from the specified directory.
    """
    try:
        files = [f for f in os.listdir(directory) if f.endswith('.md')]
        logger.info(f"Found blog files: {files}")
        return files
    except FileNotFoundError:
        logger.error(f"Directory '{directory}' not found.")
        return []
    except Exception as e:
        logger.error(f"Error accessing directory '{directory}': {e}")
        return []

def parse_markdown(file_path: str) -> Optional[BeautifulSoup]:
    """
    Convert markdown content to HTML and parse it with BeautifulSoup.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            md = markdown.Markdown()
            html_content = md.convert(f.read())
            soup = BeautifulSoup(html_content, 'html.parser')
            logger.debug(f"Parsed HTML for '{file_path}'.")
            return soup
    except Exception as e:
        logger.error(f"Failed to parse markdown file '{file_path}': {e}")
        return None

def extract_title(soup: BeautifulSoup) -> str:
    """
    Extract and sanitize the title from the HTML soup.
    """
    try:
        title = soup.h1.text.strip() if soup.h1 else 'No Title'
        sanitized_title = re.sub(ILLEGAL_CHARS_PATTERN, '', title)
        logger.info(f"Extracted title: '{sanitized_title}'.")
        return sanitized_title
    except Exception as e:
        logger.error(f"Error extracting title: {e}")
        return 'No Title'

def extract_topics(soup: BeautifulSoup) -> List[str]:
    """
    Extract and sanitize topics from h2 tags, excluding non-relevant sections.
    """
    try:
        topics = [h2.text.strip().lower() for h2 in soup.find_all('h2')]
        non_topics = {'seo meta description:', 'conclusion', 'faqs'}
        cleaned_topics = [
            re.sub(ILLEGAL_CHARS_PATTERN, '', topic)
            for topic in topics
            if topic not in non_topics and 'conclusion' not in topic
        ]
        limited_topics = cleaned_topics[:MAX_TOPICS]
        logger.info(f"Extracted topics: {limited_topics}.")
        return limited_topics
    except Exception as e:
        logger.error(f"Error extracting topics: {e}")
        return []

def generate_and_download_images(title: str, topics: List[str]) -> Dict[str, str]:
    """
    Generate search queries using LLM and download corresponding images.
    """
    query_topic_dict = {}
    for topic in topics:
        try:
            logger.info(f"Generating image for topic: '{topic}'.")
            query = f"{title} {topic}"
            prompt = (
                "Shorten this search query, it will be used to fetch relevant image from internet. "
                "Do not add any other explanation or information as it will cause error. "
                "Your response should be only shorter search query. The shortened version should "
                "capture the WHOLE essence of the original search query. Here is the search query: "
                f"{query}"
            )
            shortened_query = llm.instruct_generate(prompt)
            sanitized_query = re.sub(ILLEGAL_CHARS_PATTERN, '', shortened_query)
            query_topic_dict[topic] = sanitized_query
            outdir = os.path.join('Blogs', 'blog_images', title)
            downloader.download(sanitized_query, limit=1, output_dir=outdir, adult_filter_off=True)
            logger.info(f"Downloaded image for query '{sanitized_query}' to '{outdir}'.")
        except Exception as e:
            logger.error(f"Failed to generate/download image for topic '{topic}': {e}")
    return query_topic_dict

def insert_images_into_content(soup: BeautifulSoup, query_topic_dict: Dict[str, str], title: str) -> None:
    """
    Insert downloaded images into the HTML content after their respective h2 tags.
    """
    try:
        for h2 in soup.find_all('h2'):
            original_topic = h2.text.strip()
            sanitized_topic = re.sub(ILLEGAL_CHARS_PATTERN, '', original_topic.lower())
            query = query_topic_dict.get(sanitized_topic)
            if not query:
                continue
            image_dir = os.path.join('Blogs', 'blog_images', title, query)
            if not os.path.exists(image_dir):
                logger.warning(f"Image directory '{image_dir}' does not exist for topic '{original_topic}'.")
                continue
            image_files = os.listdir(image_dir)
            if not image_files:
                logger.warning(f"No images found in '{image_dir}' for topic '{original_topic}'.")
                continue
            image_path = os.path.join(image_dir, image_files[0])
            media_detail = media_creator(image_path)
            if media_detail:
                media_id = media_detail.get('media_id')
                media_url = media_detail.get('media_url')
                media_details_adder(media_id, original_topic, caption=original_topic, description=title)
                img_tag = soup.new_tag("img", src=media_url)
                h2.insert_after(img_tag)
                logger.info(f"Inserted image for topic '{original_topic}' at '{media_url}'.")
    except Exception as e:
        logger.error(f"Error inserting images into content: {e}")

def validate_markdown_structure(markdown_content: str) -> bool:
    """
    Validates that the markdown content contains at least one h1, multiple h2, and h3 headers.
    """
    try:
        html = markdown.markdown(markdown_content)
        soup = BeautifulSoup(html, 'html.parser')

        h1 = soup.find_all('h1')
        h2 = soup.find_all('h2')
        h3 = soup.find_all('h3')

        if len(h1) < 1:
            logger.error("Validation Failed: Less than one H1 header found.")
            return False
        if len(h2) < 2:
            logger.error("Validation Failed: Less than two H2 headers found.")
            return False
        if len(h3) < 1:
            logger.error("Validation Failed: Less than one H3 header found.")
            return False

        logger.info("Markdown structure validation passed.")
        return True
    except Exception as e:
        logger.error(f"Error during markdown validation: {e}")
        return False

def add_seo_metadata(markdown_content: str, keywords: List[str]) -> str:
    """
    Adds SEO metadata to the markdown content.
    """
    try:
        metadata = f"---\nkeywords: {', '.join(keywords)}\ndate: {datetime.now().isoformat()}\n---\n\n"
        return metadata + markdown_content
    except Exception as e:
        logger.error(f"Error adding SEO metadata: {e}")
        return markdown_content

def publish_blog(file_path: str, hours: int, social_media_manager: SocialMediaManager) -> int:
    """
    Process and publish a single blog post, then create corresponding social media posts.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        if not validate_markdown_structure(markdown_content):
            logger.warning(f"Skipping blog '{file_path}' due to invalid markdown structure.")
            return hours

        soup = parse_markdown(file_path)
        title = extract_title(soup)
        topics = extract_topics(soup)
        query_topic_dict = generate_and_download_images(title, topics)
        insert_images_into_content(soup, query_topic_dict, title)

        post_creator(title, content=str(soup), postStatus='future', hours=hours)
        logger.info(f"Scheduled post '{title}' to be published in {hours} hours.")

        # Create and post tweet
        blog_url = f"http://localhost:8000/blog/{title.replace(' ', '-').lower()}"
        tweet = social_media_manager.create_tweet(title, blog_url)
        social_media_manager.post_tweet(tweet)

        # Create and post Instagram
        summary = "Your blog summary here."  # Extract or generate summary
        caption = social_media_manager.create_instagram_caption(title, summary)
        image_path = "path_to_featured_image.jpg"  # Define how to select image
        social_media_manager.post_instagram(image_path, caption)

        return hours + 4
    except Exception as e:
        logger.error(f"Failed to publish blog '{file_path}': {e}")
        return hours

def publish_all_blogs() -> None:
    """
    Publish all blogs found in the BLOG_DIR.
    """
    try:
        blog_files = get_blog_files(BLOG_DIR)
        if not blog_files:
            logger.warning(f"No markdown files found in '{BLOG_DIR}'.")
            return

        hours = 0
        for blog_file in blog_files:
            file_path = os.path.join(BLOG_DIR, blog_file)
            hours = publish_blog(file_path, hours)
        logger.info("All blogs have been processed and scheduled for publishing.")
    except Exception as e:
        logger.error(f"Error in publishing all blogs: {e}")

def add_schema_markup(html_content: str, title: str, description: str) -> str:
    """
    Adds schema.org markup to the HTML content for better SERP visibility.
    """
    try:
        schema = f"""
        <script type="application/ld+json">
        {{
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": "{title}",
            "description": "{description}",
            "author": {{
                "@type": "Person",
                "name": "Your Name"
            }},
            "datePublished": "{datetime.now().date()}",
            "publisher": {{
                "@type": "Organization",
                "name": "Your Organization",
                "logo": {{
                    "@type": "ImageObject",
                    "url": "https://yourdomain.com/logo.png"
                }}
            }}
        }}
        </script>
        """
        return html_content + schema
    except Exception as e:
        logger.error(f"Error adding schema markup: {e}")
        return html_content

def suggest_external_links(content: str) -> List[str]:
    """
    Suggests external links based on the blog content using LLM.
    """
    try:
        prompt = (
            "Based on the following blog content, suggest five authoritative external links "
            "that can be included to enhance the content's credibility and SEO.\n\n"
            f"{content}"
        )
        links = llm.generate_text(prompt)
        link_list = [link.strip() for link in links.split('\n') if link.strip()]
        logger.info(f"Suggested external links: {link_list}")
        return link_list
    except Exception as e:
        logger.error(f"Error suggesting external links: {e}")
        return []

def insert_external_links(soup: BeautifulSoup, external_links: List[str]) -> None:
    """
    Inserts external links into the blog content at relevant positions.
    """
    try:
        for link in external_links:
            # For demonstration, append each link at the end of the first paragraph
            first_paragraph = soup.find('p')
            if first_paragraph:
                link_tag = soup.new_tag("a", href=link, target="_blank")
                link_tag.string = "External Reference"
                first_paragraph.append(link_tag)
                logger.info(f"Inserted external link: {link}")
    except Exception as e:
        logger.error(f"Error inserting external links: {e}")

def suggest_internal_links(content: str, existing_posts: List[str]) -> Dict[str, str]:
    """
    Suggests internal links based on the blog content and existing posts.
    """
    try:
        prompt = (
            "Based on the following blog content and list of existing blog titles, "
            "suggest relevant internal links to include within the content.\n\n"
            f"Content: {content}\n\n"
            f"Existing Posts: {', '.join(existing_posts)}\n\n"
            "Provide the suggestions in the format: 'keyword: link_title'"
        )
        suggestions = llm.generate_text(prompt)
        internal_links = {}
        for line in suggestions.split('\n'):
            if ':' in line:
                keyword, link_title = line.split(':', 1)
                internal_links[keyword.strip()] = link_title.strip()
        logger.info(f"Suggested internal links: {internal_links}")
        return internal_links
    except Exception as e:
        logger.error(f"Error suggesting internal links: {e}")
        return {}

def insert_internal_links(soup: BeautifulSoup, internal_links: Dict[str, str], existing_posts: List[str]) -> None:
    """
    Inserts internal links into the blog content based on the suggestions.
    """
    try:
        for keyword, link_title in internal_links.items():
            for text in soup.find_all(text=True):
                if keyword.lower() in text.lower():
                    parent = text.parent
                    if parent.name not in ['a', 'script', 'style']:
                        new_link = soup.new_tag("a", href=f"/blog/{link_title.replace(' ', '-').lower()}")
                        new_link.string = keyword
                        text.replace_with(text.replace(keyword, new_link))
                        logger.info(f"Inserted internal link for keyword '{keyword}' to '{link_title}'.")
                        break
    except Exception as e:
        logger.error(f"Error inserting internal links: {e}")
