import sys
import os

from src.AudioConverter import AudioConverter
from src.Transcripter import Transcripter
from src.Interface import Interface
from src.Config import Config

def main(
    audio_file,
    output_file,
    model,
    with_time=False,
    with_speaker=False,
    remove_original=False
):
    # Convertir le fichier audio en .wav
    converter = AudioConverter(audio_file)
    audio_file = converter.convert_file()
    # Transcrire le fichier audio
    transcripter = Transcripter(audio_file, output_file, model_size=model, with_time=with_time, with_speaker=with_speaker, remove_original=remove_original)
    output_path = transcripter.transcript()
    return output_path

if __name__ == "__main__":
    args = sys.argv
    if args[1] == "-h" or args[1] == "--help":
        print("Usage: python main.py <audio_file> <output_file> <model>")
        print("\nOptions:")
        print("\t--help, -h\t\tShow this help message.")
        print("\t--with-time\t\tAdd the start and end time of each segment.")
        print("\t--with-speaker\t\tAdd the speaker's name if known for each segment.")
        print("\t--remove-original-file\t\tDelete the original audio file after transcription.")
        sys.exit(0)
    elif args[1] == "--version" or args[1] == "-v":
        print("1.0.0")
        sys.exit(0)
    elif args[1] == "--list-models":
        print("Supported models: base, small, medium, large")
        sys.exit(0)
    elif args[1] == "--interface" or args[1] == "-i":
        interface = Interface()
        interface.run()
    elif len(args) < 4:
        print("Usage: python main.py <audio_file> <output_file> <model>")
        sys.exit(1)
    elif not os.path.exists(args[1]):
        print(f"Le fichier {args[1]} n'existe pas.")
        sys.exit(1)
    else:
        with_time = "--with-time" in args
        with_speaker = "--with-speaker" in args
        remove_original_file = "--remove-original-file" in args

        output_path = main(args[1], args[2], args[3], with_time=with_time, with_speaker=with_speaker, remove_original=remove_original_file)