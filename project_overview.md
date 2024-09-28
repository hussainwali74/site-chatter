balooger/
├── Db/
│   ├── models/
│   │   ├── todos_model.py
│   │   └── yt_models.py
│   ├── __init__.py
│   ├── database.py
│   ├── yt_db_channel_manager.py
│   ├── yt_db_channelId_manager.py
│   ├── yt_db_manager.py
│   └── yt_db_video_manager.py
├── Engines/
│   ├── OpenAILM/
│   │   ├── __init__.py
│   │   └── gpt.py
│   ├── Writer/
│   │   ├── __init__.py
│   │   ├── blog_writer.py
│   │   └── prompts.py
│   ├── youtube/
│   │   ├── __init__.py
│   │   ├── json_to_db.py
│   │   └── yt_engine.py
│   └── __init__.py
├── Scrapper/
│   ├── channel_ids.txt
│   ├── channel_names.txt
│   ├── r_playwright.py
│   └── socialblade.js
├── Tools/
│   └── __init__.py
├── Wp/
│   └── __init__.py
├── .env.example
├── .gitignore
├── docker-compose.yml
├── main.ipynb
├── README.md
├── requirements.txt
└── test.py

<ProjectOverview>
    <FolderStructure>
        <Folder name="balooger">
            <Folder name="Db">
                <Folder name="models">
                    <File name="todos_model.py" />
                    <File name="yt_models.py" />
                </Folder>
                <File name="__init__.py" />
                <File name="database.py" />
                <File name="yt_db_channel_manager.py" />
                <File name="yt_db_channelId_manager.py" />
                <File name="yt_db_manager.py" />
                <File name="yt_db_video_manager.py" />
            </Folder>
            <Folder name="Engines">
                <Folder name="OpenAILM">
                    <File name="__init__.py" />
                    <File name="gpt.py" />
                </Folder>
                <Folder name="Writer">
                    <File name="__init__.py" />
                    <File name="blog_writer.py" />
                    <File name="prompts.py" />
                </Folder>
                <Folder name="youtube">
                    <File name="__init__.py" />
                    <File name="json_to_db.py" />
                    <File name="yt_engine.py" />
                </Folder>
                <File name="__init__.py" />
            </Folder>
            <Folder name="Scrapper">
                <File name="channel_ids.txt" />
                <File name="channel_names.txt" />
                <File name="r_playwright.py" />
                <File name="socialblade.js" />
            </Folder>
            <Folder name="Tools">
                <File name="__init__.py" />
            </Folder>
            <Folder name="Wp">
                <File name="__init__.py" />
            </Folder>
            <File name=".env.example" />
            <File name=".gitignore" />
            <File name="docker-compose.yml" />
            <File name="main.ipynb" />
            <File name="README.md" />
            <File name="requirements.txt" />
            <File name="test.py" />
            <File name="routes">
                <File name="route.py" />
            </File>
        </Folder>
    </FolderStructure>
    <TechStack>
        <Technology name="Python" version="3.10.6" description="Programming language used for the project." />
        <Technology name="FastAPI" version="latest" description="Web framework for building APIs." />
        <Technology name="Uvicorn" version="latest" description="ASGI server for serving FastAPI applications." />
        <Technology name="Pymongo" version="latest" description="MongoDB driver for Python." />
        <Technology name="Google API Python Client" version="latest" description="Client library for accessing Google APIs." />
        <Technology name="Pandas" version="latest" description="Data manipulation and analysis library." />
        <Technology name="Seaborn" version="latest" description="Statistical data visualization library." />
        <Technology name="Matplotlib" version="latest" description="Plotting library for creating static, animated, and interactive visualizations." />
        <Technology name="Pytest-Playwright" version="latest" description="End-to-end testing library using Playwright." />
        <Technology name="Python-dotenv" version="latest" description="Reads key-value pairs from a .env file and can set them as environment variables." />
        <Technology name="HTTPX" version="latest" description="HTTP client for Python." />
        <Technology name="Markdown" version="latest" description="Library for converting Markdown to HTML." />
        <Technology name="Motor" version="latest" description="Asynchronous Python driver for MongoDB." />
        <Technology name="IJJSON" version="latest" description="Iterative JSON parser." />
        <Technology name="IPykernel" version="latest" description="Jupyter kernel for Python." />
        <Technology name="Docker" version="19.03" description="Containerization platform used for deployment." />
    </TechStack>
    <FileDescriptions>
        <File name="todos_model.py" description="Defines the database model for todos." />
        <File name="yt_models.py" description="Defines the database models for YouTube channels and videos." />
        <File name="__init__.py" description="Initializes Python packages." />
        <File name="database.py" description="Handles database connections and sessions." />
        <File name="yt_db_channel_manager.py" description="Manages YouTube channel data in the database." />
        <File name="yt_db_channelId_manager.py" description="Manages YouTube channel IDs in the database." />
        <File name="yt_db_manager.py" description="General YouTube database manager handling channels and videos." />
        <File name="yt_db_video_manager.py" description="Manages YouTube video data in the database." />
        <File name="gpt.py" description="Interacts with OpenAI GPT-3 for text generation." />
        <File name="blog_writer.py" description="Generates blog content using predefined prompts." />
        <File name="prompts.py" description="Contains prompts for text generation." />
        <File name="json_to_db.py" description="Converts JSON data to database entries." />
        <File name="yt_engine.py" description="Engine for processing YouTube data, including fetching and saving channel/video details." />
        <File name="r_playwright.py" description="Script for web scraping using Playwright." />
        <File name="socialblade.js" description="JavaScript file for scraping SocialBlade data." />
        <File name="main.ipynb" description="Jupyter notebook for project exploration and testing." />
        <File name="README.md" description="Project documentation and overview." />
        <File name="requirements.txt" description="List of project dependencies." />
        <File name="test.py" description="Test script for the project." />
        <File name="route.py" description="Defines API routes for the application." />
        <File name="docker-compose.yml" description="Defines Docker services, networks, and volumes for the project." />
        <File name=".env.example" description="Sample environment variables file." />
        <File name=".gitignore" description="Specifies intentionally untracked files to ignore." />
    </FileDescriptions>
    <SetupInstructions>
        <Step>Clone the repository from GitHub.</Step>
        <Step>Navigate to the project directory.</Step>
        <Step>Create a virtual environment using <code>python -m venv balooger_env</code>.</Step>
        <Step>Activate the virtual environment:</Step>
        <Step>For Windows, run <code>source balooger_env/Scripts/activate</code>.</Step>
        <Step>Install the required dependencies using <code>pip install -r requirements.txt</code>.</Step>
        <Step>Set up the database by running the <code>database.py</code> script.</Step>
        <Step>Configure environment variables as specified in <code>.env.example</code>.</Step>
        <Step>Run the project using <code>docker-compose up</code>.</Step>
    </SetupInstructions>
    <UsageInstructions>
        <Step>Start the project using <code>docker-compose up</code>.</Step>
        <Step>Access the web interface at <code>http://localhost:8000</code>.</Step>
        <Step>Use the provided endpoints to interact with the project.</Step>
        <Step>Refer to the <code>README.md</code> for detailed API documentation.</Step>
    </UsageInstructions>
    <AdditionalInformation>
        <Detail>This project is designed to scrape YouTube data and generate blog content using OpenAI GPT-3.</Detail>
        <Detail>Ensure that you have the necessary API keys and access tokens configured in the environment variables.</Detail>
        <Detail>Refer to the <code>README.md</code> for more detailed documentation and troubleshooting tips.</Detail>
    </AdditionalInformation>
</ProjectOverview>