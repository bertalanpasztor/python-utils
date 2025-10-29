import os
import zipfile


def extract_and_delete_zips(root_dir, dry_run=False):
    """
    Végigmegy a root_dir alatt, kicsomagolja az összes .zip fájlt az adott mappába,
    azonos nevű fájlokat felülírja, majd törli a zipet.
    dry_run=True esetén csak kiírja, mit csinálna.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for name in filenames:
            if name.lower().endswith(".zip"):
                zip_path = os.path.join(dirpath, name)
                extract_to = dirpath

                print(f"[INFO] Talált zip: {zip_path}")
                try:
                    if dry_run:
                        print(f"[DRY] Kicsomagolás ide: {extract_to} (felülírással)")
                        print(f"[DRY] Zip törlése: {zip_path}")

                    with zipfile.ZipFile(zip_path, 'r') as zf:
                        bad_file = zf.testzip()
                        if bad_file is not None:
                            raise zipfile.BadZipFile(f"Sérült fájl a zipben: {bad_file}")

                        for member in zf.namelist():
                            print(member)
                            # target_path = os.path.join(extract_to, member)

                            # Ha már létezik, töröljük, hogy biztosan felülíródjon
                            # if os.path.exists(target_path):
                            #     if os.path.isdir(target_path):
                            #         # ha mappa, hagyjuk békén
                            #         pass
                            #     else:
                            #         os.remove(target_path)

                            zf.extract(member, extract_to)

                    os.remove(zip_path)
                    print(f"[OK] Kicsomagolva és törölve: {zip_path}")

                except zipfile.BadZipFile as e:
                    print(f"[HIBA] Rossz vagy sérült zip: {zip_path} — {e}")
                except Exception as e:
                    print(f"[HIBA] Nem sikerült feldolgozni: {zip_path} — {e}")


if __name__ == "__main__":
    ROOT = r"c:\GIT\AKP\data-file-notifier-python\akpdir\GEPJARMU\XTX\TDC"

    # Először próba üzemmód
    extract_and_delete_zips(ROOT, dry_run=True)

    # Ha rendben van, futtasd élesben
    # extract_and_delete_zips(ROOT, dry_run=False)