import json
import os
import uuid
import random
import string


class Config:
    CONFIG_DIR = "config/"
    CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

    DEFAULT_CONFIG = {
        "id": "",
        "key": "",
        "model": "base"
    }

    def __init__(self):
        self.config = {}
        self._initialize_config()
        print(self.generate_api_key())

    def _initialize_config(self):
        """Ensure configuration directory and file exist, then load the config."""
        os.makedirs(self.CONFIG_DIR, exist_ok=True)
        if not os.path.exists(self.CONFIG_FILE):
            self.reset_config()
        else:
            self._load_config()

    def reset_config(self):
        """Reset configuration to defaults and generate a new ID."""
        self.config = self.DEFAULT_CONFIG.copy()
        self.generate_id()
        self._save_config()
        self._create_hidden_file()

    def _load_config(self):
        """Load the configuration from the file."""
        with open(self.CONFIG_FILE, "r") as file:
            self.config = json.load(file)

    def _save_config(self):
        """Save the current configuration to the file."""
        with open(self.CONFIG_FILE, "w") as file:
            json.dump(self.config, file, indent=4)

    def get_config(self, key):
        """Retrieve a configuration value."""
        return self.config.get(key)

    def set_config(self, key, value):
        """Set a configuration value."""
        self.config[key] = value
        self._save_config()

    def delete_config(self, key):
        """Delete a configuration value."""
        if key in self.config:
            del self.config[key]
            self._save_config()

    def display_config(self):
        """Print the current configuration."""
        print(json.dumps(self.config, indent=4))

    def generate_id(self):
        """Generate a unique ID and save it to the config."""
        self.set_config("id", str(uuid.uuid4()))

    def get_id_number(self):
        """Extract a numeric representation from the ID."""
        try:
            id_hex = self.get_config("id").split("-")[0]
            return str(int(id_hex, 16))
        except (ValueError, AttributeError):
            return ""

    def _create_hidden_file(self):
        """Create a hidden file with the ID and a generated secret."""
        hidden_file = os.path.join(self.CONFIG_DIR, f".{self.get_id_number()}.json")
        secret = self._generate_secret()
        with open(hidden_file, "w") as file:
            json.dump({"id": self.get_config("id"), "secret": secret}, file, indent=4)

    def _generate_secret(self):
        """Generate a secret based on the ID number."""
        id_number = self.get_id_number()
        if not id_number:
            return 0
        id_num_int = int(id_number)
        return (
            (id_num_int % 5) * 555 *
            (id_num_int % 3) * 333 +
            (id_num_int % 7) * 777
        )

    def validate_hidden_file(self):
        """Validate the hidden file's secret."""
        hidden_file = os.path.join(self.CONFIG_DIR, f".{self.get_id_number()}.json")
        if not os.path.exists(hidden_file):
            return False
        with open(hidden_file, "r") as file:
            hidden_data = json.load(file)
        return hidden_data.get("secret") == self._generate_secret() and hidden_data.get("id") == self.get_config("id")

    def validate_api_key(self):
        """Validate the API key based on its structure."""
        api_key = self.get_config("key")
        if not api_key or len(api_key) < 10:
            return False

        secret = str(self._generate_secret())
        id_number = self.get_id_number()
        id_letters = self._convert_digits_to_letters(id_number)
        secret_letters = self._convert_digits_to_letters(secret)

        return (
            secret in api_key and
            id_number in api_key and
            id_letters in api_key and
            secret_letters in api_key
        )

    def generate_api_key(self):
        """Generate and save a new API key."""
        secret = str(self._generate_secret())
        id_number = self.get_id_number()

        random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        id_letters = self._convert_digits_to_letters(id_number)
        secret_letters = self._convert_digits_to_letters(secret)

        api_key = random_chars + secret + id_number + id_letters + secret_letters
        return api_key

    @staticmethod
    def _convert_digits_to_letters(digits):
        """Convert a string of digits into corresponding letters (a-j)."""
        return ''.join(chr(97 + int(digit)) for digit in digits if digit.isdigit())
