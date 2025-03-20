from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error
import os
os.chdir("C:\code\gitproject\pythonproject\membership")

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

# 소비자 인터페이스
def consumer_interface(conn):
    while True:
        print("\n=== 소비자 메뉴 ===")
        print("[1. 멤버십 등록] [2. 검색(등급과 혜택까지)] [3. 종료]")
        choice = input("선택: ")

        if choice == '1':  # 멤버십 등록
            name = input("이름: ")
            phone = input("전화번호 (11자리): ")
            gender = input("성별 (M/F/O, 기본값 O): ") or 'O'
            if gender not in ['M', 'F', 'O']:
                print("잘못된 성별 입력입니다. M, F, O 중 선택하세요.")
                continue

            try:
                cursor = conn.cursor(buffered=True)  # Buffered 커서 사용
                cursor.execute("""
                    INSERT INTO Customers (name, phone, gender, join_date)
                    VALUES (%s, %s, %s, CURRENT_DATE)
                """, (name, phone, gender))
                conn.commit()
                customer_id = cursor.lastrowid
                cursor.execute("""
                    INSERT INTO Grades (customer_id, sum_account, update_date, tier_name)
                    VALUES (%s, 0, CURRENT_TIMESTAMP, 'Silver')
                """, (customer_id,))
                conn.commit()
                print("멤버십 등록 완료!")
            except Error as e:
                print(f"등록 오류: {e}")
            finally:
                cursor.close()

        elif choice == '2':  # 검색 (오류 수정: Buffered 커서 사용)
            phone = input("전화번호: ")
            try:
                cursor = conn.cursor(buffered=True)  # Buffered 커서로 변경
                cursor.execute("""
                    SELECT c.name, c.phone, g.sum_account, g.tier_name, b.discount_rate, b.points_reward
                    FROM Customers c
                    LEFT JOIN Grades g ON c.customer_id = g.customer_id
                    LEFT JOIN Benefit b ON g.tier_name = (
                        SELECT tier_name FROM Grade_Tiers WHERE tier_name = g.tier_name
                    )
                    WHERE c.phone = %s
                """, (phone,))
                result = cursor.fetchone()
                if result:
                    print(f"이름: {result[0]}, 전화번호: {result[1]}, 누적 구매액: {result[2]}원")
                    print(f"等급: {result[3]}, 할인율: {result[4]}%, 포인트 보상: {result[5]}")
                else:
                    print("해당 전화번호가 없습니다. 다시 입력하세요.")
            except Error as e:
                print(f"검색 오류: {e}")
            finally:
                cursor.close()

        elif choice == '3':  # 종료
            print("소비자 모드 종료")
            break
        else:
            print("잘못된 선택입니다.")

# 관리자 인터페이스
def admin_interface(conn):
    while True:
        print("\n=== 관리자 메뉴 ===")
        print("[1. 방문자 구매액 입력] [2. 고객 로그 조회] [3. 고객 목록 조회] [4. 수정] [5. 삭제] [6. 종료]")
        choice = input("선택: ")

        if choice == '1':  # 구매액 입력
            phone_last4 = input("고객 전화번호 뒷 4자리: ")
            try:
                cursor = conn.cursor(buffered=True)  # Buffered 커서 사용
                cursor.execute("""
                    SELECT customer_id, name, phone
                    FROM Customers
                    WHERE RIGHT(phone, 4) = %s
                """, (phone_last4,))
                customers = cursor.fetchall()
                if not customers:
                    print("일치하는 고객이 없습니다.")
                    continue

                print("일치하는 고객 목록:")
                for i, (cid, name, phone) in enumerate(customers, 1):
                    print(f"{i}. {name} ({phone})")
                selection = int(input("선택 (번호): ")) - 1
                if selection < 0 or selection >= len(customers):
                    print("잘못된 선택입니다.")
                    continue
                customer_id = customers[selection][0]

                account = int(input("구매액: "))
                store_name = input("매장 이름: ")
                cursor.execute("SELECT store_id FROM Stores WHERE store_name = %s", (store_name,))
                store = cursor.fetchone()
                if not store:
                    print("존재하지 않는 매장입니다.")
                    continue
                store_id = store[0]

                cursor.execute("""
                    INSERT INTO Logs (customer_id, purchase_date, account, store_id)
                    VALUES (%s, CURRENT_TIMESTAMP, %s, %s)
                """, (customer_id, account, store_id))
                conn.commit()

                # 등급 업데이트
                cursor.execute("""
                    UPDATE Grades g
                    SET g.sum_account = (SELECT SUM(account) FROM Logs WHERE customer_id = g.customer_id),
                        g.tier_name = CASE
                            WHEN g.sum_account >= 500000 THEN 'VVip'
                            WHEN g.sum_account >= 200000 THEN 'Vip'
                            WHEN g.sum_account >= 100000 THEN 'Gold'
                            ELSE 'Silver'
                        END,
                        g.update_date = CURRENT_TIMESTAMP
                    WHERE g.customer_id = %s
                """, (customer_id,))
                conn.commit()
                print("구매액 입력 및 등급 업데이트 완료!")
            except Error as e:
                print(f"입력 오류: {e}")
            finally:
                cursor.close()

        elif choice == '2':  # 고객 로그 조회
            name = input("고객 이름 (Enter로 상위 10개 조회): ")
            try:
                cursor = conn.cursor(buffered=True)  # Buffered 커서 사용
                if name:
                    cursor.execute("""
                        SELECT l.purchase_date, l.account, s.store_name
                        FROM Logs l
                        JOIN Customers c ON l.customer_id = c.customer_id
                        JOIN Stores s ON l.store_id = s.store_id
                        WHERE c.name = %s
                        ORDER BY l.purchase_date DESC
                    """, (name,))
                    logs = cursor.fetchall()
                    if logs:
                        for log in logs:
                            print(f"구매일: {log[0]}, 금액: {log[1]}원, 매장: {log[2]}")
                    else:
                        print("로그가 없습니다.")
                else:
                    cursor.execute("""
                        SELECT l.purchase_date, l.account, s.store_name
                        FROM Logs l
                        JOIN Stores s ON l.store_id = s.store_id
                        ORDER BY l.purchase_date DESC
                        LIMIT 10
                    """)
                    logs = cursor.fetchall()
                    for log in logs:
                        print(f"구매일: {log[0]}, 금액: {log[1]}원, 매장: {log[2]}")
            except Error as e:
                print(f"조회 오류: {e}")
            finally:
                cursor.close()

        elif choice == '3':  # 고객 목록 조회
            try:
                cursor = conn.cursor(buffered=True)  # Buffered 커서 사용
                cursor.execute("""
                    SELECT customer_id, name, phone, gender, join_date
                    FROM Customers
                    ORDER BY customer_id
                """)
                customers = cursor.fetchall()
                if customers:
                    print("\n=== 고객 목록 ===")
                    for customer in customers:
                        print(f"ID: {customer[0]}, 이름: {customer[1]}, 전화번호: {customer[2]}, 성별: {customer[3]}, 가입일: {customer[4]}")
                else:
                    print("등록된 고객이 없습니다.")
            except Error as e:
                print(f"조회 오류: {e}")
            finally:
                cursor.close()

        elif choice == '4':  # 수정
            name = input("수정할 고객 이름: ")
            try:
                cursor = conn.cursor(buffered=True)  # Buffered 커서 사용
                cursor.execute("SELECT customer_id, name, phone, gender FROM Customers WHERE name = %s", (name,))
                customers = cursor.fetchall()
                if not customers:
                    print("일치하는 고객이 없습니다.")
                    continue

                print("일치하는 고객 목록:")
                for i, (cid, name, phone, gender) in enumerate(customers, 1):
                    print(f"{i}. {name} ({phone}, {gender})")
                selection = int(input("선택 (번호): ")) - 1
                if selection < 0 or selection >= len(customers):
                    print("잘못된 선택입니다.")
                    continue
                customer_id = customers[selection][0]

                new_phone = input("새 전화번호 (Enter로 유지): ") or customers[selection][2]
                new_gender = input("새 성별 (M/F/O, Enter로 유지): ") or customers[selection][3]
                cursor.execute("""
                    UPDATE Customers
                    SET phone = %s, gender = %s
                    WHERE customer_id = %s
                """, (new_phone, new_gender, customer_id))
                conn.commit()
                print("수정 완료!")
            except Error as e:
                print(f"수정 오류: {e}")
            finally:
                cursor.close()

        elif choice == '5':  # 삭제
            name = input("삭제할 고객 이름: ")
            try:
                cursor = conn.cursor(buffered=True)  # Buffered 커서 사용
                cursor.execute("SELECT customer_id, name, phone FROM Customers WHERE name = %s", (name,))
                customers = cursor.fetchall()
                if not customers:
                    print("일치하는 고객이 없습니다.")
                    continue

                print("일치하는 고객 목록:")
                for i, (cid, name, phone) in enumerate(customers, 1):
                    print(f"{i}. {name} ({phone})")
                selection = int(input("선택 (번호): ")) - 1
                if selection < 0 or selection >= len(customers):
                    print("잘못된 선택입니다.")
                    continue
                customer_id = customers[selection][0]

                confirm = input("삭제하시겠습니까? (y/n): ").lower()
                if confirm == 'y':
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
                    cursor.execute("DELETE FROM Benefit_Usage_Logs WHERE customer_id = %s", (customer_id,))
                    cursor.execute("DELETE FROM Logs WHERE customer_id = %s", (customer_id,))
                    cursor.execute("DELETE FROM Grades WHERE customer_id = %s", (customer_id,))
                    cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
                    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
                    conn.commit()
                    print("삭제 완료!")
                else:
                    print("삭제 취소")
            except Error as e:
                print(f"삭제 오류: {e}")
            finally:
                cursor.close()

        elif choice == '6':  # 종료
            print("관리자 모드 종료")
            break
        else:
            print("잘못된 선택입니다.")

# 메인 함수
def main():
    conn = connect()
    if conn is None:
        print("데이터베이스 연결에 실패했습니다.")
        return

    try:
        while True:
            print("\n=== 편의점 고객 멤버십 계산 프로그램 ===")
            print("[1. 소비자] [2. 관리자]")
            role = input("역할 선택: ")

            if role == '1':
                consumer_interface(conn)
            elif role == '2':
                admin_interface(conn)
            else:
                print("잘못된 선택입니다.")
    except Error as e:
        print(f"프로그램 오류: {e}")
    finally:
        conn.close()
        print("프로그램 종료")

if __name__ == "__main__":
    main()