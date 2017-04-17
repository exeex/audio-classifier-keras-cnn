from __future__ import print_function

''' 
Preprocess audio
'''
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

import sys
import os

class visualizer:

    def draw_mel_mp3(self,audio_path):

        aud, sr = librosa.load(audio_path, sr=None)

        S = librosa.feature.melspectrogram(aud, sr=sr, n_mels=128, n_fft=1024, hop_length=512)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(librosa.power_to_db(S,ref=np.max),y_axis='mel',hop_length=512,sr=sr, fmax=8000,x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel spectrogram')
        plt.tight_layout()


    def draw_mel_npy(self,npy_path):

        melgram = np.load(npy_path)


        aud, sr = librosa.load(npy_path, sr=None)

        S = librosa.feature.melspectrogram(aud, sr=sr, n_mels=128, n_fft=1024, hop_length=512)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(librosa.power_to_db(S,ref=np.max),y_axis='mel',hop_length=512,sr=sr, fmax=8000,x_axis='time')
        plt.colorbar(format='%+2.0f dB')
        plt.title('Mel spectrogram')
        plt.tight_layout()


path = "/home/cswu/audio-classifier-keras-cnn/Samples/class1/american_bach_soloists-joseph_haydn__masses-01-kyrie__allegro_moderato-88-117.mp3"
path2 = "/home/cswu/audio-classifier-keras-cnn/Preproc/0/american_bach_soloists-j_s__bach__cantatas_volume_v-01-gleichwie_der_regen_und_schnee_vom_himmel_fallt_bwv_18_i_sinfonia-0-29.mp3.npy"
v = visualizer()
v.draw_mel_mp3(path)


