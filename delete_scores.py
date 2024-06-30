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

def delete_all_scores():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("DELETE FROM scores")
        connection.commit()
        print("모든 기록이 삭제되었습니다.")
    except mysql.connector.Error as err:
        print(f"기록 삭제에 실패했습니다: {err}")
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    delete_all_scores()
