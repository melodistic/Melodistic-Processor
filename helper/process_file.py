from spleeter.separator import Separator
from pydub import AudioSegment
import os
import shutil
import gc
import random

def detect_leading_silence(sound, chunk_size=10):
    silence_threshold = sound.dBFS * 1.5
    trim_ms = 0 
    assert chunk_size > 0
    while sound[trim_ms:trim_ms+chunk_size].dBFS < silence_threshold and trim_ms < len(sound):
        trim_ms += chunk_size

    return trim_ms

def preprocessing(audio):
    start_trim = detect_leading_silence(audio)
    end_trim = detect_leading_silence(audio.reverse())
    duration = len(audio)
    trimmed_sound = audio[start_trim:duration-end_trim]
    del audio
    gc.collect()
    return trimmed_sound

def extract_instrumental(audio,name):
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(audio, 'instrumental/')
    os.rename('instrumental/'+name.split('.')[0]+'/accompaniment.wav', 'instrumental/'+name)
    shutil.rmtree('instrumental/'+name.split(".")[0])

def extracting(audio,filename,mood):
    size = len(audio)
    time_30_sec = 30 * 1000
    audio_list = []
    for i in range(20):
        start = random.randint(0,size-time_30_sec)
        end = start + time_30_sec
        audio_list.append(audio[start:end])
    try:
        os.mkdir('extract/'+str(mood))
    except:
        pass
    data = []
    for i in range(len(audio_list)):
        audio_list[i].export("extract/"+str(mood) + "/" + str(filename.split(".")[0]) + "_"+ str(i) + '.wav', format="wav")
        data.append([str(filename.split(".")[0]) + "_"+ str(i) + '.wav', mood])
    del audio_list
    gc.collect()
    return data

def process_file(filename: str):
    extract_instrumental("process/"+filename, filename)
    audio = AudioSegment.from_wav("instrumental/"+filename)
    audio = preprocessing(audio)
    data = extracting(audio,filename,"test")
    os.remove("instrumental/"+filename)
    os.remove("process/"+filename)
    return data