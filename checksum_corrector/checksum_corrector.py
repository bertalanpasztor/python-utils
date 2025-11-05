"""
SQL UPDATE parancsokat generál, hogy javítsa az ellenőrzőösszegeket egy adatbázis changelog-ban egy hibalog fájl alapján.
Helyezd a log részletét az 'error_log.txt' fájlba
és futtasd a programot, hogy létrejöjjön az 'update_commands.sql' fájl,
amely tartalmazza a javító SQL parancsokat.
"""

def read_error_log_file(filename: str) -> list[str]:
    """
    Hibalog fájlt olvas be és visszaadja a releváns sorokat egy listában
    :paraméter filename: Hibalog fájl neve.
    :Viszaadott érték: A hibalog releváns sorainak listája.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        # read lines containing"but is now:"
        lines = [line.strip() for line in f.readlines() if 'but is now:' in line]
    return lines


def gen_update_commands_to_file(log: object, output_file: object) -> None:
    """SQL UODATE parancsokat generál, hogy javítsa az ellenőrzőösszegeket egy adatbázis changelog-ban.
    :paraméter log: Hibalog sorok listája.
    :paraméter output_file: Az SQL parancsokat tartalmazó kimeneti fájl neve.
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        for line in log:
            id_parts = line.split('::')
            author = id_parts[2].split(' was:')[0]
            changeset_id = id_parts[1]
            filename = id_parts[0]
            new_checksum = line.split('but is now: ')[1]
            update_command = f"UPDATE DATABASECHANGELOG SET MD5SUM='{new_checksum}' WHERE ID='{changeset_id}' AND AUTHOR='{author}' AND FILENAME='{filename}';\n"
            f.write(update_command)


if __name__ == '__main__':
    errorlog = read_error_log_file('error_log.txt')
    gen_update_commands_to_file(errorlog, 'update_commands.sql')
