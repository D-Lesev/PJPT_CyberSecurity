#!/usr/bin/python3

"""
This script will collect all hashes and try to make them unique.
It will collect each hash with the proper username.
"""


def enter_hash():
    data = {}
    while True:
        answer = input("\n[!] Provide a hash,\n"
                       "or enter 'Show' for printing the current hashes and user\n"
                       "or enter 'exit' for quiting:\n\n")

        if answer.lower() == "show":
            print()
            for k, v in data.items():
                print(f"{k} - {', '.join(name for name in v)}")
        elif answer.lower() == "exit":
            writing_hash_to_file(data)
            break
        else:
            username, ntlm = separate_hash(answer)
            collecting_data(data, username, ntlm)


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


def writing_hash_to_file(obj):
    """Writing the credentials to a file"""
    with open("all_hashes.txt", "w") as file:
        for k, v in obj.items():
            row = f"{k} - {', '.join(name for name in v)}" + "\n"
            file.write(row)
    print("\n[!] File with name 'all_hashes.txt' is created.")


if __name__ == "__main__":
    enter_hash()
