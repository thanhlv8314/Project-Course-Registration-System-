import sys
from UserRepository import UserRepository
from CourseRepository import CourseRepository
from OrderRepository import OrderRepository

PRICE_PER_CREDIT = 500000


def admin_controller(user):
    u_repo = UserRepository()
    c_repo = CourseRepository()
    o_repo = OrderRepository()

    while True:
        print("\n" + "█" * 20 + " QUẢN TRỊ VIÊN " + "█" * 20)
        print("1. QUẢN LÝ ĐĂNG KÝ (UC11)   | 2. QUẢN LÝ HỌC PHÍ (UC12)")
        print("3. QUẢN LÝ MÔN & LỚP (UC13) | 4. QUẢN LÝ SINH VIÊN (UC14)")
        print("5. CẤU HÌNH HỆ THỐNG (UC15) | 6. THỐNG KÊ & BÁO CÁO (UC16)")
        print("0. Đăng xuất")

        choice = input("Chọn nghiệp vụ: ")

        # ========= UC11 =========
        if choice == '1':
            regs = c_repo.get_all_enrollments_detailed()
            print(f"{'ID':<5} | {'Sinh viên':<20} | {'Môn học':<25} | {'Điểm'}")
            print("-" * 60)
            for r in regs:
                print(f"{r['enrollment_id']:<5} | {r['full_name']:<20} | {r['course_name']:<25} | {r['grade'] if r['grade'] is not None else 'Chưa có'}")

            if input("\n[1] Nhập/Sửa điểm | [0] Quay lại: ") == '1':
                print(c_repo.update_grade(
                    input("ID đăng ký: "),
                    input("Điểm (0-10): ")
                ))

        # ========= UC12 =========
        elif choice == '2':
            while True:
                print("\n--- QUẢN LÝ HỌC PHÍ ---")
                print("1. Danh sách hóa đơn")
                print("2. Làm mới dữ liệu")
                print("3. Xác nhận thanh toán")
                print("0. Quay lại")

                sub = input("Chọn: ")

                if sub == '1':
                    invoices = o_repo.get_all_invoices()
                    if not invoices:
                        print("Chưa có hóa đơn")
                    else:
                        for i in invoices:
                            print(f"{i['invoice_id']} | {i['full_name']} | {i['total_amount']:,} | {i['payment_status']}")
                    input("Enter để quay lại...")

                elif sub == '2':
                    print(o_repo.sync_invoices(PRICE_PER_CREDIT))
                    input("Enter để quay lại...")

                elif sub == '3':
                    print(o_repo.update_invoice(
                        input("ID hóa đơn: "),
                        "PAID"
                    ))
                    input("Enter để quay lại...")

                elif sub == '0':
                    break
                else:
                    print("Lựa chọn không hợp lệ")
                    input("Enter...")

        # ========= UC13 =========
        elif choice == '3':
            print("\n1. Thêm môn | 2. Mở lớp | 3. Xóa môn | 0. Quay lại")
            sub = input("Chọn: ")

            if sub == '1':
                print(c_repo.add_course(
                    input("Mã môn: "),
                    input("Tên môn: "),
                    input("Số tín chỉ: "),
                    input("Mô tả: ")
                ))

            elif sub == '2':
                print(c_repo.add_section(
                    input("Mã môn: "),
                    input("Phòng: "),
                    input("Thứ: "),
                    input("Bắt đầu: "),
                    input("Kết thúc: "),
                    input("Sĩ số: ")
                ))

            elif sub == '3':
                for c in c_repo.get_all_courses():
                    print(f"{c['course_code']} - {c['course_name']}")
                code = input("Nhập mã môn cần xóa (0 hủy): ")
                if code != '0':
                    print(c_repo.delete_course(code))

        # ========= UC14 =========
        elif choice == '4':
            for s in u_repo.get_all_students():
                print(f"{s['user_id']} | {s['username']} | {s['full_name']} | {s['status']}")
            uid = input("ID SV cần khóa/mở (0 hủy): ")
            if uid != '0':
                print(u_repo.toggle_user_status(uid))

        elif choice == '5':
            print("\n--- CẤU HÌNH CỔNG ĐĂNG KÝ ---")
            print("1. MỞ đăng ký")
            print("0. ĐÓNG đăng ký")

            status = input("Chọn: ").strip()

            if status not in ('0', '1'):
                print("❌ Chỉ được nhập 0 hoặc 1")
            else:
                print(c_repo.set_registration_status(status))

            input("Enter để quay lại menu...")


        # ========= UC16 =========
        elif choice == '6':
            for r in o_repo.generate_report():
                print(f"{r['course_name']} | {r['total_students']}")
            input("Enter để tiếp tục...")

        elif choice == '0':
            break


def student_controller(user):
    c_repo = CourseRepository()
    o_repo = OrderRepository()
    sid = user['user_id']

    while True:
        print(f"\n——— SINH VIÊN: {user['full_name'].upper()} ———")
        print("1. Tra cứu môn | 2. Đăng ký | 3. Hủy Môn | 4. TKB")
        print("5. Học phí | 6. Bảng điểm")
        print("0. Đăng xuất")

        c = input("Chọn: ")

        # 1. Tra cứu môn
        if c == '1':
            for i in c_repo.get_all_courses():
                print(f"{i['course_code']} - {i['course_name']} - {i['credits']}")

        # 2. Đăng ký
        elif c == '2':
            for s in c_repo.get_available_sections():
                print(f"{s['section_id']} | {s['course_name']} | {s['current_enrollment']}/{s['capacity']}")
            sec = input("ID lớp (0 hủy): ")
            if sec != '0':
                print(c_repo.register_course(sid, sec))

        # 3. Hủy môn
        elif c == '3':
            for s in c_repo.get_registered_sections(sid):
                print(f"{s['section_id']} | {s['course_name']}")
            sec = input("ID lớp cần hủy (0 hủy): ")
            if sec != '0':
                print(c_repo.drop_course(sid, sec))

        # 4. Thời khóa biểu
        elif c == '4':
            for s in c_repo.get_registered_sections(sid):
                print(f"{s['day_of_week']} {s['start_time']}-{s['end_time']} | {s['course_name']}")
            input("Enter...")

        # 5. Học phí
        elif c == '5':
            secs = c_repo.get_registered_sections(sid)
            total_credits = sum(s['credits'] for s in secs)

            print("\n--- CHI TIẾT HỌC PHÍ ---")
            for s in secs:
                print(f"{s['course_name']} : {s['credits'] * PRICE_PER_CREDIT:,}")

            print("Tổng:", total_credits * PRICE_PER_CREDIT)
            print("Trạng thái:", o_repo.get_tuition_status(sid))
            input("Enter...")

        # 6. Bảng điểm + GPA
        elif c == '6':
            grades = c_repo.get_grades(sid)
            total = cr = 0

            print("\n--- BẢNG ĐIỂM ---")
            for g in grades:
                print(f"{g['course_name']} | {g['grade']}")
                if g['grade'] is not None:
                    total += g['grade'] * g['credits']
                    cr += g['credits']

            if cr:
                print("GPA:", round(total / cr, 2))

            input("Enter...")

        # 0. Đăng xuất
        elif c == '0':
            break




def main_entry():
    u_repo = UserRepository()
    while True:
        print("\n===== HỆ THỐNG ĐĂNG KÝ HỌC =====")
        print("1. Đăng nhập | 2. Đăng ký | 0. Thoát")
        c = input("Chọn: ")

        if c == '1':
            user = u_repo.login(input("User: "), input("Pass: "))
            if user:
                admin_controller(user) if user['role'] == 'Admin' else student_controller(user)
            else:
                print("Sai thông tin đăng nhập")
        elif c == '2':
            print(u_repo.register_student(
                input("User: "),
                input("Pass: "),
                input("Họ tên: ")
            ))
        elif c == '0':
            sys.exit()


if __name__ == "__main__":
    main_entry()

