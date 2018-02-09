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

def noise_reduction():
	waveFile = wave.open(path, 'rb')
	audio = pyaudio.PyAudio()
	stream = audio.open(format=audio.get_format_from_width(waveFile.getsampwidth()),
                channels=waveFile.getnchannels(),
                rate=waveFile.getframerate())
	data = waveFile.readframes(chunk)
	while data != '':
		data = waveFile.readframes(chunk)
		#process audio//
	stream.stop_stream()
	stream.close()
	audio.terminate()
	

while(True):
	choice = input("1.Record audio \n2.Get audio from device\n3.Play audio.\n4.Exit.\nEnter choice: ")
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
		exit(0)
	

