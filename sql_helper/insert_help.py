"""
SQL INSERT elemző (Tkinteres GUI)

A program célja a hosszú vagy bonyolult INSERT utasítások értelmezésének megkönnyítése.

Ez a program egy egyszerű grafikus felületet biztosít, amelybe a felhasználó beilleszthet egy SQL INSERT utasítást.
Ha a felhasználó a kurzort egy mezőnévre (pl. `name`) helyezi az SQL szövegben, a program automatikusan
kiemeli a mezőhöz tartozó értéket a VALUES záradékból (pl. `'Alice'`).
"""
import tkinter as tk
import re


def extract_fields_and_values(sql_text):
    """
    Kinyeri a mezőneveket és a hozzájuk tartozó értékeket egy SQL INSERT utasításból.

    Feltételezi, hogy az SQL utasítás így néz ki:
    INSERT INTO table (field1, field2, ...) VALUES (value1, value2, ...);
    A string típusú értékeket figyelembe veszi idézőjelek alapján,
    és nem darabolja fel azokat vessző mentén.
    """
    field_match = re.search(r"\((.*?)\)\s*VALUES", sql_text, re.IGNORECASE | re.DOTALL)
    value_match = re.search(r"VALUES\s*\((.*?)\)", sql_text, re.IGNORECASE | re.DOTALL)

    if not field_match or not value_match:
        return [], []

    fields = [f.strip() for f in field_match.group(1).split(",")]
    raw_values = value_match.group(1)

    # okos szétválasztás vessző mentén, figyelembe véve aposztrófot
    values = []
    current = ''
    in_string = False
    for char in raw_values:
        if char == "'" and (not current or current[-1] != "\\"):
            in_string = not in_string
        if char == ',' and not in_string:
            values.append(current.strip())
            current = ''
        else:
            current += char
    if current:
        values.append(current.strip())

    return fields, values

def find_value_position(sql, raw_values, value_index):
    # Find the start position of the VALUES clause
    values_start = sql.lower().find("values")
    if values_start == -1:
        return None, None
    paren_start = sql.find("(", values_start)
    if paren_start == -1:
        return None, None
    # Now, walk through raw_values to find the N-th value's position
    pos_in_sql = paren_start + 1
    in_string = False
    current_index = 0
    value_start = pos_in_sql
    for i, char in enumerate(raw_values):
        if char == "'" and (i == 0 or raw_values[i-1] != "\\"):
            in_string = not in_string
        if char == ',' and not in_string:
            if current_index == value_index:
                value_end = pos_in_sql
                return value_start, value_end
            current_index += 1
            value_start = pos_in_sql + 1
        pos_in_sql += 1
    # Last value
    if current_index == value_index:
        value_end = pos_in_sql
        return value_start, value_end
    return None, None

def on_cursor_move(event):
    cursor_index = text.index(tk.INSERT)
    cnt = text.count("1.0", cursor_index, "chars")
    if cnt is None:
        return
    cursor_pos = text.count("1.0", cursor_index, "chars")[0]
    sql = text.get("1.0", tk.END)

    fields, values = extract_fields_and_values(sql)
    if len(fields) != len(values):
        return

    for field in fields:
        start = sql.find(field)
        end = start + len(field)
        if start <= cursor_pos <= end:
            field_index = fields.index(field)
            # Find raw VALUES part
            value_match = re.search(r"VALUES\s*\((.*?)\)", sql, re.IGNORECASE | re.DOTALL)
            if not value_match:
                return
            raw_values = value_match.group(1)
            value_start, value_end = find_value_position(sql, raw_values, field_index)
            if value_start is not None and value_end is not None:
                start_index = f"1.0 + {value_start}c"
                end_index = f"1.0 + {value_end}c"
                text.tag_remove("highlight", "1.0", tk.END)
                text.tag_add("highlight", start_index, end_index)
                text.tag_config("highlight", background="yellow")
            return
    text.tag_remove("highlight", "1.0", tk.END)


root = tk.Tk()
root.title("SQL INSERT segítő")

text = tk.Text(root, wrap=tk.WORD, width=100, height=20, font=("Courier New", 11))
text.pack(padx=10, pady=10)

text.bind("<KeyRelease>", on_cursor_move)
text.bind("<ButtonRelease>", on_cursor_move)

root.mainloop()
