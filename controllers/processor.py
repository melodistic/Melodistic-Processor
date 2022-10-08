from helper.process_file import process_file
from helper.youtube_download import download_video

def youtube_processor(args):
    filename = download_video(args['video_id'])
    data = process_file(filename)
    return {"success": True, "data": data}

def file_processor(args):
    return args['file_path']