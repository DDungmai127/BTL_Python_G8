import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="localhost",
        port = "3306",
        user= "root",
        password="12072003",
        )
    print("Kết nối thành công đến cơ sở dữ liệu")
    if(connection.is_connected):
        print("da ket noi")
    
    cursor = connection.cursor()
    cursor.execute("create database if not exists btl_python")
    cursor.execute("use btl_python")

    # Tạo bảng nếu chưa tồn tại
    create_themes_table = """
    CREATE TABLE IF NOT EXISTS themes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        theme_name VARCHAR(50) UNIQUE NOT NULL
    );
    """

    create_types_table = """
    CREATE TABLE IF NOT EXISTS types (
        id INT AUTO_INCREMENT PRIMARY KEY,
        type_name VARCHAR(50) UNIQUE NOT NULL
    );
    """

    create_words_table = """
    CREATE TABLE IF NOT EXISTS words (
        id INT AUTO_INCREMENT PRIMARY KEY,
        word VARCHAR(50) UNIQUE NOT NULL,
        meaning  VARCHAR(255) NOT NULL,
        phonetic VARCHAR(50),
        usage_word Text,
        synonyms VARCHAR(255),
        antonyms VARCHAR(255),
        theme_id INT,
        type_id INT,
        path VARCHAR(255),
        FOREIGN KEY (theme_id) REFERENCES themes(id),
        FOREIGN KEY (type_id) REFERENCES types(id)
    );
    """

    # Thực thi các truy vấn tạo bảng
    cursor.execute(create_themes_table)
    cursor.execute(create_types_table)
    cursor.execute(create_words_table)


    # Thêm sample data cho bảng themes
    theme_data = [
        ("Thực phẩm",),  
        ("Động vật",),
        ("Thời tiết",),
        ("Công nghệ thông tin",),
        ("Khoa học máy tính",)
    ]
    cursor.executemany("INSERT IGNORE INTO themes (theme_name) VALUES (%s)", theme_data)

    # Thêm sample data cho bảng types
    type_data = [
        ("Noun",),
        ("Verb",),
        ("Adjective",),
        ("Adverb",)
    ]
    cursor.executemany("INSERT IGNORE INTO types (type_name) VALUES (%s)", type_data)

    # Thêm sample data cho bảng words
    word_data = [
        ("algorithm", "Thuật toán", "ˈælgərɪðəm", "Algorithms are essential for computer programming.", "procedure, formula", "randomness", 4, 1, None),
        ("debug", "Gỡ lỗi", "ˈdiːbʌɡ", "She needs to debug the code before deploying.", "fix, troubleshoot", "break", 4, 2, None),
        ("responsive", "Phản hồi nhanh", "rɪˈspɒnsɪv", "The website is fully responsive.", "adaptive, reactive", "unresponsive", 4, 3, None),
        ("cloud", "Điện toán đám mây", "klaʊd", "Cloud computing allows scalable resources.", "sky, network", "local", 4, 1, None),
        ("compile", "Biên dịch", "kəmˈpaɪl", "The code must be compiled before execution.", "assemble, translate", "decompile", 4, 2, None),
        ("encryption", "Mã hóa", "ɪnˈkrɪpʃən", "Encryption secures the data from unauthorized access.", "coding, encoding", "decryption", 4, 1, None),
        ("iterate", "Lặp lại", "ˈɪtəreɪt", "The function iterates through the list.", "repeat, loop", "halt", 4, 2, None),
        ("binary", "Hệ nhị phân", "ˈbaɪnəri", "Binary numbers are fundamental in computing.", "dual, base-2", "decimal", 4, 1, None),
        ("syntax", "Cú pháp", "ˈsɪntæks", "Syntax errors prevent code from running.", "structure, grammar", "semantics", 4, 1, None),
        ("optimize", "Tối ưu hóa", "ˈɒptɪmaɪz", "The developer optimized the code for performance.", "enhance, improve", "degrade", 4, 2, None)
    ]
    cursor.executemany(
        """
        INSERT IGNORE INTO words (
            word, meaning, phonetic, usage_word, synonyms, antonyms, theme_id, type_id, path
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """,
        word_data
    )

    # Lưu thay đổi và đóng kết nối
    connection.commit()
    cursor.close()
    connection.close()
except Error as e:
    print(f"Lỗi khi kết nối: {e}")

