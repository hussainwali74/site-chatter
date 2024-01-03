from Tools.utils import  timer_decorator

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
        It should be in Using markdown formatting. The article should be written in a formal, informative, and optimistic tone. Must Read all the information below.

        Use English for the keyword "{focus_keyphrase}" and write at least 400–500 words of engaging paragraph under each and every Heading. This article should show 
        the experience, expertise, authority and trust for the Topic {focus_keyphrase}. Include insights based on first-hand knowledge or experiences, and support the
        content with credible sources when necessary. Focus on providing accurate, relevant, and helpful information to readers, showcasing both subject matter expertise
        and personal experience in the topic {focus_keyphrase}.

        Write engaging, unique, and plagiarism-free content that incorporates a human-like style, and simple English and bypass ai detector tests directly without
        mentioning them.

        Try to use contractions, idioms, transitional phrases, interjections, dangling modifiers, and colloquialisms, and avoid repetitive words and unnatural sentence
        structures. 

        The article must include an SEO meta-description right after the title (you must include the {focus_keyphrase} in the description), an introduction, and a 
        click-worthy short title. Also, use the seed keyword as the first H2. Always use a combination of paragraphs, lists, and tables for a better reader experience.
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
        res = self.llm.generate_text(blog_write_prompt)
        return res
