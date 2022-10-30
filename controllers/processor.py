from helper.process_file import get_duration, processor
from helper.youtube_download import download_video

def youtube_processor(args):
    try:
        (file_name, song_name, duration) = download_video(args['video_id'])
        process_id = processor(args['user_id'], file_name, song_name, duration)
        return {"success": True, "process_id": process_id}
    except Exception as e:
        return {"success": False, "message": str(e)}, 400

def file_processor(args):
    duration = get_duration(args['file_path'])
    process_id = processor(args['user_id'], args['file_path'], args['file_name'], duration)
    return {"success": True, "process_id": process_id}