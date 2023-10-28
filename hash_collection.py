#!/usr/bin/python3

"""
The script serves as a tool for collecting and managing SAM hashes, separating the username and NTLM hash.
Users can input SAM hashes multiple times, and the script maintains a JSON format database.
It checks for existing hashes and associated usernames, appending new usernames to existing hashes.
The script provides options to display current entries, appends unique entries to a JSON file upon exit,
and allows users to create a text file containing all hashes and usernames.

Key Features:
1. SAM Hash Collection: Accepts user input of SAM hashes, separating and storing the username and NTLM hash.
2. Dynamic Database: Supports multiple script runs, checking and updating entries in a JSON format database.
3. Data Validation: Verifies the existence of hashes and associated usernames before appending new data.
4. User Interaction: Offers options to display current entries, facilitating user awareness of stored data.
5. Persistent Storage: Appends unique entries to a JSON file when exiting the script.
6. Export Option: Allows users to create a text file containing all hashes and associated usernames.

This script provides a convenient and user-friendly way to manage SAM hashes,
ensuring data integrity and offering flexibility for future expansions or use cases.
"""

import json
import os


def enter_hash():
    data = {}
    while True:
        answer = input("\nProvide a hash\n,"
                       "'Show' for printing the current hashes and user\n"
                       "'Exit' for quiting\n"
                       "'Create' for file with all credentials:\n\n")

        try:
            if answer.lower() == "show":
                print()
                for k, v in data.items():
                    print(f"{k} - {', '.join(name for name in v)}")
            elif answer.lower() == "exit":
                if data:
                    writing_hash_to_db(data)
                break
            elif answer.lower() == "create":
                with open("all_hashes.json", "r") as file:
                    current_db = json.load(file)

                with open("credentials.txt", "w") as f:
                    for k, v in current_db.items():
                        row = f"{k} - {', '.join(name for name in v)}" + "\n"
                        f.write(row)
                print("\n[+] Your file 'credentials.txt' is ready!")
                break
            else:
                username, ntlm = separate_hash(answer)
                collecting_data(data, username, ntlm)
        except IndexError:
            pass


def separate_hash(hash_id):
    """Will separate the hash and the username"""
    results = hash_id.split(":", maxsplit=2)
    username = results[0]
    ntlm = results[2].rstrip(":::")

    return username, ntlm


def collecting_data(data, user, hash_usr):
    """Check hashes and usernames"""
    if hash_usr not in data:
        data[hash_usr] = []
    if user not in data[hash_usr]:
        data[hash_usr].append(user)


def writing_hash_to_db(obj):
    """Writing the credentials to a json file"""
    json_file = "all_hashes.json"
    existing_data = {}
    if os.path.exists(json_file):
        with open(json_file, "r") as file:
            existing_data = json.load(file)

    if not existing_data:
        with open(json_file, "w") as file:
            json.dump(obj, file)
    else:
        for hash_id, usernames in obj.items():
            if hash_id in existing_data:
                value = existing_data[hash_id]
                for item in usernames:
                    if item not in value:
                        existing_data[hash_id].append(item)
            else:
                existing_data[hash_id] = usernames

        with open(json_file, "w") as file:
            json.dump(existing_data, file)

    print("\n[!] Data written to 'all_hashes.json'.")


if __name__ == "__main__":
    enter_hash()
