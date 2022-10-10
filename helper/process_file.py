import sys
from singleton.prediction_model import PredictionModel
from pydub import AudioSegment
import os
import shutil
import gc
import random
import librosa
import numpy as np
import tensorflow as tf
from PIL import Image

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

def scale_minmax(X, min=0.0, max=1.0):
    X_std = (X - X.min()) / (X.max() - X.min())
    X_scaled = X_std * (max - min) + min
    return X_scaled

def save_image(data,file_path):
    img = scale_minmax(data, 0, 255).astype(np.uint8)
    img = np.flip(img, axis=0) # put low frequencies at the bottom in image
    img = 255-img
    im = Image.fromarray(img)
    im = im.resize((224,224))
    im.save(file_path)
    del img, im
    gc.collect()

def convert_audio_to_mel_spectogram(filename):
    x, sr = librosa.load(filename)
    S = librosa.feature.melspectrogram(x, sr=sr, n_mels=256)
    mels = np.log(S + 1e-9)
    spectogram_path = "spectogram/" + filename.split("/")[-1].split('.')[0] + '.png'
    save_image(mels,spectogram_path)
    del x, sr, S, mels
    gc.collect()
    return spectogram_path

def extracting(audio,filename):
    size = len(audio)
    time_30_sec = 30 * 1000
    audio_list = []
    for i in range(20):
        start = random.randint(0,size-time_30_sec)
        end = start + time_30_sec
        audio_list.append(audio[start:end])
    try:
        os.mkdir('extract/')
    except:
        pass
    data = []
    for i in range(len(audio_list)):
        audio_list[i].export("extract/" + str(filename.split(".")[0]) + "_"+ str(i) + '.wav', format="wav")
        data.append(str(filename.split(".")[0]) + "_"+ str(i) + '.wav')
    del audio_list
    gc.collect()
    return data

def get_spectrogram(path):
    IMAGE_SIZE = 224
    img = tf.keras.preprocessing.image.load_img(path, target_size=(IMAGE_SIZE, IMAGE_SIZE)
    )
    img_array = tf.keras.preprocessing.image.img_to_array(img)
    img_array = img_array / 255
    img_array = img_array.reshape(1,IMAGE_SIZE,IMAGE_SIZE,3)
    return img_array

def get_bpm(path):
    path = 'extract/' + path
    y, sr = librosa.load(path)
    tempo, _ = librosa.beat.beat_track(y,sr)
    del y, sr
    gc.collect()
    return tempo

def prediction(audio):
    model = PredictionModel().model
    model.compile()
    model.run_eagerly = True
    class_labels = ["Anxious","Chill","Focus","Party","Romance","Sad"]
    predictions = model.predict(audio)
    mood = class_labels[np.argmax(predictions)]
    feature_model = PredictionModel().feature_model
    features = feature_model.predict(audio)
    return mood,features

def process_file(filename: str):
    # Insert Process Data into DB (ProcessedMusic)
    os.system("python3 helper/separator.py -f " + filename)
    audio = AudioSegment.from_wav("instrumental/"+filename)
    audio = preprocessing(audio)
    extract_list = extracting(audio,filename)
    data = []
    for file in extract_list:
        spectrogram_path = convert_audio_to_mel_spectogram("extract/"+file)
        spectrogram = get_spectrogram(spectrogram_path)
        bpm = get_bpm(file)
        mood, features = prediction(spectrogram)
        # Write Features into JSON file
        # Insert Data into DB (Music, ProcessedMusicExtract)
        data.append({"file":file,"mood":mood,"bpm":int(bpm)})
    # Update ProcessedMusic
    os.remove("instrumental/"+filename)
    os.remove("process/"+filename)
    return data