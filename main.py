import os
import time
from datetime import datetime

import logging
logging.basicConfig(level=logging.INFO)

from WpManager.wp_manager import publishAllBlogs
from core.blog_writer import BlogWriter
from AI.llm import LLM
from Tools.utils import clear_cache, get_data_or_load_from_cache, read_file

def main():
    directory='Transcripts'
    llm = LLM()
    writer = BlogWriter(llm)
    
    for file_name in os.listdir(directory):
        if file_name.endswith('.txt'):
            transcript_path = os.path.join(directory, file_name)
            print("-------------------------------------------------------------------------")
            print(f"{transcript_path=}")
            print("-------------------------------------------------------------------------")
            
            transcript = read_file(transcript_path)

            key_information = get_data_or_load_from_cache(writer.get_key_information, 'key_information', transcript)
            time.sleep(4)
            focus_keyphrase = get_data_or_load_from_cache(writer.get_focus_keyphrase, 'focus_keyphrase', key_information)
            time.sleep(4)
            blog_outline = get_data_or_load_from_cache(writer.get_blog_outline, 'blog_outline', focus_keyphrase, key_information)
            time.sleep(5)
            if blog_outline:
                blog = get_data_or_load_from_cache(writer.write_blog, 'blog', key_information, blog_outline, focus_keyphrase)

                final_blog_file_name = file_name.split('.')[0]
                now = datetime.now()
                st = now.strftime('%H%M%S%d%m%y')
                final_blog_file_name += st + '.md'
                final_blog_file_name = final_blog_file_name.replace('\\n', '')
                logging.info('Saving to file \n ')
                with open('Blogs/' + final_blog_file_name, 'w', encoding='utf-8') as f:
                    f.write(blog)
                clear_cache()
                # clear_cache(['key_information', 'focus_keyphrase', 'blog_outline'])

if __name__ == "__main__":
    # main()
    publishAllBlogs()

