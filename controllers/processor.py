from helper.process_file import get_duration, process_file
from helper.youtube_download import download_video

def youtube_processor(args):
    (file_name, song_name, duration) = download_video(args['video_id'])
    process_file(args['user_id'], file_name, song_name, duration, "process/")
    return {"success": True}

def file_processor(args):
    print(args)
    try:
        duration = get_duration(args['file_path'])
        process_file(args['user_id'], args['file_path'], args['file_name'], duration)
    except Exception as e:
        print(e)
    return {"success": True}