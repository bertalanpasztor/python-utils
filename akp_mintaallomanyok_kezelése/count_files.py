"""
Számolja és kiírja az adott könyvtár közvetlen alkönyvtáraiban található fájlok számát (rekurzívan).
"""
import os

def count_files_in_dir(path: str) -> int:
    """Visszaadja az adott könyvtárban (rekurzívan) található fájlok számát."""
    total = 0
    for _, _, files in os.walk(path):
        total += len(files)
    return total

def list_subdir_file_counts(base_path: str):
    """Kiírja az adott útvonal közvetlen alkönyvtáraiban lévő (rekurzív) fájlszámot."""
    for entry in os.scandir(base_path):
        if entry.is_dir():
            count = count_files_in_dir(entry.path)
            print(f"{entry.name}: {count} fájl")


if __name__ == "__main__":
    path = 'c:/GIT/AKP/data-file-notifier-python/akpdir/KEREKPAR'
    if not os.path.exists(path):
        print("Hiba: Az útvonal nem létezik.")
    else:
        list_subdir_file_counts(path)