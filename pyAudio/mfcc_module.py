from python_speech_features import mfcc
from python_speech_features import logfbank
import librosa
from pysndfx import AudioEffectsChain
import numpy as np
import math
import scipy.io.wavfile as wav
import pyaudio
import datetime
import wave
 
au_format = pyaudio.paInt16
no_channels = 2
chunk = 1024

def record_audio(sec,sampling_rate):
	audio = pyaudio.PyAudio()
	stream = audio.open(format=au_format, channels=no_channels,
		rate=sampling_rate, input=True,
		frames_per_buffer=chunk)
	print "Recording..."
	frames = []
	for i in range(0, int(sampling_rate / chunk * sec)):
    		data = stream.read(chunk)
    		frames.append(data)
	print "Finished recording.\n"
	stream.stop_stream()
	stream.close()
	audio.terminate()
	file_name = 'file_'+str(datetime.datetime.now()).replace(" ", "_").replace(":", "_").replace(".", "_")+'.wav'
	waveFile = wave.open(file_name, 'wb')
	waveFile.setnchannels(no_channels)
	waveFile.setsampwidth(audio.get_sample_size(au_format))
	waveFile.setframerate(sampling_rate)
	waveFile.writeframes(b''.join(frames))
	waveFile.close()

def play_audio(path):
	wf = wave.open(path, 'rb')
	audio = pyaudio.PyAudio()
	stream = audio.open(format=audio.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
	data = wf.readframes(chunk)
	while data != '':
		stream.write(data)
		data = wf.readframes(chunk)
	stream.stop_stream()
	stream.close()
	audio.terminate()
	print "\n"

def read_file_for_noise_cancelation(path):
	y, sr = librosa.load(path)
	return y, sr

def reduce_noise_centroid_simple(y, sr):
	cent = librosa.feature.spectral_centroid(y=y, sr=sr)
	threshold_h = np.max(cent)
	threshold_l = np.min(cent)
	less_noise = AudioEffectsChain().lowshelf(gain=-12.0, frequency=threshold_l, slope=0.5).highshelf(gain=-12.0, frequency=threshold_h, slope=0.5).limiter(gain=6.0)
	y_cleaned = less_noise(y)
	return y_cleaned

def reduce_noise_centroid_bass_boost(y, sr):
	cent = librosa.feature.spectral_centroid(y=y, sr=sr)
	threshold_h = np.max(cent)
	threshold_l = np.min(cent)
	less_noise = AudioEffectsChain().lowshelf(gain=-30.0, frequency=threshold_l, slope=0.5).highshelf(gain=-30.0, frequency=threshold_h, slope=0.5).limiter(gain=10.0)
        #less_noise = AudioEffectsChain().lowpass(frequency=threshold_h).highpass(frequency=threshold_l)
	y_cleaned = less_noise(y)
	cent_cleaned = librosa.feature.spectral_centroid(y=y_cleaned, sr=sr)
	columns, rows = cent_cleaned.shape
	boost_h = math.floor(rows/3*2)
	boost_l = math.floor(rows/6)
	boost = math.floor(rows/3)
        #boost_bass = AudioEffectsChain().lowshelf(gain=20.0, frequency=boost, slope=0.8)
	boost_bass = AudioEffectsChain().lowshelf(gain=16.0, frequency=boost_h, slope=0.5)#.lowshelf(gain=-20.0, frequency=boost_l, slope=0.8)
	y_clean_boosted = boost_bass(y_cleaned)
	return y_clean_boosted

def trim_silence(y):
	y_trimmed, index = librosa.effects.trim(y, top_db=20, frame_length=2, hop_length=500)
	trimmed_length = librosa.get_duration(y) - librosa.get_duration(y_trimmed)
	return y_trimmed, trimmed_length

def mfcc_extract(path):
	(rate,sig) = wav.read(path)
	mfcc_feat = mfcc(sig,rate)
	fbank_feat = logfbank(sig,rate)
	print(fbank_feat[1:3,:])

def output_file(destination ,filename, y, sr, ext=""):
    	destination = destination + filename[:-4] + ext + '.wav'
	librosa.output.write_wav(destination, y, sr)
	

while(True):
	choice = input("\n1.Record audio \n2.Get audio from device\n3.Play audio.\n4.Noise reduction.\n5.MFCC extraction.\n6.Exit.\nEnter choice: ")
	if(choice == 1):
		sec = input("Enter number of sec to record: ")
		sampling_rate = input("Enter sampling rate: ")
		record_audio(sec,sampling_rate)
	if(choice == 2):
		path = raw_input("Enter path to wav file: ")
	if(choice == 3):
		path = raw_input("Enter path to wav file: ")
		play_audio(path)
	if(choice == 4):
		filename = raw_input("Enter wav filename: ")
		y, sr = read_file_for_noise_cancelation(filename)
		print "\nAudio time series: "+ str(y) + "\nSampling rate: " + str(sr)
		y_reduced_centroid_s = reduce_noise_centroid_simple(y, sr)
		y_reduced_centroid_mb = reduce_noise_centroid_bass_boost(y, sr)
		y_reduced_centroid_s, time_trimmed = trim_silence(y_reduced_centroid_s)
		print (time_trimmed)
		y_reduced_centroid_mb, time_trimmed = trim_silence(y_reduced_centroid_mb)
		print (time_trimmed)
		output_file('noise_cleaned_samples/' ,filename, y_reduced_centroid_s, sr, '_ctr_s')
		output_file('noise_cleaned_samples/' ,filename, y_reduced_centroid_mb, sr, '_ctr_bb')
	if(choice == 5):
		path = raw_input("Enter path to cleaned wav file: ")
		mfcc_extract(path)
	if(choice == 6):
		exit(0)
	

