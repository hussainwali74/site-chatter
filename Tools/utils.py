import timeit
import os
import glob
import pickle
import logging

def timer_decorator(func):
   def wrapper(*args, **kwargs):
       start_time = timeit.default_timer()
       result = func(*args, **kwargs)
       end_time = timeit.default_timer()
       print(f'{func.__name__} executed in {end_time - start_time} seconds')
       return result
   return wrapper

cache_directory = 'cache'
os.makedirs(cache_directory, exist_ok=True)  # Create the cache directory if it doesn't exist

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
def load_from_cache(file_name):
    with open(os.path.join(cache_directory, file_name), 'rb') as f:
        return pickle.load(f)

def save_to_cache(data, file_name):
    with open(os.path.join(cache_directory, file_name), 'wb') as f:
        pickle.dump(data, f)

def splitTranscript(transcript):
    if len(transcript.split())>2000:
        return [''.join(transcript[i:i+3000]) for i in range(0, len(transcript),3000)]
    return transcript

def process_transcript(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        transcript = f.read()
    return splitTranscript(transcript)

def get_data_or_load_from_cache(get_data_func, data_name, *args):
    cache_file_name = f'{data_name}.pkl'
    if os.path.exists(os.path.join(cache_directory, cache_file_name)):
        data = load_from_cache(cache_file_name)
        if data:  # Check if data is not empty
            logging.info(f'Loading {data_name} from cache')
            return data
    logging.info(f'Getting {data_name}')
    data = get_data_func(*args)
    save_to_cache(data, cache_file_name)
    return data

def clear_cache(cache_names=None):
    if cache_names is None:
        files = glob.glob(os.path.join(cache_directory, '*'))
    else:
        files = [os.path.join(cache_directory, f'{name}.pkl') for name in cache_names]
    for file_path in files:
        if os.path.exists(file_path):
            with open(file_path, 'wb') as file:
                pickle.dump({}, file)
            pickle.dump({}, file)