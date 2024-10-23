import csv
import os
import tkinter as tk
from tkinter import messagebox

class UserManager:
    def __init__(self, users_file):
        self.users_file = users_file
        self.users = self.load_users_from_csv()

    def load_users_from_csv(self):
        users = {}
        try:
            with open(self.users_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    users[row["username"]] = {"password": row["password"], "role": row["role"]}
        except Exception as e:
            print(f"Error reading file: {e}")
        return users

    def save_user_to_csv(self, username, password, role):
        try:
            with open(self.users_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([username, password, role])
                print(f"User {username} added to CSV.")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def add_user(self, username, password, role):
        if username not in self.users:
            self.save_user_to_csv(username, password, role)
            self.users[username] = {"password": password, "role": role}
            return True
        return False

    def validate_login(self, username, password):
        user = self.users.get(username)
        if user and user["password"] == password:
            return user["role"]
        return None

class HomeScreen:
    def __init__(self, root, user_manager):
        self.root = root
        self.user_manager = user_manager

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Chào Mừng", font=("Arial", 16, "bold")).pack(pady=20)
        tk.Button(self.root, text="Đăng Nhập", command=self.show_login_screen, width=20).pack(pady=10)
        tk.Button(self.root, text="Đăng Ký", command=self.show_register_screen, width=20).pack(pady=10)

    def show_login_screen(self):
        login_screen = LoginScreen(self.root, self.user_manager)
        login_screen.show()

    def show_register_screen(self):
        register_screen = RegisterScreen(self.root, self.user_manager)
        register_screen.show()

class LoginScreen:
    def __init__(self, root, user_manager):
        self.root = root
        self.user_manager = user_manager

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Tên người dùng:").pack(pady=10)
        username_entry = tk.Entry(self.root)
        username_entry.pack(pady=5)

        tk.Label(self.root, text="Mật khẩu:").pack(pady=5)
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        def login():
            username = username_entry.get()
            password = password_entry.get()
            role = self.user_manager.validate_login(username, password)
            if role:
                messagebox.showinfo("Thông báo", "Đăng nhập thành công!")
                if role == "teacher":
                    teacher_screen = TeacherScreen(self.root, self.user_manager)
                    teacher_screen.show()
                else:
                    student_screen = StudentScreen(self.root, self.user_manager)
                    student_screen.show()
            else:
                messagebox.showerror("Lỗi", "Tên người dùng hoặc mật khẩu không chính xác!")

        tk.Button(self.root, text="Đăng nhập", command=login).pack(pady=20)
        tk.Button(self.root, text="Quay lại", command=self.show_home_screen).pack(pady=10)

    def show_home_screen(self):
        home_screen = HomeScreen(self.root, self.user_manager)
        home_screen.show()

class RegisterScreen:
    def __init__(self, root, user_manager):
        self.root = root
        self.user_manager = user_manager

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Đăng Ký Tài Khoản", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.root, text="Tên người dùng:").pack(pady=10)
        new_username_entry = tk.Entry(self.root)
        new_username_entry.pack(pady=5)

        tk.Label(self.root, text="Mật khẩu:").pack(pady=10)
        new_password_entry = tk.Entry(self.root, show="*")
        new_password_entry.pack(pady=5)

        tk.Label(self.root, text="Vai trò (teacher/student):").pack(pady=10)
        new_role_entry = tk.Entry(self.root)
        new_role_entry.pack(pady=5)

        def register():
            username = new_username_entry.get()
            password = new_password_entry.get()
            role = new_role_entry.get()

            if username and password and role in ["teacher", "student"]:
                if self.user_manager.add_user(username, password, role):
                    messagebox.showinfo("Thông báo", "Đăng ký thành công!")
                    self.show_home_screen()
                else:
                    messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")
            else:
                messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

        tk.Button(self.root, text="Đăng Ký", command=register).pack(pady=20)
        tk.Button(self.root, text="Quay lại", command=self.show_home_screen, fg="red").pack(pady=5)

    def show_home_screen(self):
        home_screen = HomeScreen(self.root, self.user_manager)
        home_screen.show()

class StudentScreen:
    def __init__(self, root, user_manager):
        self.root = root
        self.user_manager = user_manager

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Chức năng sinh viên", font=("Arial", 14, "bold")).pack(pady=10)
        functions = ["Thông báo chung", "Hồ sơ sinh viên", "Lịch học", "Lịch thi", "Điểm số", "Đăng ký học"]

        for func in functions:
            if func == "Cập nhật thông tin":
                tk.Button(self.root, text=func, width=30, command=self.show_update_student_screen).pack(pady=5)
            elif func == "Đăng ký học":
                tk.Button(self.root, text=func, width=30, command=self.open_registration_app).pack(pady=5)
            else:
                tk.Button(self.root, text=func, width=30, command=lambda f=func: self.show_message(f)).pack(pady=5)

        tk.Button(self.root, text="Đăng xuất", command=self.show_home_screen).pack(pady=20)


    def open_registration_app(self):
        registration_screen = CourseRegistrationScreen(self.root, self.user_manager)
        registration_screen.show()

    def show_message(self, func):
        messagebox.showinfo("Thông báo", f"Chức năng '{func}' đang được phát triển")

    def show_home_screen(self):
        home_screen = HomeScreen(self.root, self.user_manager)
        home_screen.show()

class CourseRegistrationScreen:
    def __init__(self, root, user_manager):
        self.root = root
        self.user_manager = user_manager
        self.registrations_file = "registrations.csv"  # Tên file CSV để lưu thông tin đăng ký

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Đăng Ký Môn Học", font=("Arial", 16, "bold")).pack(pady=20)

        # Nhập tên sinh viên
        tk.Label(self.root, text="Nhập Tên Sinh Viên:", font=("Arial", 12)).pack(pady=10)
        self.entry_student_name = tk.Entry(self.root)
        self.entry_student_name.pack(pady=5)

        # Nhập email sinh viên
        tk.Label(self.root, text="Nhập Email Sinh Viên:", font=("Arial", 12)).pack(pady=10)
        self.entry_student_email = tk.Entry(self.root)
        self.entry_student_email.pack(pady=5)

        # Đăng ký môn học
        tk.Label(self.root, text="Chọn Môn Học:", font=("Arial", 12)).pack(pady=10)
        self.listbox_courses = tk.Listbox(self.root, height=5)
        self.listbox_courses.insert(1, "Môn 1 - Đại số tuyến tính")
        self.listbox_courses.insert(2, "Môn 2 - Toán cao cấp")
        self.listbox_courses.insert(3, "Môn 4 - Giải tích")
        self.listbox_courses.insert(4, "Môn 5 - Vật lý đại cương")
        self.listbox_courses.insert(5, "Môn 5 - Tin học Đại cương")
        self.listbox_courses.insert(6, "Môn 6 - Lập trình hướng đối tượng")
        self.listbox_courses.pack(pady=5)

        self.button_register_course = tk.Button(self.root, text="Đăng Ký Môn", command=self.register_course)
        self.button_register_course.pack(pady=10)

        self.button_back = tk.Button(self.root, text="Quay lại", command=self.show_student_screen)
        self.button_back.pack(pady=5)  # Add the back button here

    def register_course(self):
        student_name = self.entry_student_name.get()
        student_email = self.entry_student_email.get()
        selected_course = self.listbox_courses.get(tk.ACTIVE)

        if selected_course:
            # Hiển thị thông báo xác nhận
            confirmation = messagebox.askyesno("Xác nhận", 
                f"Bạn có chắc chắn muốn đăng ký môn: {selected_course} cho sinh viên: {student_name} với email: {student_email}?")
            
            if confirmation:  # Nếu người dùng nhấn "Yes"
                self.save_registration(student_name, student_email, selected_course)
                messagebox.showinfo("Thông báo", f"Bạn đã đăng ký môn: {selected_course}")
            else:  # Nếu người dùng nhấn "No"
                messagebox.showinfo("Thông báo", "Đăng ký đã bị hủy.")
        else:
            messagebox.showwarning("Cảnh báo", "Vui lòng chọn môn học!")

    def save_registration(self, student_name, student_email, course):
        try:
            with open(self.registrations_file, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([student_name, student_email, course])
                print(f"Thông tin đăng ký đã được lưu vào {self.registrations_file}.")
        except Exception as e:
            print(f"Không thể lưu thông tin đăng ký: {e}")

    def show_student_screen(self):
        student_screen = StudentScreen(self.root, self.user_manager)
        student_screen.show()

class TeacherScreen:
    def __init__(self, root, user_manager):
        self.root = root
        self.user_manager = user_manager

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Chức năng giảng viên", font=("Arial", 14, "bold")).pack(pady=10)
        functions = ["Quản lý sinh viên", "Cập nhật thông tin sinh viên", "Quản lý khóa học", "Lịch dạy", "Chấm điểm", "Thêm sinh viên"]
        
        for func in functions:
            if func == "Thêm sinh viên":
                tk.Button(self.root, text=func, width=30, command=self.show_add_student_screen).pack(pady=5)
            elif func == "Cập nhật thông tin sinh viên":
                tk.Button(self.root, text=func, width=30, command=self.show_update_student_screen).pack(pady=5)
            elif func == "Quản lý sinh viên":
                tk.Button(self.root, text=func, width=30, command=self.show_student_management_screen).pack(pady=5)
            else:
                tk.Button(self.root, text=func, width=30, command=lambda f=func: self.show_message(f)).pack(pady=5)

        tk.Button(self.root, text="Đăng xuất", command=self.show_home_screen).pack(pady=20)

    def show_student_management_screen(self):
        student_management_screen = StudentManagementScreen(self.root, self.user_manager)
        student_management_screen.show()

    def show_add_student_screen(self):
        add_student_screen = AddStudentScreen(self.root, self.user_manager)
        add_student_screen.show()

    def show_update_student_screen(self):
        update_student_screen = UpdateStudentScreen(self.root, self.user_manager)
        update_student_screen.show()

    def show_message(self, func):
        messagebox.showinfo("Thông báo", f"Chức năng '{func}' đang được phát triển")

    def show_home_screen(self):
        home_screen = HomeScreen(self.root, self.user_manager)
        home_screen.show()

class UpdateStudentScreen:
    def __init__(self, root, user_manager):
        self.root = root
        self.user_manager = user_manager
        self.student_data = self.load_students()  # Tải dữ liệu sinh viên từ file CSV

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Quản lý thông tin sinh viên", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.root, text="ID Sinh Viên:").pack(pady=10)
        self.id_entry = tk.Entry(self.root)
        self.id_entry.pack(pady=5)

        tk.Button(self.root, text="Tìm sinh viên", command=self.find_student).pack(pady=20)

        # Các trường nhập thông tin sinh viên
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)
        self.name_entry.insert(0, "Tên sinh viên")

        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)
        self.email_entry.insert(0, "Email sinh viên")

        tk.Button(self.root, text="Cập nhật thông tin", command=self.update_student_info).pack(pady=10)
        tk.Button(self.root, text="Thêm sinh viên", command=self.add_student).pack(pady=10)
        tk.Button(self.root, text="Xóa sinh viên", command=self.delete_student).pack(pady=10)
        tk.Button(self.root, text="Quay lại", command=self.show_teacher_screen).pack(pady=10)

    def find_student(self):
        student_id = self.id_entry.get()
        student = self.get_student_by_id(student_id)

        if student:
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, student[1])  # Tên sinh viên
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, student[2])  # Email sinh viên
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy sinh viên với ID này!")

    def get_student_by_id(self, student_id):
        for student in self.student_data:
            if student[0] == student_id:  # Giả định rằng ID sinh viên là trường đầu tiên
                return student
        return None

    def update_student_info(self):
        student_id = self.id_entry.get()
        new_name = self.name_entry.get()
        new_email = self.email_entry.get()

        if student_id and new_name and new_email:
            updated = False
            for i, student in enumerate(self.student_data):
                if student[0] == student_id:
                    self.student_data[i][1] = new_name
                    self.student_data[i][2] = new_email
                    updated = True
                    break

            if updated:
                self.save_students()
                messagebox.showinfo("Thông báo", "Cập nhật thông tin sinh viên thành công!")
            else:
                messagebox.showerror("Lỗi", "Không tìm thấy sinh viên với ID này!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def add_student(self):
        new_id = self.id_entry.get()
        new_name = self.name_entry.get()
        new_email = self.email_entry.get()

        if new_id and new_name and new_email:
            if not self.get_student_by_id(new_id):  # Kiểm tra nếu sinh viên chưa tồn tại
                self.student_data.append([new_id, new_name, new_email])
                self.save_students()
                messagebox.showinfo("Thông báo", "Thêm sinh viên thành công!")
                self.clear_entries()  # Xóa các trường nhập
            else:
                messagebox.showerror("Lỗi", "ID sinh viên đã tồn tại!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def delete_student(self):
        student_id = self.id_entry.get()

        if student_id:
            for i, student in enumerate(self.student_data):
                if student[0] == student_id:
                    del self.student_data[i]
                    self.save_students()
                    messagebox.showinfo("Thông báo", "Xóa sinh viên thành công!")
                    self.clear_entries()  # Xóa các trường nhập
                    return

            messagebox.showerror("Lỗi", "Không tìm thấy sinh viên với ID này!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập ID sinh viên!")

    def save_students(self):
        with open("students.csv", mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(self.student_data)

    def load_students(self):
        try:
            with open("students.csv", mode="r") as file:
                reader = csv.reader(file)
                return list(reader)
        except FileNotFoundError:
            return []  # Trả về danh sách rỗng nếu file không tồn tại

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)

    def show_teacher_screen(self):
        teacher_screen = TeacherScreen(self.root, self.user_manager)
        teacher_screen.show()

class AddStudentScreen:
    def __init__(self, root, user_manager):
        self.root = root
        self.user_manager = user_manager

    def show(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Thêm Sinh Viên", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(self.root, text="Tên người dùng:").pack(pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        tk.Label(self.root, text="Mật khẩu:").pack(pady=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        tk.Label(self.root, text="Vai trò (student):").pack(pady=10)
        self.role_entry = tk.Entry(self.root)
        self.role_entry.insert(0, "student")
        self.role_entry.config(state='disabled')
        self.role_entry.pack(pady=5)

        tk.Button(self.root, text="Thêm Sinh Viên", command=self.add_student).pack(pady=20)
        tk.Button(self.root, text="Quay lại", command=self.show_teacher_screen).pack(pady=10)

    def add_student(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = "student"

        if username and password:
            if self.user_manager.add_user(username, password, role):
                messagebox.showinfo("Thông báo", "Thêm sinh viên thành công!")
            else:
                messagebox.showerror("Lỗi", "Tài khoản đã tồn tại!")
        else:
            messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ thông tin!")

    def show_teacher_screen(self):
        teacher_screen = TeacherScreen(self.root, self.user_manager)
        teacher_screen.show()

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


class University:
    def __init__(self, name):
        self.name = name
        self.faculties = []

    def add_faculty(self, faculty):
        self.faculties.append(faculty)


class Faculty(University):
    def __init__(self, name):
        super().__init__(name)
        self.lecturers = []
        self.courses = []

    def add_lecturer(self, lecturer):
        self.lecturers.append(lecturer)

    def add_course(self, course):
        self.courses.append(course)


class Lecturer(Person):
    def __init__(self, name, age, faculty):
        super().__init__(name, age)
        self.faculty = faculty
        self.courses = []

    def assign_course(self, course):
        self.courses.append(course)
        course.lecturer = self


class Course:
    def __init__(self, name, credits):
        self.name = name
        self.credits = credits
        self.lecturer = None
        self.students = []

    def add_student(self, student):
        self.students.append(student)
        student.courses.append(self)


class Student(Person):
    def __init__(self, name, age, student_id):
        super().__init__(name, age)
        self.student_id = student_id
        self.courses = []

    def register_course(self, course):
        course.add_student(self)

def main():
    root = tk.Tk()
    root.title("Hệ Thống Quản Lý Sinh Viên")
    root.geometry("400x400")

    users_file = "users.csv"
    user_manager = UserManager(users_file)

    if not os.path.exists(users_file):
        with open(users_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["username", "password", "role"])

    home_screen = HomeScreen(root, user_manager)
    home_screen.show()

    root.mainloop()

if __name__ == "__main__":
    main()
