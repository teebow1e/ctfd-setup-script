import requests
import json
import os

from util import *

USERNAME = "admin"
PASSWORD = "admin"

URL = "http://192.168.194.130"

def main():
    s = requests.Session()
    r = s.get(URL)
    m = CSRF_REGEX.search(r.content.decode())
    csrf_token = m.group(1)
    if csrf_token:
        print("[+] Found CSRF token")
    else:
        print("[+] CSRF token not found or can not be parsed")
        os._exit(1)

    # Authenticate as admin
    login_data = {
        "name": USERNAME,
        "password": PASSWORD,
        "_submit": "Submit",
        "nonce": csrf_token
    }

    login_phase = s.post(URL + "/login", data=login_data, allow_redirects=False)
    if login_phase.status_code == 302:
        print("[+] Login success")
    else:
        print(f"[?] Received abnormal status code {login_phase.status_code}")
        os._exit(1)

    check_authentication = s.get(URL + '/api/v1/users/me')
    current_user_data = json.loads(check_authentication.content.decode())
    if current_user_data.get('data').get('name') == USERNAME:
        print("[+] Authentication success")
    else:
        print("[-] Something probably gone wrong..")
        os._exit(1)

    # Get the CSRF token one more time..
    x = s.get(URL)
    csrf_token2 = CSRF_REGEX.search(x.content.decode()).group(1)

    csrf_header = {
        'CSRF-Token': csrf_token2,
    }

    # Create challenge
    chall_data = {
        "name":"chall_name",
        "category":"sample_category",
        "state":"hidden",
        "value":"100",
        "type":"standard",
        "description":"This is a description"
    }

    r = s.post(URL + '/api/v1/challenges', headers=csrf_header, json=chall_data)
    print("[!] Create challenge result: " + r.content.decode())
    chall_data_dict = json.loads(r.content.decode())
    chall_id = chall_data_dict.get("data").get("id")

    # Add flag to previously-created challenge
    flag_data = {
        "challenge": chall_id,
        "content": "FLAG{flag_here}",
        "type":"static"
    }
    r = s.post(URL + '/api/v1/flags', headers=csrf_header, json=flag_data)
    print("[!] Add flag result: " + r.content.decode())

    # Add attachment to previously-created challenge
    file_chall_data = {
        'nonce': csrf_token2,
        'challenge': chall_id,
        'type': 'challenge',
    }
    files = {
        'file': ('sample.txt', 'This is sample, nothing here'),
        # 'file': ('file.txt', open('file', 'rb'))
    }
    r = s.post(URL + '/api/v1/files', data=file_chall_data, files=files)
    print("[!] Add file result: " + r.content.decode())

    # Change previously-created challenge status to visible
    visible_dict = {
        'state': 'visible',
    }
    r = s.patch(URL + f'/api/v1/challenges/{chall_id}', headers=csrf_header, json=visible_dict)
    print("[!] Change visible result: " + r.content.decode())

if __name__ == "__main__":
    main()
