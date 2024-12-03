from pydub import AudioSegment
import os

class AudioConverter:
    def __init__(self, input_path, remove_original=False):
        self.input_path = input_path
        self.remove_original = remove_original

    def supported_file(self):
        """Vérifier si le fichier audio est supporté."""
        extention = self.input_path.split(".")[-1]
        return extention in ["m4a", "mp3", "wav", "flac", "aac", "ogg", "wma", "amr", "aiff", "aif"]

    def convert_to_wav(self, extention):
        """Convertir un fichier .m4a en .wav et retourner le chemin du fichier .wav."""
        audio = AudioSegment.from_file(self.input_path, format=extention)
        wav_path = os.path.splitext(self.input_path)[0] + ".wav"
        audio.export(wav_path, format="wav")
        if os.path.exists(self.input_path) and self.remove_original:
            os.remove(self.input_path)
        return wav_path

    def convert_file(self):
        """Convertir un fichier audio en .wav si ce n'est pas déjà le cas."""
        extention = self.input_path.split(".")[-1]
        if not self.supported_file():
            raise Exception(f"Le fichier {self.input_path} n'est pas supporté.")
        if extention != "wav":
            return self.convert_to_wav(extention)
        return self.input_path