from scipy.io import wavfile
import scipy.signal as signal
import matplotlib.pyplot as plt
import librosa
import soundfile as sf
import numpy as np

# constants
window_length = 51
polyorder = 3
STD_n = 0.001


def get_spectrogram(filename):
  audio, sr = librosa.load(filename, sr = None)

  window_size = 1024  # Size of the window for the STFT
  hop_length = int(window_size / 4)  # Hop size between consecutive windows
  n_fft = window_size


  spectrogram = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length, window=signal.hann(window_size))
  spectrogram_db = librosa.amplitude_to_db(np.abs(spectrogram), ref=np.max)


  # Plot the spectrogram
  plt.figure(figsize=(12, 5))
  librosa.display.specshow(spectrogram_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log') 
  plt.colorbar(format='%+2.0f dB')
  plt.title('Spectrogram')
  plt.xlabel('Time')
  plt.ylabel('Frequency')
  return plt

def savgol_filter(filename = 'audios/main.wav'):
  sample_rate, data = wavfile.read(filename)
  data = data.astype(float)


  filtered_data = signal.savgol_filter(data, window_length, polyorder)

  filtered_data = filtered_data.astype('int16')
  wavfile.write('audios/main_filtered_via_savgol_filter.wav', sample_rate, filtered_data)

  # Wiener filter
  sample_rate, data = wavfile.read(filename)
  data = data.astype(float)

  filtered_data = signal.wiener(data)

  filtered_data = filtered_data.astype('int16')
  wavfile.write('audios/main_filtered_via_wiener.wav', sample_rate, filtered_data)


  spectrogram_original = get_spectrogram("audios/main.wav")
  spectrogram_original.savefig('spectrograms/spectrogram_original.png')


  spectrogram_savgol_filter = get_spectrogram("audios/main_filtered_via_savgol_filter.wav")
  spectrogram_savgol_filter.savefig('spectrograms/spectrogram_savgol_filter.png')


  spectrogram_wiener = get_spectrogram("audios/main_filtered_via_wiener.wav")
  spectrogram_wiener.savefig("spectrograms/spectrogram_wiener.png")

def add_noise():
  # Add noise to audiofile
  audio, sr = librosa.load('audios/main.wav', sr = None)
  RMS = np.sqrt(np.mean(audio**2))
  noise = np.random.normal(0, STD_n, audio.shape[0])
  audio_noise = audio + noise
  sf.write('audios/main_mono_with_noise.wav', audio_noise, sr)

def noise_filter():
  # Savgol filter for noise audiofilez
  sample_rate, data = wavfile.read('audios/main_mono_with_noise.wav')
  data = data.astype(float)

  filtered_data = signal.savgol_filter(data, window_length, polyorder)
  filtered_data = filtered_data.astype('int16')

  wavfile.write('audios/main_mono_with_noise_via_savgol_filter.wav', sample_rate, filtered_data)


  spectrogram_noise = get_spectrogram("audios/main_mono_with_noise.wav")
  spectrogram_noise.savefig("spectrograms/spectrogram_noise.png")


  spectrogram_noise_via_savgol = get_spectrogram("audios/main_mono_with_noise_via_savgol_filter.wav")
  spectrogram_noise_via_savgol.savefig("spectrograms/spectrogram_noise_via_savgol.png")