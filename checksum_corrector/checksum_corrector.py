"""
Generates SQL update commands to correct checksums in a database changelog based on an error log file.
PLace the log into 'error_log.txt' and run the script to produce 'update_commands.sql'.
"""

def read_error_log_file(filename: str) -> list[str]:
    with open(filename, 'r', encoding='utf-8') as f:
        # read lines containing"but is now:"
        lines = [line.strip() for line in f.readlines() if 'but is now:' in line]
    return lines


def gen_update_commands_to_file(log: object, param: object) -> None:
    """Generates SQL update commands to correct checksums in a database changelog.
    :param log: List of error log lines.
    :param param: Output filename for the SQL commands.
    """
    with open(param, 'w', encoding='utf-8') as f:
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
