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
    information = YoutubeDL(ydl_opts).extract_info('https://www.youtube.com/watch?v=' + video_id, download=True)
    return (video_id + '.wav', information['title'], information['duration'])
