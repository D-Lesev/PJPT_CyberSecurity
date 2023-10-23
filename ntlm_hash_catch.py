#!/usr/bin/python3

"""
This is simple tool, which can extract users and user's NTLM hashes
From running secretsdump.py. This tool replace the usage of some hand matching users + passwords
Or running Excell to match the proper user + password.
During running, it creates few files in order to combine all users with the proper password.
In a given moment you must supply the script with the cracked password and credentials.
This was tested with hashcat.
After supplying the script, it will generate a file with the proper user and its password.
Finally, it will remove all other files it creates during running the script.
Feel free to make the script better.
"""

import re
import argparse
import os


def get_argument():
    """
    We specify the argument for the file we will add to the script
    """
    parser = argparse.ArgumentParser(description="Getting NTLM hashes from secretsdump.py")
    parser.add_argument("-f", "--file", dest="text_file", help="Fill the text file with the NTLM hashes")

    file_hashes = parser.parse_args()

    if not file_hashes.text_file:
        parser.error("[-] Provide the text file with the hashes")

    return file_hashes


def placing_passwd(pswd_input):
    dict_usr_psw = {}
    with open("usr_psw.txt", "r") as f:
        content = f.readlines()
        # for row in content:
        #     usr = row.split(" ")[0]
        #     psw = row.split(" ")[1].rstrip()
        #     dict_usr_psw[usr] = psw

        dict_usr_psw = {row.split()[0]: row.split()[1].rstrip() for row in content}

    end_result = {}
    for row in pswd_input:
        hash_psw = row.split(":")
        for k, v in dict_usr_psw.items():
            if hash_psw[0] in v:
                if len(hash_psw) == 2:
                    end_result[k] = hash_psw[1]

    return end_result


def writing_end_file(results):
    with open("credentials.txt", "w") as f:
        for k, v in results.items():
            f.write(f"{k} -> {v}\n")

    print("[+] File 'credentials.txt' is created.\nDecrypted password and usernames are inside.")


def writing_usr_psw(dict_input):
    with open("usr_psw.txt", "w") as f:
        f.write("\n".join(f"{k} {v}" for k, v in dict_input.items()))
        # for k, v in dict_input.items():
        #     usr = k
        #     ntlm_hash = v
        #     f.write(f"{usr} {ntlm_hash}\n")
    print("[+] Done writing full file!")


def writing_nt_hash(ntlm_hash):
    nt_hash = ntlm_hash.split(":")[1]

    with open("nt_hashes.txt", "a") as f:
        f.write(nt_hash + "\n")


def separate_hash(hashes):
    usr_no_psw = {

    }

    for hash in hashes:
        result = hash.split(":", maxsplit=2)
        user = result[0]
        ntlm_hash = result[2].rstrip(":::")

        if user not in usr_no_psw:
            usr_no_psw[user] = ntlm_hash

        writing_nt_hash(ntlm_hash)
    writing_usr_psw(usr_no_psw)

    print("[+] Separating hash: Done!")


def get_clean_hash(file):
    with open(file, "r") as f:
        text = f.read()

    pattern_match_hashes = r"(.+NTDS.DIT secrets)(.+)(\[\*\].+)"
    pattern_clean_hashes = r"(.+:::$)"

    matches = re.search(pattern_match_hashes, text, re.S)

    if matches:
        user_hash = matches.group(2).strip()

        possible_matches = re.findall(pattern_clean_hashes, user_hash, re.MULTILINE)
        separate_hash(possible_matches)


def main():
    total_result = []
    file = get_argument()

    get_clean_hash(file.text_file)
    print("[!] Use file 'nt_hashes.txt' in cracking tool to decrypt the hashes.")
    print("[!] Enter the result from cracking tool along with the hash nad password")
    while True:
        result = input()
        if not result:
            break
        total_result.append(result)

    writing_end_file(placing_passwd(total_result))

    if os.path.exists("usr_psw.txt"):
        os.remove("usr_psw.txt")
    if os.path.exists("nt_hashes.txt"):
        os.remove("nt_hashes.txt")


main()
