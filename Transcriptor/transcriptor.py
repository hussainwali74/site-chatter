from typing import Optional
import logging
import os
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

from AI.llm import LLM

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define cache directory and cache index file
CACHE_DIR = os.path.join('Transcriptor', 'transcripts_cache')
CACHE_INDEX_FILE = os.path.join(CACHE_DIR, 'cache_index.json')

# Ensure cache directory exists
os.makedirs(CACHE_DIR, exist_ok=True)

def get_video_id(youtube_url: str) -> str:
    """
    Extracts the video ID from a YouTube URL.
    """
    try:
        import re
        video_id = re.search(r"(?<=v=)[^&#]+", youtube_url)
        if video_id:
            return video_id.group(0)
        else:
            logger.error("Invalid YouTube URL format.")
            return ""
    except Exception as e:
        logger.error(f"Error extracting video ID: {e}")
        return ""

def load_cache_index() -> dict:
    """
    Loads the cache index from the JSON file.
    """
    if os.path.exists(CACHE_INDEX_FILE):
        with open(CACHE_INDEX_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_cache_index(cache_index: dict):
    """
    Saves the cache index to the JSON file.
    """
    with open(CACHE_INDEX_FILE, 'w') as f:
        json.dump(cache_index, f, indent=2)

def fetch_transcript(youtube_url: str, llm:LLM) -> Optional[str]:
    """
    Fetches the transcript for a given YouTube URL, using local cache if available.
    """
    try:
        video_id = get_video_id(youtube_url)
        if not video_id:
            return None

        cache_index = load_cache_index()
        cache_file = os.path.join(CACHE_DIR, f"{video_id}.txt")

        # Check if transcript is in cache
        if video_id in cache_index and os.path.exists(cache_file):
            logger.info(f"Using cached transcript for video {video_id}")
            with open(cache_file, 'r', encoding='utf-8') as f:
                return f.read()

        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript(['en'])
        fetched_transcript = transcript.fetch()
        transcript_text = ' '.join([entry['text'] for entry in fetched_transcript])
        logger.info(f"Fixing the Transcript")
        transcript_text = fix_transcript(transcript_text, llm)
        logger.info(f"Transcript fixed")
        # Save to Transcripts folder (original behavior)
        transcript_path = os.path.join('Transcripts', f"{video_id}.txt")
        with open(transcript_path, 'w', encoding='utf-8') as f:
            f.write(transcript_text)
        logger.info(f"Transcript fetched and saved to '{transcript_path}'.")

        # Save to cache
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(transcript_text)
        cache_index[video_id] = cache_file
        save_cache_index(cache_index)
        logger.info(f"Transcript cached for video {video_id}")

        return transcript_text
    except TranscriptsDisabled:
        logger.error("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        logger.error("No transcript found for this video.")
    except Exception as e:
        logger.error(f"Error fetching transcript: {e}")
    return None

def fix_transcript(transcript: str, llm:LLM) -> str:
    """
    Fixes the transcript by replacing common transcription errors.
    """
    # Example: Replace 'langraph' with 'Langra'
    prompt = f"""
    This is a transcript of a YouTube video that was automatically generated. 
    Due to the limitations of automatic speech recognition, there are often errors or misinterpretations in the transcript. 
    For example, the system might confuse technical terms or proper nouns:
    - 'LangChain' might be transcribed as 'Langa chain' or 'language chain'
    - 'LangGraph' might be transcribed as 'Langra' or 'language graph'
    - 'GPT-4' might appear as 'GPT 4' or 'G PT 4'
    - 'GPT-4o' might appear as 'GPD 40'
    - Names of people or places might be misspelled

    Please review and correct any such errors in the following transcript to best of your ability, 
    paying special attention to technical terms, proper nouns, and commonly misheard phrases.
    
    Here is the transcript to be corrected:

    {transcript}
    """
    transcript = llm.fast_generate(prompt)
    return transcript

