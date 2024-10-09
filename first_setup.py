import requests

from util import *

URL = "hxxp://xxxxxxxxxxxxx"

def main():
    print("[!] starting")

    boundary = "----WebKitFormBoundaryK8QM9WJHvQbABDxk"

    headers = {
        'Content-Type': f'multipart/form-data; boundary={boundary}',
    }

    s = requests.Session()

    r = s.get(URL + '/setup')
    m = CSRF_REGEX.search(r.content.decode())
    csrf_token = m.group(1)
    if csrf_token:
        print("[+] Found CSRF token")

    body = f"""--{boundary}
Content-Disposition: form-data; name="ctf_name"

CTF_TEST
--{boundary}
Content-Disposition: form-data; name="ctf_description"

CTF_TEST
--{boundary}
Content-Disposition: form-data; name="user_mode"

teams
--{boundary}
Content-Disposition: form-data; name="challenge_visibility"

private
--{boundary}
Content-Disposition: form-data; name="account_visibility"

private
--{boundary}
Content-Disposition: form-data; name="score_visibility"

private
--{boundary}
Content-Disposition: form-data; name="registration_visibility"

private
--{boundary}
Content-Disposition: form-data; name="verify_emails"

false
--{boundary}
Content-Disposition: form-data; name="team_size"

4
--{boundary}
Content-Disposition: form-data; name="name"

admin
--{boundary}
Content-Disposition: form-data; name="email"

admin@admin.admin
--{boundary}
Content-Disposition: form-data; name="password"

admin
--{boundary}
Content-Disposition: form-data; name="ctf_logo"; filename=""
Content-Type: application/octet-stream

--{boundary}
Content-Disposition: form-data; name="ctf_banner"; filename=""
Content-Type: application/octet-stream

--{boundary}
Content-Disposition: form-data; name="ctf_small_icon"; filename=""
Content-Type: application/octet-stream

--{boundary}
Content-Disposition: form-data; name="ctf_theme"

core-beta
--{boundary}
Content-Disposition: form-data; name="_submit"

Finish
--{boundary}
Content-Disposition: form-data; name="nonce"

{csrf_token}
--{boundary}--"""

    r = s.post(URL + '/setup', headers=headers, data=body, allow_redirects=False)

    if r.status_code == 302:
        print("[+] Finished setup")

    print("[+] Done")
if __name__ == '__main__':
    main()