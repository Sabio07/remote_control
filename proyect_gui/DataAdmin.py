import sqlite3
import datetime
import pyautogui
import bcrypt
import json

def query_db(query, parameters = ()):
    conn = sqlite3.connect('userData.db')
    
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    result = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return result

def query_many_db(query, parameters):
    conn = sqlite3.connect('userData.db')

    cursor = conn.cursor()
    cursor.executemany(query, parameters)
    result = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()
    return result

def append_rowDb(table, values=()):
    table_info = query_db(f"PRAGMA table_info({table})")
    # Evitar errores con el número de columnas disponibles
    if table_info[0][1] == "id":
        columns = [row[1] for row in table_info[1:]]
    else:
        columns = [row[1] for row in table_info]
    
    # Validar si la cantidad de valores coincide con la cantidad de columnas
    if len(values) != len(columns):
        raise ValueError("La cantidad de valores no coincide con la cantidad de columnas en la tabla")

    columns_str = ', '.join(columns)

    # Construir la cadena de marcadores de posición para los valores
    placeholders = ', '.join(['?'] * len(columns))

    query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
    query_db(query, values)

    return 1

def getValueDb(table, column_reference, key_reference, column_to_search):
    """Get any value in a table"""
    if not table.isidentifier() or not column_reference.isidentifier():
        raise ValueError("Nombre de tabla o nombre de columna inválido")
    value = query_db(f"""SELECT {column_to_search} FROM {table} WHERE {column_reference} = ?;""", (key_reference,))
    value = value[0][0]

    if value.isdigit():
        if int(value) == 1:
            value = True
        elif int(value) == 0:
            value = False
    return value

def update_valueDb(table, column_reference, key, column_to_search, new_value):
    query_db(f"""UPDATE {table}
    SET {column_reference} = ?
    WHERE {column_to_search} = ?""", (key, new_value))

def del_rowDb(table, column, key):
    """Delete a row in a table with the value in a specific column to refer it"""
    if not table.isidentifier() or not column.isidentifier():
        raise ValueError("Nombre de tabla o nombre de columna inválido")
    query_db(f"""DELETE FROM {table} WHERE {column} = ?;""", (key,))

def del_dataDb(table):
    """Delete all data in a table"""
    query_db(f"DELETE FROM {table}")

def hashing_password(pwd):
    pwd = pwd.encode()
    salt = bcrypt.gensalt()
    pwd_hashed = bcrypt.hashpw(pwd, salt)
    
    return pwd_hashed

def checkpwd(username, password_to_check):
    pwd_hashed = query_db('''SELECT Password FROM users WHERE Username = ?''', (username,))
    if bcrypt.checkpw(password_to_check.encode("utf-8"), pwd_hashed[0][0]):
        return True
    else:
        return False
    

def create_UserDb(username, password):
    # Check if username already exits
    user_exits = query_db("""SELECT COUNT(*) FROM users WHERE Username = ?;""",(username,))
    if user_exits[0][0] > 0:
        pyautogui.alert("The username already exits", f'"{username}" is not disponible.')
        # Actions in gui...
    else:
        # Add the new user and his password hashed to db
        if password == None:
            append_rowDb("users", (username, None))
        else:
            append_rowDb("users", (username, hashing_password(password)))

        # Create the respective tables in db for the user
        query_db(f"""CREATE TABLE macros_{username} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Service TEXT,
        State TEXT);""")

        query_db(f"""CREATE TABLE settings_{username} (
        Service TEXT,
        State TEXT);""")

        SETTINGS = "settings.json"
        with open(SETTINGS, 'r') as file_json:
            data = json.load(file_json)

        filas = []

        for key, value in data.items():
            filas.append((key, value))
        
        query_many_db(f"INSERT INTO settings_{username} VALUES (?, ?)", filas)
        
        # Save the first action in macros
        date_time_now = datetime.datetime.now()
        date_time_now_format = date_time_now.strftime("%I:%M | %d/%m/%Y")
        append_rowDb(f"macros_{username}", (date_time_now_format, f'The user "{username}" was created'))

def del_UserDb(username):
    query_db(f"DROP TABLE settings_{username}")
    query_db(f"DROP TABLE macros_{username}")
    del_rowDb("users", "Username", username)


if __name__ == "__main__":
    create_UserDb("josesp07","hola123")
    create_UserDb("josesp01","hola123")
    create_UserDb("josesp02","hola123")
    create_UserDb("josesp03", None)