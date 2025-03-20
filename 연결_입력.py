from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error
import os
os.chdir("C:/code/gitproject/pythonproject/CVS/SQL")


# 데이터베이스 설정 불러오기
def read_config(filename='app.ini', section='mysql'):    
    config = ConfigParser()
    config.read(filename)
    data = {}
    if config.has_section(section):
        items = config.items(section)
        for item in items:
            data[item[0]] = item[1]
    else:
        raise Exception(f'{section} section not found in the {filename} file')
    return data

# MySQL 연결
def connect(): 
    try: 
        config = read_config()
        return MySQLConnection(**config)
    except Error as error:
        print(f"데이터베이스 연결 오류: {error}")
        return None

# 멤버십 등록 함수
def register_customer():
    connection = connect()
    if connection is None:
        return
    
    cursor = connection.cursor()
    try:
        name = input("이름 (최대 15자): ")
        phone = input("전화번호 (01012345678 형식): ")
        gender = input("성별 (M/F/O): ").upper()
        join_date = input("가입 날짜 (YYYY-MM-DD): ")
        
        # 입력 검증
        if len(name) > 15:
            print("이름은 15자를 넘을 수 없습니다.")
            return
        if len(phone) != 11 or not phone.isdigit():
            print("전화번호는 11자리 숫자여야 합니다.")
            return
        if gender not in ['M', 'F', 'O']:
            print("성별은 M, F, O 중 하나여야 합니다.")
            return
        
        query = """
        INSERT INTO Customers (name, phone, gender, join_date)
        VALUES (%s, %s, %s, %s)
        """
        values = (name, phone, gender, join_date)
        cursor.execute(query, values)
        connection.commit()
        print(f"멤버십이 등록되었습니다. 고객 ID: {cursor.lastrowid}")
    except Error as e:
        print(f"등록 오류: {e}")
    finally:
        cursor.close()
        connection.close()

# 멤버십 수정 함수
def modify_customer():
    connection = connect()
    if connection is None:
        return
    
    cursor = connection.cursor()
    try:
        customer_id = input("수정할 고객 ID: ")
        
        # 고객 존재 여부 확인
        cursor.execute("SELECT * FROM Customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            print("해당 고객이 존재하지 않습니다.")
            return
        
        print(f"현재 정보: ID: {customer[0]}, 이름: {customer[1]}, 전화번호: {customer[2]}, 성별: {customer[3]}, 가입일: {customer[4]}")
        print("1. 이름")
        print("2. 전화번호")
        print("3. 성별")
        print("4. 가입 날짜")
        
        choice = input("수정할 항목 번호: ")
        
        if choice == '1':
            new_value = input("새 이름 (최대 15자): ")
            if len(new_value) > 15:
                print("이름은 15자를 넘을 수 없습니다.")
                return
            query = "UPDATE Customers SET name = %s WHERE customer_id = %s"
            values = (new_value, customer_id)
        elif choice == '2':
            new_value = input("새 전화번호 (01012345678 형식): ")
            if len(new_value) != 11 or not new_value.isdigit():
                print("전화번호는 11자리 숫자여야 합니다.")
                return
            query = "UPDATE Customers SET phone = %s WHERE customer_id = %s"
            values = (new_value, customer_id)
        elif choice == '3':
            new_value = input("새 성별 (M/F/O): ").upper()
            if new_value not in ['M', 'F', 'O']:
                print("성별은 M, F, O 중 하나여야 합니다.")
                return
            query = "UPDATE Customers SET gender = %s WHERE customer_id = %s"
            values = (new_value, customer_id)
        elif choice == '4':
            new_value = input("새 가입 날짜 (YYYY-MM-DD): ")
            query = "UPDATE Customers SET join_date = %s WHERE customer_id = %s"
            values = (new_value, customer_id)
        else:
            print("잘못된 항목 번호입니다.")
            return
        
        cursor.execute(query, values)
        connection.commit()
        print("멤버십이 수정되었습니다.")
    except Error as e:
        print(f"수정 오류: {e}")
    finally:
        cursor.close()
        connection.close()

# 멤버십 삭제 함수
def delete_customer():
    connection = connect()
    if connection is None:
        return
    
    cursor = connection.cursor()
    try:
        customer_id = input("삭제할 고객 ID: ")
        
        # 고객 존재 여부 확인
        cursor.execute("SELECT * FROM Customers WHERE customer_id = %s", (customer_id,))
        customer = cursor.fetchone()
        if not customer:
            print("해당 고객이 존재하지 않습니다.")
            return
        
        print(f"삭제할 고객: ID: {customer[0]}, 이름: {customer[1]}, 전화번호: {customer[2]}")
        confirm = input("삭제하시겠습니까? (y/n): ")
        
        if confirm.lower() == 'y':
            query = "DELETE FROM Customers WHERE customer_id = %s"
            cursor.execute(query, (customer_id,))
            connection.commit()
            print("멤버십이 삭제되었습니다.")
        else:
            print("삭제가 취소되었습니다.")
    except Error as e:
        print(f"삭제 오류: {e}")
    finally:
        cursor.close()
        connection.close()

# 메인 메뉴
def main():
    while True:
        print('''
        \n=== 멤버십 관리 시스템 ===")
        1. 멤버십 등록
        2. 멤버십 수정
        3. 멤버십 삭제
        4. 프로그램 종료
              ''')
        
        choice = input("메뉴 선택: ")
        
        if choice == '1':
            register_customer()
        elif choice == '2':
            modify_customer()
        elif choice == '3':
            delete_customer()
        elif choice == '4':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")

# 데이터베이스 연결 함수
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="your_password",  # 본인의 비밀번호로 변경
            database="market_db"       # 데이터베이스 이름 (미리 생성 필요)
        )
        return conn
    except mysql.connector.Error as e:
        print(f"데이터베이스 연결 실패: {e}")
        return None

# 로그 추가 함수
def add_purchase_log(conn, customer_id, account, store_name):
    try:
        cursor = conn.cursor()
        
        # 쿼리 작성 (log_id와 purchase_date 생략)
        query = """
            INSERT INTO Logs (customer_id, account, store_name)
            VALUES (%s, %s, %s)
        """
        values = (customer_id, account, store_name)

        # 쿼리 실행
        cursor.execute(query, values)
        conn.commit()
        print(f"로그가 추가되었습니다: 고객 ID {customer_id}, 금액 {account}")

    except mysql.connector.Error as e:
        print(f"로그 추가 실패: {e}")
    finally:
        cursor.close()

# 메인 실행 코드
def main():
    # 데이터베이스 연결
    conn = connect_db()
    if not conn:
        return

    # 사용자 입력 받기
    try:
        customer_id = int(input("고객 ID를 입력하세요: "))
        account = int(input("구매 금액을 입력하세요 (정수): "))
        store_name = input("가게 이름을 입력하세요: ")

        # 로그 추가 (log_id와 purchase_date는 자동 삽입)
        add_purchase_log(conn, customer_id, account, store_name)

    except ValueError as e:
        print(f"입력 오류: 숫자를 정확히 입력해주세요. ({e})")
    except Exception as e:
        print(f"오류 발생: {e}")
    finally:
        conn.close()