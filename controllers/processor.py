from helper.youtube_download import download_video

def youtube_processor(args):
    filename = download_video(args['video_id'])
    return {"success": True, "filename": filename}

def file_processor(args):
    return args['file_path']