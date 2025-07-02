import json
import bcrypt

CONFIG_FILE = 'config.json'
HASHED_CONFIG_FILE = 'hashed_config.json'

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {CONFIG_FILE} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {CONFIG_FILE}.")
        return {}

def load_hashed_config():
    try:
        with open(HASHED_CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: {HASHED_CONFIG_FILE} not found.")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {HASHED_CONFIG_FILE}.")
        return {}

def save_hashed_config(config_data):
    try:
        with open(HASHED_CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
    except IOError as e:
        print(f"Error: Could not write to {HASHED_CONFIG_FILE}. {e}")
