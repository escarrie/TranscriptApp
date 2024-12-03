from src.AudioConverter import AudioConverter
from src.Transcripter import Transcripter

# Convertir un fichier audio en .wav
audio_converter = AudioConverter("audio.m4a")
audio_path = audio_converter.convert_file()
# Générer la transcription
transcripter = Transcripter(audio_path, "transcription.txt", model_size="base", with_speaker=True, with_time=True)
transcripter.transcript()