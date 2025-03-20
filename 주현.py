import pymysql

# MySQL 데이터베이스 연결 설정
conn = pymysql.connect(
    host='localhost',   # MySQL 서버 주소
    user='root',        # MySQL 사용자
    password='password', # MySQL 비밀번호
    database='membership_db', # 사용 DB
    charset='utf8mb4'
)
cursor = conn.cursor()

def register_customer():
    """멤버십 등록 (중복 체크 후 등록)"""
    name = input("이름을 입력하세요: ")
    phone = input("전화번호(010-xxxx-xxxx)를 입력하세요: ")
    gender = input("성별(M/F/O): ")
    tier_name = 'Silver'  # 기본 등급
    
    # 중복 확인
    cursor.execute("SELECT * FROM Customers WHERE phone = %s", (phone,))
    if cursor.fetchone():
        print("이미 등록된 전화번호입니다.")
        return
    
    # 등록
    cursor.execute("INSERT INTO Customers (name, phone, gender, join_date, tier_name) VALUES (%s, %s, %s, CURDATE(), %s)",
                   (name, phone, gender, tier_name))
    conn.commit()
    print(f"{name} 님이 멤버십에 등록되었습니다.")

def search_customer():
    """회원 검색 (등급 및 혜택 조회)"""
    phone = input("전화번호를 입력하세요: ")
    cursor.execute("SELECT name, tier_name FROM Customers WHERE phone = %s", (phone,))
    result = cursor.fetchone()
    if result:
        name, tier = result
        print(f"회원: {name}, 등급: {tier}")
        cursor.execute("SELECT description FROM Benefit WHERE tier_name = %s", (tier,))
        benefits = cursor.fetchall()
        print("혜택:")
        for benefit in benefits:
            print(f"- {benefit[0]}")
    else:
        print("회원 정보를 찾을 수 없습니다.")

def log_purchase():
    """방문자 구매 내역 입력 및 등급 자동 업데이트"""
    phone_last4 = input("전화번호 뒷 4자리를 입력하세요: ")
    cursor.execute("SELECT customer_id, name FROM Customers WHERE phone LIKE %s", (f"%{phone_last4}",))
    customers = cursor.fetchall()
    if not customers:
        print("해당 전화번호를 가진 고객이 없습니다.")
        return
    
    for idx, (cid, name) in enumerate(customers, 1):
        print(f"{idx}. {name} (ID: {cid})")
    choice = int(input("고객을 선택하세요 (번호 입력): ")) - 1
    if choice < 0 or choice >= len(customers):
        print("잘못된 선택입니다.")
        return
    
    customer_id = customers[choice][0]
    store_id = int(input("매장 ID를 입력하세요: "))
    amount = int(input("구매액을 입력하세요: "))
    
    # 로그 저장 및 구매 누적 업데이트
    cursor.execute("INSERT INTO Logs (customer_id, purchase_date, account, store_id) VALUES (%s, NOW(), %s, %s)",
                   (customer_id, amount, store_id))
    cursor.execute("UPDATE Grades SET sum_account = sum_account + %s WHERE customer_id = %s",
                   (amount, customer_id))
    
    # 등급 자동 업데이트
    cursor.execute("""
        UPDATE Grades
        SET tier_name = CASE 
            WHEN sum_account >= 500000 THEN 'VVip'
            WHEN sum_account >= 200000 THEN 'Vip'
            WHEN sum_account >= 100000 THEN 'Gold'
            ELSE 'Silver'
        END
        WHERE customer_id = %s
    """, (customer_id,))
    conn.commit()
    print("구매 내역이 기록되었으며 등급이 업데이트되었습니다.")

def delete_customer():
    """고객 삭제"""
    phone = input("삭제할 고객의 전화번호를 입력하세요: ")
    cursor.execute("SELECT customer_id, name FROM Customers WHERE phone = %s", (phone,))
    customer = cursor.fetchone()
    if not customer:
        print("해당 고객이 없습니다.")
        return
    
    customer_id, name = customer
    confirm = input(f"{name} 님을 삭제하시겠습니까? (Y/N): ").strip().upper()
    if confirm == 'Y':
        cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
        conn.commit()
        print(f"{name} 님이 삭제되었습니다.")

def main():
    while True:
        print("[1. 소비자] [2. 관리자] [3. 종료]")
        choice = input("선택: ")
        if choice == '1':
            while True:
                print("[1. 멤버십 등록] [2. 검색] [3. 종료]")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    register_customer()
                elif sub_choice == '2':
                    search_customer()
                elif sub_choice == '3':
                    break
        elif choice == '2':
            while True:
                print("[1. 구매 기록 입력] [2. 로그 조회] [3. 수정] [4. 삭제] [5. 종료]")
                sub_choice = input("선택: ")
                if sub_choice == '1':
                    log_purchase()
                elif sub_choice == '4':
                    delete_customer()
                elif sub_choice == '5':
                    break
        elif choice == '3':
            break

if __name__ == "__main__":
    main()
    conn.close()
