import os
import whisper

class Transcripter:
    def __init__(
        self,
        file_path,
        output_path,
        model_size="base",
        with_speaker = False,
        with_time = False,
        remove_original = False
    ):
        self.file_path = file_path
        self.output_path = output_path
        self.model_size = model_size
        self.with_speaker = with_speaker
        self.with_time = with_time
        self.remove_original = remove_original
        self.model = None

    def loadModel(self):
        self.model = whisper.load_model(self.model_size)  # Remplacez "base" par d'autres modèles si besoin (ex: "small", "medium", "large")

    def audioToSegment(self):
        filename = os.path.basename(self.file_path)
        # Transcription avec Whisper
        result = self.model.transcribe(self.file_path, language="fr", fp16=False)
        # Supprimer le fichier audio une fois transcri
        if os.path.exists(self.file_path) and self.remove_original:
            os.remove(self.file_path)
        return result.get("segments", [])

    def segmentsToFile(self, segments = []):
        with open(self.output_path, "w") as text_file:
            for segment in segments:
                if self.with_time and self.with_speaker:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    speaker = segment.get("speaker", "Interlocuteur inconnu")  # Nom d'interlocuteur (ou par défaut "Interlocuteur")
                    text = segment["text"]
                    text_file.write(f"[{speaker}] {start_time:.2f} - {end_time:.2f}: {text}\n")
                elif self.with_time:
                    start_time = segment["start"]
                    end_time = segment["end"]
                    text = segment["text"]
                elif self.with_speaker:
                    speaker = segment.get("speaker", "Interlocuteur inconnu")  # Nom d'interlocuteur (ou par défaut "Interlocuteur")
                    text = segment["text"]
                    text_file.write(f"[{speaker}]: {text}\n")
                else:
                    text = segment["text"]
                    text_file.write(f"{text}\n")
        return self.output_path

    def transcript(self):
        self.loadModel()
        segments = self.audioToSegment()
        return self.segmentsToFile(segments)