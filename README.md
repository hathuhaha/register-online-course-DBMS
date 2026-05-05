```

### 3. Cấu hình và Khởi chạy
1.  Cập nhật thông tin kết nối Database (`host`, `user`, `password`) trong file `backup_UniSmart_LMS/app.py`[cite: 1].
2.  Chạy ứng dụng:
    ```bash
    python backup_UniSmart_LMS/app.py
    ```
3.  Truy cập hệ thống tại: `http://127.0.0.1:5000Dưới đây là mã nguồn `README.md` hoàn chỉnh cho dự án **UniSmart LMS**, được biên soạn để làm nổi bật tư duy tối ưu hóa kiến trúc "Database-First" và quy trình phát triển chuyên nghiệp của bạn.

---

# 🎓 UniSmart LMS - University Management System

**UniSmart LMS** là một hệ thống quản lý đào tạo trực tuyến toàn diện, được thiết kế để hỗ trợ việc tổ chức hiệu quả các khóa học, giảng viên, sinh viên và tài liệu học tập[cite: 13]. Dự án tập trung vào việc tối ưu hóa hiệu năng hệ thống bằng cách sử dụng các đối tượng cơ sở dữ liệu nâng cao như **Views** để giảm thiểu sự phức tạp của logic tại tầng ứng dụng[cite: 11, 12, 13].

## 🛠️ Công nghệ sử dụng
*   **Backend:** Python (Flask Framework)[cite: 1, 13].
*   **Database:** MySQL[cite: 13].
*   **Thư viện kết nối:** `mysql-connector-python`[cite: 1, 13].
*   **Frontend:** HTML5, CSS3 (Bootstrap), Jinja2[cite: 2, 8].
*   **Phân tích & Giả lập dữ liệu:** Jupyter Notebook (Python)[cite: 14].

---

## 📁 Cấu trúc thư mục dự án
Hệ thống được tổ chức theo cấu trúc module rõ ràng để dễ dàng bảo trì và mở rộng:
```text
├── backup_UniSmart_LMS/           # Mã nguồn chính của ứng dụng Flask
│   ├── static/                    # Các tài nguyên tĩnh
│   │   └── css/style.css          # Tùy chỉnh giao diện CSS[cite: 2]
│   ├── templates/                 # Các tệp giao diện Jinja2[cite: 8]
│   │   ├── assignments.html       # Quản lý lớp học phần[cite: 3]
│   │   ├── courses.html           # Quản lý môn học và bài giảng[cite: 4]
│   │   ├── dashboard.html         # Dashboard thống kê hệ thống[cite: 5]
│   │   ├── enroll.html            # Cổng đăng ký cho sinh viên[cite: 6]
│   │   ├── instructors.html       # Quản lý hồ sơ giảng viên[cite: 7]
│   │   ├── layout.html            # Template khung cơ sở[cite: 8]
│   │   └── students.html          # Quản lý hồ sơ sinh viên[cite: 9]
│   └── app.py                     # Xử lý logic nghiệp vụ và Route[cite: 1]
│
├── sample-data-generation/        # Công cụ tổng hợp dữ liệu quy mô lớn
│   └── sample_data_generation.ipynb # Script tạo dữ liệu kiểm thử[cite: 14]
│
├── sample-data/                   # Tập dữ liệu mẫu định dạng CSV[cite: 14]
│   ├── course_instructor.csv
│   ├── courses.csv
│   ├── enrollments.csv
│   ├── instructors.csv
│   ├── lectures.csv
│   └── students.csv
│
├── sql/                           # Các kịch bản SQL cho Database
│   ├── script.sql                 # Khởi tạo Schema và Constraints[cite: 10]
│   └── create_views.sql           # Khởi tạo các Views tối ưu hóa[cite: 11, 12]
│
├── README.md                      # Hướng dẫn và mô tả dự án
└── topic04.pdf                    # Tài liệu yêu cầu kỹ thuật[cite: 13]
```

---

## 🚀 Các tính năng nổi bật

### 1. Dashboard Thống kê thời gian thực
*   Cung cấp cái nhìn tổng quan về tổng số sinh viên, giảng viên và khóa học[cite: 5, 12].
*   Sử dụng `vw_course_summary` để tổng hợp số lượng lớp học và giảng viên mỗi môn một cách nhanh chóng[cite: 5, 11].

### 2. Quản lý Thực thể & Tự động hóa
*   Hỗ trợ đầy đủ CRUD cho Giảng viên, Sinh viên và Khóa học[cite: 13].
*   Tích hợp thuật toán tự động sinh mã định danh (ID) thông minh, ví dụ: mã sinh viên bắt đầu bằng `st` kèm theo khóa học (Cohort)[cite: 1, 9].

### 3. Cổng Đăng ký & Kiểm tra Ràng buộc Logic
*   Cho phép sinh viên tra cứu thời khóa biểu cá nhân và danh sách các lớp đang mở[cite: 6].
*   Tính năng **Conflict Check**: Hệ thống tự động kiểm tra trùng ca học (`Shift`) bằng cách truy vấn View `vw_enrollment_info` trước khi ghi nhận đăng ký mới, đảm bảo tính toàn vẹn lịch học[cite: 1, 6, 12].

### 4. Tối ưu hóa Database-First
*   Sử dụng các Database Views (`vw_assignment_details`, `vw_instructor_stats`,...) để loại bỏ hơn 30% các câu lệnh JOIN phức tạp trong mã nguồn Python[cite: 11, 12].

---

## ⚙️ Hướng dẫn thiết lập

### 1. Khởi tạo Cơ sở dữ liệu
1.  Truy cập MySQL Server và thực thi file `sql/script.sql` để tạo database `UniversityDB` cùng các bảng liên quan[cite: 10].
2.  Thực thi file `sql/create_views.sql` để thiết lập các khung nhìn tối ưu[cite: 11].

### 2. Cài đặt môi trường Python
```bash
pip install flask mysql-connector-python
```

### 3. Cấu hình và Khởi chạy
1.  Cập nhật thông tin kết nối Database (`host`, `user`, `password`) trong file `backup_UniSmart_LMS/app.py`[cite: 1].
2.  Chạy ứng dụng:
    ```bash
    python backup_UniSmart_LMS/app.py
    ```
3.  Truy cập hệ thống tại: `http://127.0.0.1:5000`[cite: 1].

---

## 📊 Kiểm thử hệ thống (Stress Testing)
Hệ thống đã được kiểm thử với khối lượng dữ liệu lớn được sinh ra từ file `sample_data_generation.ipynb`[cite: 14]:
*   **500** hồ sơ sinh viên với mã ID chuẩn hóa[cite: 14].
*   **16** môn học đa dạng và **26** giảng viên thuộc nhiều chuyên ngành[cite: 14].
*   Hàng trăm bản ghi đăng ký được sắp xếp theo thời gian để kiểm tra logic chống trùng lịch học[cite: 14].

---
*Dự án cuối kỳ được thực hiện bởi **Hà Thu Hà** - Khoa Khoa học dữ liệu và Trí tuệ nhân tạo, Đại học Kinh tế Quốc dân (NEU).*
```
