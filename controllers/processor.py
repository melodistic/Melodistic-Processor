from helper.process_file import process_file
from helper.youtube_download import download_video

def youtube_processor(args):
    (file_name, song_name, duration) = download_video(args['video_id'])
    process_file(args['user_id'], file_name, song_name, duration)
    return {"success": True}

def file_processor(args):
    return args['file_path']