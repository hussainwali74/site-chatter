import os
import time
from datetime import datetime
import logging
import warnings
import traceback
warnings.filterwarnings("ignore", category=RuntimeWarning)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

from Tools.enums import ModelProvidersEnum
from WpManager.wp_manager import publish_all_blogs
from core.blog_writer import BlogWriter
from AI.llm import LLM
from Tools.utils import clear_cache, get_data_or_load_from_cache, read_file
from Transcriptor.transcriptor import fetch_transcript, fix_transcript

# llm = LLM(model_name=ModelProvidersEnum.G4F)
# messages = [{"role":"system","content":"You are a pirate"},{"role":"user","content":"Hello"}]
# # res = llm.generate_text("Hello")
# res = llm.chat(messages)
# print(res)
def main():
    directory = 'Transcripts'
    llm = LLM(model_name=ModelProvidersEnum.G4F)
    writer = BlogWriter(llm)
    
    youtube_urls = [
        "https://www.youtube.com/watch?v=mNxAM1ETBvs&ab_channel=LangChain"

        # Add more URLs as needed
    ]

    for url in youtube_urls:
        logging.info(f"Fetching transcript for URL: {url}")
        transcript = fetch_transcript(url,llm)

        if transcript:
            # Proceed with blog generation
            # Example:
            # generate_blog_from_transcript(transcript)
            pass
        else:
            logging.warning(f"Skipping URL due to missing transcript: {url}")
    
    try:
        for file_name in os.listdir(directory):
            if file_name.endswith('.txt'):
                transcript_path = os.path.join(directory, file_name)
                logging.info(f"Processing file: {transcript_path}")
                
                try:
                    transcript = read_file(transcript_path)
                    # fix transcript

                    key_information = get_data_or_load_from_cache(writer.get_key_information, 'key_information', transcript)
                    logging.info("Key information extracted")
                    time.sleep(4)
                    focus_keyphrase = get_data_or_load_from_cache(writer.get_focus_keyphrase, 'focus_keyphrase', key_information)
                    logging.info("Focus keyphrase generated")
                    time.sleep(4)

                    blog_outline = get_data_or_load_from_cache(writer.get_blog_outline, 'blog_outline', focus_keyphrase, key_information)
                    logging.info("Blog outline created")
                    time.sleep(5)
                    print('\n\n blog_outline',blog_outline);
                    print('\n ============\n\n');


                    if blog_outline:
                        blog = get_data_or_load_from_cache(writer.write_blog, 'blog', key_information, blog_outline, focus_keyphrase)
                        logging.info("Blog content generated")

                        final_blog_file_name = file_name.split('.')[0]
                        now = datetime.now()
                        st = now.strftime('%H%M%S%d%m%y')
                        final_blog_file_name += st + '.md'
                        final_blog_file_name = final_blog_file_name.replace('\\n', '')
                        
                        try:
                            with open('Blogs/' + final_blog_file_name, 'w', encoding='utf-8') as f:
                                f.write(blog)
                            logging.info(f"Blog saved to file: {final_blog_file_name}")
                        except IOError as e:
                            logging.error(f"Error saving blog to file: {e}")
                        
                        clear_cache()
                        logging.info("Cache cleared")
                    else:
                        logging.warning(f"No blog outline generated for {file_name}")
                
                except Exception as e:
                    logging.error(f"Error processing file {file_name}: {str(e)}")
                    logging.debug(traceback.format_exc())
    
    except Exception as e:
        logging.critical(f"Critical error in main function: {str(e)}")
        logging.debug(traceback.format_exc())

if __name__ == "__main__":
    try:
        main()
        # publish_all_blogs()
        logging.info("All blogs published successfully")
    except Exception as e:
        logging.critical(f"Error in publishing blogs: {str(e)}")
        logging.debug(traceback.format_exc())