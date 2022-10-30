from yt_dlp import YoutubeDL
import os
def download_video(video_id):
    ydl_opts = {
        'format': 'bestaudio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192'
        }],
        'postprocessor_args': [
            '-ar', '16000'
        ],
        'prefer_ffmpeg': False,
        'keepvideo': False,
        'outtmpl': os.path.join(f'{video_id}.wav')
    }
    ydl = YoutubeDL(ydl_opts)
    video_url = 'https://www.youtube.com/watch?v=' + video_id
    information = ydl.extract_info(video_url, download= False)
    if information['duration'] > 600:
        raise Exception('The duration of the video is more than 10 minutes')
    ydl.download([video_url])
    return (video_id + '.wav', information['title'], information['duration'])
