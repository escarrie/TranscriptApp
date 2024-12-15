import tkinter as tk
from src.Config import Config

class Interface:
    def __init__(self):
        self.window = tk.Tk()
        self.config = Config()

    def page_transcrire(self):
        if hasattr(self, 'config_frame') and self.config_frame:
            self.config_frame.destroy()

        self.window.title("Page Transcrire")

        # Options de sélection
        self.transcript_frame = tk.Frame(self.window, borderwidth=2, relief="groove")
        self.transcript_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        self.model_button = tk.Button(self.transcript_frame, text="Selecteur Model")
        self.model_button.pack(pady=5)

        self.file_button = tk.Button(self.transcript_frame, text="Fichier")
        self.file_button.pack(pady=5)

        # Boutons Annuler et Transcrire
        self.buttons_frame = tk.Frame(self.window)
        self.buttons_frame.grid(row=1, column=1, padx=10, pady=10, sticky="e")

        self.cancel_button = tk.Button(self.buttons_frame, text="ANNULER")
        self.cancel_button.pack(side="left", padx=5)

        self.transcribe_button = tk.Button(self.buttons_frame, text="TRANSCRIRE")
        self.transcribe_button.pack(side="right", padx=5)

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
