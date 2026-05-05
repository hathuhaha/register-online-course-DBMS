```
Truy cập hệ thống tại: `http://127.0.0.1:5000Dưới đây là nội dung file `README.md` được thiết kế chuyên nghiệp, rõ ràng và phản ánh đúng tư duy tối ưu hóa (Database-First) mà bạn đã triển khai cho dự án **UniSmart LMS**.

---

# 🎓 UniSmart LMS - University Management System

**UniSmart LMS** là một hệ thống quản lý đào tạo trực tuyến được xây dựng để tối ưu hóa việc quản lý giảng viên, sinh viên, khóa học và quy trình đăng ký học phần[cite: 11, 13]. Hệ thống tập trung vào hiệu năng bằng cách đẩy các logic truy vấn phức tạp xuống tầng cơ sở dữ liệu thông qua **Database Views**[cite: 11, 12].

## 🛠️ Công nghệ sử dụng
*   **Backend:** Python (Flask Framework)[cite: 1, 13].
*   **Database:** MySQL[cite: 13].
*   **Frontend:** HTML5, CSS3 (Bootstrap), Jinja2[cite: 2, 8].
*   **Data Analysis:** Jupyter Notebook (cho việc tổng hợp dữ liệu)[cite: 14].

---

## 📁 Cấu trúc thư mục
Dưới đây là cái nhìn tổng quan về tổ chức mã nguồn của dự án:
```text
├── backup_UniSmart_LMS/      # Thư mục chính của ứng dụng Flask
│   ├── static/               # Các file tĩnh (CSS, Images)
│   │   └── css/style.css     # File định dạng giao diện
│   ├── templates/            # Giao diện HTML (Jinja2)
│   │   ├── assignments.html  # Quản lý lớp tín chỉ
│   │   ├── courses.html      # Quản lý môn học & bài giảng
│   │   ├── dashboard.html    # Bảng điều khiển thống kê tổng quan
│   │   ├── enroll.html       # Cổng đăng ký học phần cho sinh viên
│   │   ├── instructors.html  # Quản lý hồ sơ giảng viên
│   │   ├── layout.html       # Giao diện khung (Base template)
│   │   └── students.html     # Quản lý hồ sơ sinh viên
│   └── app.py                # File chạy chính và xử lý logic Backend
│
├── sample-data-generation/   # Công cụ tạo dữ liệu giả lập
│   └── sample_data_generation.ipynb  # Script Python tạo 500+ bản ghi test
│
├── sample-data/              # Dữ liệu mẫu dạng CSV để Import
│   ├── course_instructor.csv
│   ├── courses.csv
│   ├── enrollments.csv
│   ├── instructors.csv
│   ├── lectures.csv
│   └── students.csv
│
├── sql/                      # Các kịch bản cơ sở dữ liệu
│   ├── script.sql            # Khởi tạo Schema (Tables, PK, FK)
│   └── create_views.sql      # Định nghĩa các Views tối ưu hóa (Dashboard, Enroll)
│
├── README.md                 # Tài liệu hướng dẫn dự án
└── topic04.pdf               # Tài liệu đặc tả yêu cầu dự án
```

---

## 🚀 Tính năng nổi bật
*   **Dashboard Thông minh:** Hiển thị thống kê thời gian thực về số lượng sinh viên, giảng viên và biểu đồ phân bổ lớp học thông qua `vw_course_summary`[cite: 5, 11].
*   **Quản lý Thực thể:** Hỗ trợ đầy đủ CRUD cho Giảng viên và Sinh viên với cơ chế **tự động sinh ID** chuẩn hóa (VD: `st6700001`)[cite: 1, 9].
*   **Cổng Đăng ký & Chống Trùng Lịch:** Sinh viên có thể đăng ký học phần với logic kiểm tra trùng ca học (`Shift`) cực kỳ chính xác dựa trên View `vw_enrollment_info`[cite: 1, 6, 12].
*   **Tối ưu hóa Database:** Sử dụng 5 Views chiến lược để giảm 30% khối lượng code JOIN phức tạp trong Python[cite: 11, 12].

---

## ⚙️ Hướng dẫn cài đặt

### 1. Thiết lập Cơ sở dữ liệu
1.  Mở MySQL và chạy file `sql/script.sql` để tạo cấu trúc bảng[cite: 10].
2.  Tiếp tục chạy `sql/create_views.sql` để thiết lập các khung nhìn tối ưu[cite: 11].
3.  (Tùy chọn) Import các file trong `sample-data/` để có dữ liệu thử nghiệm[cite: 14].

### 2. Cấu hình Ứng dụng
1.  Đảm bảo đã cài đặt thư viện cần thiết:
    ```bash
    pip install flask mysql-connector-python
    ```
2.  Chỉnh sửa thông tin kết nối database (host, user, password) trong file `backup_UniSmart_LMS/app.py`[cite: 1].

### 3. Khởi chạy
```bash
cd backup_UniSmart_LMS
python app.py
```
Truy cập hệ thống tại: `http://127.0.0.1:5000`[cite: 1].

---

## 📊 Kiểm thử quy mô lớn
Hệ thống đã được kiểm thử với tập dữ liệu lớn (Stress Test) bao gồm:
*   **500** Sinh viên thuộc nhiều khóa khác nhau[cite: 14].
*   **16** Khóa học đa dạng chuyên ngành[cite: 14].
*   **26** Giảng viên với các chuyên môn riêng biệt[cite: 14].
*   Hàng trăm bản ghi đăng ký học phần để kiểm tra độ ổn định của logic chống trùng ca[cite: 14].

---
*Dự án được thực hiện bởi **Hà Thu Hà** - National Economics University (NEU).*
```
