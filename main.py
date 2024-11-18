import os
import re
import hashlib
import platform
from tqdm import tqdm
from colorama import Fore, init

init(autoreset=True) # Inicializar colorama

def clear():
    os.system('cls' if platform.system() == 'Windows' else 'clear')

def calc_file_hash(file_path):
    sha256 = hashlib.sha256() # Hash del archivo
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
    except (PermissionError, OSError):
        print(f"{Fore.RED}[WARNING]{Fore.RESET} Could not read '{file_path}'")
        return None # No analizar archivos ilegibles
    return sha256.hexdigest()

def is_valid_path(path): # Verifica la validez de la ruta para cada sistema operativo
    current_os = platform.system() # Sistema operativo

    if current_os == 'Windows':
        if re.match(r'^[a-zA-Z]:\\|^\\\\', path):
            return True
        else:
            clear()
            print(f"{Fore.RED}[ERROR]{Fore.RESET} The path isn't valid for Windows systems " + r"(C:\Users\user)")
            return False
    elif current_os == 'Linux':
        if path.startswith("/"):
            return True
        else:
            clear()
            print(f"{Fore.RED}[ERROR]{Fore.RESET} The path isn't valid for Linux systems (/home/user/)")
            return False
    else:
        clear()
        print(f"{Fore.RED}[ERROR]{Fore.RESET} Unsupported operating system.")

# Encontrar duplicados a partir del hash
def find_dups(root_dir):
    hashes = {}
    total_files = sum(len(files) for _, _, files in os.walk(root_dir))

    with tqdm(total=total_files, desc="Processing files", unit=" files") as pbar:
        for root, _, files in os.walk(root_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if os.path.isfile(file_path): # Verificar validez del archivo
                    file_hash = calc_file_hash(file_path)
                    if file_hash:
                        hashes.setdefault(file_hash, []).append(file_path)
                pbar.update(1) # Actualización barra de progreso

    # Archivos duplicados
    dups = {hash_val: paths for hash_val, paths in hashes.items() if len(paths) > 1}
    if dups:
        print("Duplicate files found:")
        for hash_val, paths in dups.items():
            print(f"   Hash: {hash_val}")
            for path in paths:
                print(f"      - {Fore.GREEN}{path}{Fore.RESET}")
    else:
        print("No duplicate files found")

if __name__ == '__main__':
    while True:
        root_directory = input("Enter the absolute path of the directory you want to analyse: ")
        if is_valid_path(root_directory):
            if os.path.isdir(root_directory):
                break
            else:
                clear()
                print(f"{Fore.RED}[ERROR]{Fore.RESET} The path isn't a valid directory")
    
    find_dups(root_directory)