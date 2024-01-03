pip install git+https://github.com/MIDORIBIN/langchain-gpt4free.git
## YT transcript to Balooger
    paste yt transcript in Transcripts folder.
    -  main.py -> 
        from yt transcript create markdown blog
`---`
WpManager:
    convert markdown blog to html post_manager, use wp_manager to add media under 3 sections of each blog

    wp_manager: 
        upload blog
        upload media
        upload media detail

<!-- ------------------------------------------------------------------------- -->
Todo:
    - Core
        - verify core output blogs are valid markdown with h1, h2, h3
        - improve SEO, keywords addition 
        - write using only titles
        - SERP for title only blogs
        - SERP external linking 
        - internal linking

    - Social Media Manager
        - create tweet and post automatically
        - insta post create
    - WpManager:
        - featured images
    - Transcriptor:
        - from yt link get transcript
            - https://pypi.org/project/youtube-transcript-api/  
            - extract key informations from the transcript    