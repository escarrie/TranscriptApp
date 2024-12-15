import tkinter as tk

from tkinter import ttk, filedialog
from src.Config import Config
from src.AudioConverter import AudioConverter
from src.Transcripter import Transcripter

class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.config = Config()

    def page_transcrire(self):
        if hasattr(self, 'config_frame') and self.config_frame:
            self.config_frame.destroy()

        self.window.title("Page Transcrire")

        # Dernier texte transcrit
        self.text_frame = tk.Frame(self.window, borderwidth=2, relief="groove")
        self.text_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.label_text = tk.Label(self.text_frame, text="DERNIER TEXT TRANSCRIT")
        self.label_text.pack(fill="both", expand=True)

        # Options de sélection
        self.transcript_frame = tk.Frame(self.window, borderwidth=2, relief="groove")
        self.transcript_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.model_label = tk.Label(self.transcript_frame, text="Modèle")
        self.model_label.pack(pady=5)
        self.model_var = tk.StringVar(value="tiny")
        self.model_dropdown = ttk.Combobox(self.transcript_frame, textvariable=self.model_var, values=["tiny", "base", "small", "medium", "large", "turbo"], state="readonly")
        self.model_dropdown.pack(pady=5)

        self.file_button = tk.Button(self.transcript_frame, text="Fichier", command=self.select_file)
        self.file_button.pack(pady=5)

        self.time_indicator_var = tk.BooleanVar()
        self.time_indicator_checkbox = tk.Checkbutton(self.transcript_frame, text="Indicateur de temps", variable=self.time_indicator_var)
        self.time_indicator_checkbox.pack(pady=5)

        self.speaker_indicator_var = tk.BooleanVar()
        self.speaker_indicator_checkbox = tk.Checkbutton(self.transcript_frame, text="Indicateur de Speaker", variable=self.speaker_indicator_var)
        self.speaker_indicator_checkbox.pack(pady=5)

        # Boutons Annuler et Transcrire
        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.cancel_button = tk.Button(self.buttons_frame, text="ANNULER", command=self.window.quit)
        self.cancel_button.pack(side="left", padx=5)

        self.transcribe_button = tk.Button(self.buttons_frame, text="TRANSCRIRE", command=self.transcribe_action)
        self.transcribe_button.pack(side="right", padx=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(title="Sélectionner un fichier audio", filetypes=[
            ("Fichiers audio", "*.m4a *.mp3 *.wav *.flac *.aac *.ogg *.wma *.amr *.aiff *.aif"),
            ("Tous les fichiers", "*.*")
        ])
        if file_path:
            self.file_path = file_path

    def transcribe_action(self):
        model = self.model_var.get()
        with_time = self.time_indicator_var.get()
        with_speaker = self.speaker_indicator_var.get()
        converter = AudioConverter(self.file_path)
        audio_file = converter.convert_file()
        # Transcrire le fichier audio
        transcripter = Transcripter(audio_file, "transcript.txt", model_size=model, with_time=with_time, with_speaker=with_speaker)
        output_path = transcripter.transcript()
        print(output_path)

    def page_config(self):
        if hasattr(self, 'transcript_frame') and self.transcript_frame:
            self.transcript_frame.destroy()

        self.window.title("Page Config")

        # Configuration des identifiants
        self.config_frame = tk.Frame(self.window, borderwidth=2, relief="groove")
        self.config_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # IDENTIFIANT
        id = self.config.get_config("id")
        value = tk.StringVar()
        value.set(id)

        self.label_id = tk.Label(self.config_frame, text="IDENTIFIANT-LOGICIEL")
        self.label_id.pack(anchor="w", pady=5)
        self.entry_id = tk.Entry(self.config_frame, textvariable=value, state="readonly")
        self.entry_id.pack(fill="x", pady=5)

        # API KEY
        self.label_api_key = tk.Label(self.config_frame, text="LOGICIEL KEY")
        self.label_api_key.pack(anchor="w", pady=5)
        self.entry_api_key = tk.Entry(self.config_frame)
        self.entry_api_key.pack(fill="x", pady=5)

        self.validate_button = tk.Button(self.config_frame, text="VALIDER", command=self.validate_config)
        self.validate_button.pack(pady=10)

    def check_config(self):
        if not self.config.get_config("key") or not self.config.validate_api_key() or not self.config.validate_hidden_file():
            self.page_config()
        else:
            self.page_transcrire()

    def run(self):
        self.check_config()
        self.window.mainloop()

    def validate_config(self):
        api_key = self.entry_api_key.get()
        print(api_key)
        self.config.set_config("key", api_key)
        if (self.config.validate_api_key()):
            self.page_transcrire()
