import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
import librosa
from scipy.io import wavfile
import soundfile as sf


def get_spectrogram(filename):
  audio, sr = librosa.load(filename, sr = None)

  window_size = 2048  # Size of the window for the STFT
  hop_length = int(window_size / 4)  # Hop size between consecutive windows
  n_fft = window_size


  spectrogram = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length, window=signal.hann(window_size))
  spectrogram_db = librosa.amplitude_to_db(np.abs(spectrogram), ref=np.max)


  # Plot the spectrogram
  plt.figure(figsize=(12, 5))
  librosa.display.specshow(spectrogram_db, sr=sr, hop_length=hop_length, x_axis='time', y_axis='log') 
  plt.colorbar(format='%+2.0f dB')
  plt.title(f'Spectrogram {filename}')
  plt.xlabel('Time')
  plt.ylabel('Frequency')
  return plt

def save_spec(base_filename):
  spectrogram_A = get_spectrogram(f'audios/{base_filename}.wav')
  spectrogram_A.savefig(f'spectrograms/spectrogram_{base_filename}.png')

# spectrogram_A = get_spectrogram('audios/A.wav')
# spectrogram_A.savefig('spectrograms/spectrogram_A.png')

# spectrogram_E = get_spectrogram('audios/E.wav')
# spectrogram_E.savefig('spectrograms/spectrogram_E.png')

# spectrogram_gav = get_spectrogram('audios/gav.wav')
# spectrogram_gav.savefig('spectrograms/spectrogram_gav.png')


def get_min_max_speech_freq(filename):
  audio_data, sample_rate = librosa.load(filename, sr=None, mono=True)
  frequencies = np.fft.rfftfreq(len(audio_data), d=1/sample_rate)
  magnitudes = np.abs(np.fft.rfft(audio_data))
  voice_frequencies = frequencies[np.where(magnitudes > np.mean(magnitudes))]
  min_voice_freq = np.min(voice_frequencies)
  max_voice_freq = np.max(voice_frequencies)
  return int(min_voice_freq), int(max_voice_freq)

def print_max_min_freq(base_filename):
  min_voice_freq, max_voice_freq = get_min_max_speech_freq(f"audios/{base_filename}.wav")
  print(base_filename)
  print("Минимальная частота голоса:", int(min_voice_freq))
  print("Максимальная частота голоса:", int(max_voice_freq))

# min_voice_freq, max_voice_freq = get_min_max_speech_freq("audios/A.wav")
# print('A')
# print("Минимальная частота голоса:", int(min_voice_freq))
# print("Максимальная частота голоса:", int(max_voice_freq))

# min_voice_freq, max_voice_freq = get_min_max_speech_freq("audios/E.wav")
# print('E')
# print("Минимальная частота голоса:", int(min_voice_freq))
# print("Максимальная частота голоса:", int(max_voice_freq))

# min_voice_freq, max_voice_freq = get_min_max_speech_freq("audios/gav.wav")
# print('Gav')
# print("Минимальная частота голоса:", int(min_voice_freq))
# print("Максимальная частота голоса:", int(max_voice_freq))