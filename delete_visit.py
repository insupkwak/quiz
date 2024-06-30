import mysql.connector

def get_db_connection():
    connection = mysql.connector.connect(
        host="svc.sel5.cloudtype.app",
        port=31200,
        user="mariadb",
        password="1234",
        database="mariadb"
    )
    return connection

def delete_all_visit_count():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM visit_count")
        connection.commit()
        print("모든 방문자 기록이 삭제되었습니다.")
    except mysql.connector.Error as err:
        print(f"기록 삭제에 실패했습니다: {err}")
    finally:
        cursor.close()
        connection.close()

def initialize_database():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visit_count (
            id INT AUTO_INCREMENT PRIMARY KEY,
            count INT NOT NULL
        )
    ''')
    cursor.execute('''
        INSERT INTO visit_count (count)
        SELECT 0
        WHERE NOT EXISTS (SELECT 1 FROM visit_count)
    ''')
    connection.commit()
    cursor.close()
    connection.close()

def print_visit_count():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT count FROM visit_count")
        count = cursor.fetchone()[0]
        print(f"현재 방문자 수: {count}")
    except mysql.connector.Error as err:
        print(f"방문자 수를 가져오는 데 실패했습니다: {err}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
  
    initialize_database()
    print_visit_count()
