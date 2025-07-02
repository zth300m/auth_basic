import json
from utils import hash_password, load_config, save_hashed_config, CONFIG_FILE, HASHED_CONFIG_FILE

def main():
    config = load_config()

    hashed_data = {}
    hashed_data['auth'] = {}

    users = config['auth']['users']

    hashed_passwords_list = []
    usernames_list = []

    for user_data in users:
        username = user_data['username']
        password = user_data['password']
        hashed_password = hash_password(password)
        hashed_passwords_list.append(hashed_password)
        usernames_list.append(username)
        print(f"Hashing password for user '{username}': Hashed={hashed_passwords_list[-1]}")

    hashed_data['auth']['usernames'] = usernames_list
    hashed_data['auth']['hashed_passwords'] = hashed_passwords_list

    save_hashed_config(hashed_data)
    print("Hashed passwords saved to hashed_config.json")

if __name__ == "__main__":
    main()
