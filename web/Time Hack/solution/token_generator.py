import time, hashlib

def generate_token(username: str) -> str:
    token = hashlib.md5(username.encode()).hexdigest() + "-" + str(int(time.time()))
    return token


with open("tokens.txt", "a") as fw:
    tokens = set()
    for i in range(1000):
        token = generate_token("admin")
        if token in tokens : continue
        tokens.add(token)
        fw.write(f"{token}\n")
        time.sleep(0.7)
    
