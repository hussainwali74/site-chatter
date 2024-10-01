from Tools.utils import  timer_decorator
from typing import List
import logging
import markdown
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

def extract_keywords(blog_content: str, llm_instance) -> List[str]:
    """
    Extracts relevant keywords from the blog content using LLM.
    """
    try:
        prompt = (
            "Extract the top 10 SEO keywords from the following blog content. "
            "Ensure that the keywords are relevant and have high search volume.\n\n"
            f"{blog_content}"
        )
        keywords_text = llm_instance.generate_text(prompt)
        keywords = [keyword.strip() for keyword in keywords_text.split(',')][:10]
        logger.info(f"Extracted keywords: {keywords}")
        return keywords
    except Exception as e:
        logger.error(f"Error extracting keywords: {e}")
        return []

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

class BlogWriter:
    def __init__(self, llm):
        self.llm = llm

    @timer_decorator
    def get_key_information(self, transcript):
        extract_information_prompt=f"""Please ignore all previous instructions. I want you to only answer in English.
            Extract a list of facts from the given content, if any. Keep facts short and easy to understand. Write the most important facts first.
            Format result in a bullet point list. 
            Do not extract information about the speaker, just the products and any other information they are talking about. 
            Do not include information about the people in the script. present it from your own point of view.
            Do not talk about sponsors of the video
            this is the content:  {transcript}
            Do not include any additional information like "Hello, this is bing" etc.
        """
        key_information = self.llm.generate_text(extract_information_prompt)
        return key_information

    @timer_decorator
    def get_focus_keyphrase(self, key_information):
        focus_keyphrase_prompt=f"""
            'please try again you did not do a good job. I am writing a blog article and I want you to give me a focus keyphrase for the article. please don't add apology or any other explaination. please only give me the keyphrase nothing else. your response is directly being fed to a python program if your response includes anything other than the keyphrase the whole program breaks.
            Your reponse should be only the focus keyphrase. using this key_information: 
            --------------------------------------------------------------------------------
            '{key_information}'
            --------------------------------------------------------------------------------
            Important Note: 
            - do not include explainations in your response like: Here is a focus keyphrase for your blog article:
            - do not include any question like: Would you like me to generate another focus keyphrase?
            """
            
        focus_keyphrase = self.llm.generate_text(focus_keyphrase_prompt)
        if '\n' in focus_keyphrase:
            focus_keyphrase = focus_keyphrase.split('\n')[0]
        return focus_keyphrase
    
    @timer_decorator
    def get_blog_outline(self, focus_keyphrase, key_information):
        outline_creation_prompt=f"""
        forget all previous commands.  
        Using the information Develop a comprehensive "Outline" for a long-form article for the Keyword {focus_keyphrase}, featuring at least 25 engaging headings and subheadings that are detailed, mutually exclusive, collectively exhaustive, and cover the entire topic. Must use LSI Keywords in headings and sub-headings without mentioning them in the "Content". Must show these "Outlines" in a table.
        information for you: {key_information}
        Note: Your response should include only the outline, no other explaination or additional information or greetings for example "Sure! Here is a possible outline .." .
        """
        blog_outline = self.llm.generate_text(outline_creation_prompt)
        return blog_outline

    @timer_decorator
    def write_blog(self, key_information, blog_outline, focus_keyphrase):
        blog_write_prompt = f"""
        forget all previous commands.  
        use this key information as your context for writing it: {key_information}
        Act as an Expert Article Writer employed at Balooger.com and write a fully detailed, long-form, 100% unique, creative, and human-like informational article of
        a minimum of 2000 words in Grade 7 English, using headings and sub-headings.
        Use this blog outline. OUTLINE: {blog_outline}
        Click-worthy short title. Also, use the seed keyword as the first H2. Always use a combination of paragraphs, lists, and tables for a better reader experience.
        Use fully detailed paragraphs that engage the reader. Write at least one section with the heading {focus_keyphrase}. Write down at least six FAQs with answers
        and a conclusion. 

        Note: Don't assign Numbers to Headings. Don't assign numbers to Questions. Don't write Q: before the question (faqs)

        Make sure the article is plagiarism-free. Don't forget to use a question mark (?) at the end of questions. Try not to change the original {focus_keyphrase}
        while writing the title. Try to use "{focus_keyphrase}" 2-3 times in the article. Try to include {focus_keyphrase} in the headings as well. write content that
        can easily pass the AI detection tools test. Bold all the headings and sub-headings using Markdown formatting. 

        MUST FOLLOW THESE INSTRUCTIONS IN THE ARTICLE:
        1. Make sure you are using the Focus Keyword in the SEO Title.
        2. Use The Focus Keyword inside the SEO Meta Description.
        3. Make Sure The Focus Keyword appears in the first 10% of the content.
        4. Make sure The Focus Keyword was found in the content
        5. Make sure Your content is 2000 words long. 
        6. Must use The Focus Keyword in the subheading(s).
        7. Make sure the Keyword Density is 1.30
        8. Must Create At least one external link in the content.
        9. Must use a positive or a negative sentiment word in the Title.
        10. Must use a Power Keyword in the Title.
        11. Must use a Number in the Title.
        12. The article must be using markdown formatting for headings and subheadings etc
        13. Ensure proper spacing
        14. Mention balooger.com

        Note: Now start, it should be complete blog.
        Your response should be only the markdown formatted blog, no other explainations like "I'm happy to help you write a detailed..."
        """

        blog_content = self.llm.generate_text(blog_write_prompt)

        # Extract keywords from the generated blog content
        keywords = extract_keywords(blog_content, self.llm)

        # Add SEO metadata to the blog content
        blog_content_with_metadata = add_seo_metadata(blog_content, keywords)

        if not self.validate_markdown_structure(blog_content_with_metadata):
            logger.warning("Generated blog failed markdown structure validation. Skipping publish.")
            return ""
        return blog_content_with_metadata

    def extract_keywords(self, blog_content: str) -> List[str]:
        """
        Extracts relevant keywords from the blog content using LLM.
        """
        try:
            prompt = (
                "Extract the top 10 SEO keywords from the following blog content. "
                "Ensure that the keywords are relevant and have high search volume.\n\n"
                f"{blog_content}"
            )
            keywords = self.llm.generate_text(prompt)
            keyword_list = [keyword.strip() for keyword in keywords.split(',')]
            logger.info(f"Extracted keywords: {keyword_list}")
            return keyword_list
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []

    def write_blog_from_titles(self, titles: List[str]) -> str:
        """
        Generates blog content based solely on the provided titles.
        Each title is used as a heading followed by generated content.
        """
        try:
            if not titles:
                logger.error("No titles provided for blog generation.")
                return ""
            
            prompt = (
                "Write a comprehensive blog post using only the following titles. "
                "Ensure that each section strictly follows its title without adding unrelated information.\n\n"
                f"Titles: {', '.join(titles)}\n\n"
                "Blog Content:"
            )
            blog_content = self.llm.generate_text(prompt)
            logger.info("Blog content generated based on titles.")
            return blog_content
        except Exception as e:
            logger.error(f"Error writing blog from titles: {e}")
            return ""

    def validate_markdown_structure(self, markdown_content: str) -> bool:
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