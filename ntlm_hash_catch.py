#!/usr/bin/python3

import re


def placing_passwd(pswd_input):
    dict_usr_psw = {}
    with open("usr_psw.txt", "r") as f:
        content = f.readlines()
        for row in content:
            usr = row.split(" ")[0]
            psw = row.split(" ")[1].rstrip()
            dict_usr_psw[usr] = psw

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


def writing_usr_psw(dict_input):
    with open("usr_psw.txt", "w") as f:
        for k, v in dict_input.items():
            usr = k
            ntlm_hash = v
            f.write(f"{usr} {ntlm_hash}\n")
    print("Done writing full file")


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

    print("Done")


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
    get_clean_hash("ntlm.txt")
    print("Enter the result from cracking tool:")
    while True:
        result = input()
        if not result:
            break
        total_result.append(result)

    writing_end_file(placing_passwd(total_result))


main()
