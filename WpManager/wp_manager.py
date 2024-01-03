import re
import os
import markdown

from bs4 import BeautifulSoup

from bing_image_downloader import downloader

from WpManager.post_manager import media_creator, media_details_adder, post_creator

import logging
logging.basicConfig(level=logging.INFO)

from AI.llm import LLM

# get a list of all markdown files in the Blogs directory
blog_dir = 'Blogs'
blog_files = [f for f in os.listdir(blog_dir) if f.endswith('.md')]
print("-------------------------------------------------------------------------")
print(f"{blog_files=}")
print("-------------------------------------------------------------------------")

hours = 0
llm = LLM()
def publishAllBlogs():
    global hours
    illegal_chars = r'[,.:"/\\|?*]'
    for i, blog_file in enumerate(blog_files):
        with open(os.path.join(blog_dir, blog_file), 'r') as f:
            md = markdown.Markdown()
            html = md.convert(f.read())
            soup = BeautifulSoup(html, 'html.parser')
            print("-------------------------------------------------------------------------")
            print(f"{soup=}")
            print(f"{html=}")
            print("-------------------------------------------------------------------------")
            
            title = soup.h1.text if soup.h1 else 'No Title'
            print("-------------------------------------------------------------------------")
            print(f"{title=}")
            print("-------------------------------------------------------------------------")
            
            topics = [h2.text.strip().lower() for h2 in soup.find_all('h2')]
            
            non_topics = [x.lower() for x in ['SEO Meta Description:', 'Conclusion', 'FAQs']]
            topics = [re.sub(illegal_chars,'',topic.lower()) for topic in topics if topic not in non_topics and 'conclusion' not in topic.lower()]
            n = len(topics) if len(topics) < 3 else 3

            query_topic_dict = {}
            for i in range(n):
                topic = topics[i]
                logging.info(f'getting image for topic: {topics[i]=} \n', )
                title=re.sub(illegal_chars,'',title)
                topic=re.sub(illegal_chars,'',topic)
                outdir = os.path.join('Blogs','blog_images',title)
                query = title+ ' ' +topic
                query = llm.instruct_generate('shorten this search query, it will be used to fetch relevant image from internet. do not add any other explaination or information as it will cause error. your response should be only shorter search query. The shortened version should capture the WHOLE essence of the original search query. Here is the search query: '+query)
                print("-------------------------------------------------------------------------")
                print(f"{query=}")
                print("-------------------------------------------------------------------------")
                query = re.sub(illegal_chars,'',query)
                query_topic_dict[topic] = query
                downloader.download(query, limit=1, output_dir=outdir, adult_filter_off=True)
            
            print("-------------------------------------------------------------------------")
            print(f"{query_topic_dict=}")
            all_topics = [j.text for j in soup.find_all('h2')]
                        
            for topic_ in all_topics:
                topic__ = re.sub(illegal_chars,'',topic_.lower())
                topic_img_dir = query_topic_dict.get(topic__)

                if topic_img_dir:
                    
                    h2 = soup.find('h2', string=topic_)  
                    if h2:
                        title_for_dir= re.sub(illegal_chars,'',title)
                        outdir = os.path.join('Blogs','blog_images',title_for_dir,topic_img_dir)
                        print("-------------------------------------------------------------------------")
                        print(f"{outdir=}")
                        print("-------------------------------------------------------------------------")
                        
                        image_paths = [os.path.join(outdir, img) for img in os.listdir(outdir)]
                        if image_paths:
                            image_path=image_paths[0]
                            print("-------------------------------------------------------------------------")
                            print(f"{image_path=}")
                            print("-------------------------------------------------------------------------")
                            media_detail=media_creator(image_path)
                            if media_detail:
                                media_id, media_url = media_detail['media_id'], media_detail['media_url']
                                media_details_adder(media_id,topic_, caption=topic_,description=title)
                                img_tag = soup.new_tag("img") 
                                img_tag['src'] = media_url
                                h2.insert_after(img_tag)
                          
            # schedule the post for i hours from now
            hours+=4
            post_creator(title, content=soup.prettify(), postStatus='future', hours=hours)
            
        break
   

##############################################################################
# you are changing the query with llm
##############################################################################
    
