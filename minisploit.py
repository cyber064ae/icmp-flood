import cmd
import os
import importlib

class MiniSploit(cmd.Cmd):
    intro = "Welcome to MiniSploit. Type help or ? to list commands.\n"
    prompt = 'minisploit > '

    def do_use(self, module_path):
        """Use a module. Example: use payloads/powershell_reverse_tcp"""
        try:
            parts = module_path.split('/')
            if len(parts) != 2:
                print("[!] Invalid module format. Use: use <category/module>")
                return
            mod_type, mod_name = parts
            full_path = f"core.{mod_type}.{mod_name}"
            mod = importlib.import_module(full_path)
            print(f"[+] Running module: {module_path}\n")
            mod.run()
        except ModuleNotFoundError:
            print(f"[!] Module not found: {module_path}")
        except Exception as e:
            print(f"[!] Error running module: {e}")

    def do_list(self, arg):
        """List available modules"""
        base_path = os.path.join("core")
        print("\nAvailable Modules:\n")
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(".py") and not file.startswith("__"):
                    relative_path = os.path.join(root, file).replace("\\", "/")
                    module_path = relative_path.replace("core/", "").replace(".py", "")
                    print(f"  {module_path}")
        print()

    def do_help(self, arg):
        """Show help"""
        print("""
Available Commands:
  use <module>     Load and run a module (e.g., use payloads/powershell_reverse_tcp)
  list             List available modules
  credits          Show framework credits
  help             Show this help message
  exit             Exit the framework
""")

    def do_credits(self, arg):
        """Show credits"""
        gray = "\033[90m"
        blue = "\033[94m"
        reset = "\033[0m"
        print(f"Developed by: {gray}blt{reset} and {blue}venqus0000{reset}")

    def do_exit(self, arg):
        """Exit the framework"""
        print("Exiting MiniSploit.")
        return True

if __name__ == "__main__":
    MiniSploit().cmdloop()