# database.py

import mysql.connector
from mysql.connector import Error
connection = mysql.connector.connect(
    host="localhost",
    port = "3306",
    user= "root",
    password="12072003",   
    database="btl_python",
)
def get_cursor():
    """Trả về cursor để thực hiện truy vấn."""
    return connection.cursor()
def getAllTypes():
    try:
        cursor = get_cursor()
        # Truy vấn dữ liệu từ bảng types
        cursor.execute("SELECT t.type_name FROM types t")
        types = cursor.fetchall()
        # Truy vấn dữ liệu từ bảng words
        types_list= []
        for type_ in types:
            types_list.append(type_[0])
        # print(dictionary_data)
        return  types_list

    except Error as e:
        print(f"Lỗi khi kết nối hoặc truy vấn: {e}")

def addWordToTheme(word, themeid):
    try:
        cursor = get_cursor()
        update_query = """
        UPDATE words
        SET theme_id = %s
        WHERE word = %s
        """
        cursor.execute(update_query, (themeid, word))
        connection.commit()
    except Error as e:
        print(f"Lỗi khi kết nối hoặc truy vấn: {e}")

def removeWordOutTheme(word, themeid):
    try:
        cursor = get_cursor()
        update_query = """
        UPDATE words
        SET theme_id = null
        WHERE word = %s and theme_id=%s
        """
        cursor.execute(update_query, (word, themeid))
        connection.commit()
    except Error as e:
        print(f"Lỗi khi kết nối hoặc truy vấn: {e}")

def getAllWords():
    try:
        cursor = get_cursor()
        query = """
        SELECT w.word, w.meaning, w.phonetic, w.usage_word, t.type_name, w.synonyms, w.antonyms, th.theme_name, w.path 
        FROM words w
        JOIN types t ON w.type_id = t.id 
        LEFT JOIN themes th on w.theme_id = th.id ;
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        # Truy vấn dữ liệu từ bảng 
        dictionary_data = {}
        for row in rows:
            word = row[0]
            dictionary_data[word] = {
                "meaning": row[1],
                "phonetic": row[2],
                "usage": row[3],
                "type": row[4],
                "synonyms": row[5].split(",") if row[5] else [],
                "antonyms": row[6].split(",") if row[6] else [],
                "theme": row[7],
                "path": str(row[8])
            }
        # print(dictionary_data)
        return  dictionary_data
    except Error as e:
        print(f"Lỗi khi kết nối hoặc truy vấn: {e}")

def get_words_by_type(word_type):
    """Lấy từ theo loại từ."""
    try:
        cursor = get_cursor()
        query = """
        SELECT words.*, types.type_name 
        FROM words 
        JOIN types ON words.type_id = types.id 
        WHERE types.type_name = %s;
        """
        cursor.execute(query, (word_type,))
        words = cursor.fetchall()

        words_list = [{
            "id": word[0],
            "word": word[1],
            "meaning": word[2],
            "phonetic": word[3],
            "usage": word[4],
            "synonyms": word[5],
            "antonyms": word[6],
            "theme_id": word[7],
            "type_id": word[8],
            "path": word[9],
            "type_name": word[10]
        } for word in words]

        return words_list

    except Error as e:
        print(f"Lỗi khi truy vấn theo loại từ: {e}")
def getWordByName(word):
    try:
        cursor = get_cursor()
        # query = 
    except Error as e:
        print(f"Lỗi khi truy vấn theo loại từ: {e}")

def getWordByThemeId(theme_id):
    try:
        cursor = get_cursor()
        query = "select word from words where theme_id = %s"
        cursor.execute(query, (theme_id,))
        rows = cursor.fetchall()
        words =[]
        for word in rows:
            words.append(word[0])
        return words
        # query = 
    except Error as e:
        print(f"Lỗi khi truy vấn theo loại từ: {e}")


def getAllTheme():
    try: 
        cursor = get_cursor()
        # Truy vấn dữ liệu từ bảng themes
        cursor.execute("SELECT t.theme_name FROM themes t")
        themes = cursor.fetchall()
        themes_list =[]
        for theme in themes:
            themes_list.append(theme[0])
        return themes_list
    except Error as e:
        print(f"Lỗi khi truy vấn theo loại từ: {e}")
def getThemeByName(themename):
    try:
        cursor = get_cursor()
        query = "select * from themes where theme_name =%s"
        cursor.execute(query, (themename,))
        theme = cursor.fetchone()
        return theme[0]
    except Error as e:
        print(f"Lỗi khi truy vấn theo loại từ: {e}")
def addTheme(themename):
    cursor = get_cursor()
    query = "INSERT IGNORE INTO themes (theme_name) VALUES (%s)"
    cursor.execute(query, (themename,))
    connection.commit()
def deleteTheme(theme_name):
    cursor = get_cursor()
    delete_query = "DELETE FROM themes WHERE theme_name = %s"
    cursor.execute(delete_query, (theme_name,))  # Truyền giá trị vào câu truy vấn
    connection.commit()

