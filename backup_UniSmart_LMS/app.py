from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import datetime

app = Flask(__name__)
app.secret_key = "unismart_super_secret_key"

# Mật khẩu gốc của bạn được giữ nguyên
db_config = {'host': 'localhost', 'user': 'root', 'password': '060718', 'database': 'UniversityDB'}

def get_db():
    return mysql.connector.connect(**db_config)

# ======= HÀM TẠO ID TỰ ĐỘNG THÔNG MINH =======
def get_next_id(cursor, table, column, prefix, length):
    cursor.execute(f"SELECT {column} FROM {table} WHERE {column} LIKE '{prefix}%'")
    ids = [row[column] for row in cursor.fetchall() if row[column]]
    nums = [int(id_str[len(prefix):]) for id_str in ids if id_str[len(prefix):].isdigit()]
    nums_set = set(nums)
    new_num = 0
    while new_num in nums_set:
        new_num += 1
    return f"{prefix}{new_num:0{length}d}"

def get_next_student_id(cursor, khoa):
    cursor.execute("SELECT LearnerID FROM LEARNERS WHERE LearnerID LIKE 'st%'")
    ids = [row['LearnerID'] for row in cursor.fetchall() if row['LearnerID']]
    nums = [int(id_str[-5:]) for id_str in ids if id_str[-5:].isdigit()]
    nums_set = set(nums)
    new_num = 0
    while new_num in nums_set:
        new_num += 1
    return f"st{khoa}{new_num:05d}"

# ======= CÁC ROUTES =======

@app.route('/')
def dashboard():
    conn = get_db(); cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM LEARNERS")
    total_students = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM INSTRUCTORS")
    total_instructors = cursor.fetchone()['total']

    cursor.execute("SELECT COUNT(*) as total FROM COURSES")
    total_courses = cursor.fetchone()['total']

    # Dùng View vw_course_summary thay vì JOIN
    cursor.execute("SELECT * FROM vw_course_summary")
    course_instructors = cursor.fetchall()

    # Dùng View vw_course_summary, sắp xếp cho bảng
    cursor.execute("SELECT * FROM vw_course_summary ORDER BY TotalClasses DESC")
    course_classes = cursor.fetchall()

    conn.close()
    return render_template('dashboard.html', 
                           total_students=total_students, 
                           total_instructors=total_instructors, 
                           total_courses=total_courses,
                           course_instructors=course_instructors,
                           course_classes=course_classes)

@app.route('/instructors', methods=['GET', 'POST'])
def manage_instructors():
    conn = get_db(); cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        email = request.form['email']
        cursor.execute("SELECT Email FROM INSTRUCTORS WHERE Email = %s", (email,))
        if cursor.fetchone():
            flash(f"Lỗi: Email '{email}' đã được đăng ký!", "danger")
        else:
            new_id = get_next_id(cursor, 'INSTRUCTORS', 'InstructorID', 'ins', 5)
            cursor.execute("INSERT INTO INSTRUCTORS (InstructorID, InstructorName, Expertise, Email) VALUES (%s, %s, %s, %s)", 
                           (new_id, request.form['name'], request.form['expertise'], email))
            conn.commit()
            flash(f"Đã thêm giảng viên! Mã GV: {new_id}", "success")
        return redirect(url_for('manage_instructors'))

    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    offset = (page - 1) * 10
    
    # Dùng View vw_instructor_stats
    cursor.execute("SELECT * FROM vw_instructor_stats WHERE InstructorName LIKE %s LIMIT 10 OFFSET %s", (f'%{search}%', offset))
    instructors = cursor.fetchall()
    
    conn.close()
    return render_template('instructors.html', instructors=instructors, page=page, search=search)

@app.route('/students', methods=['GET', 'POST'])
def manage_students():
    conn = get_db(); cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        email = request.form['email']
        phone = request.form['phone']
        cursor.execute("SELECT Email FROM LEARNERS WHERE Email = %s", (email,))
        if cursor.fetchone():
            flash(f"Lỗi: Email '{email}' đã tồn tại!", "danger")
        else:
            khoa = request.form['khoa']
            new_id = get_next_student_id(cursor, khoa)
            cursor.execute("INSERT INTO LEARNERS (LearnerID, LearnerName, Email, PhoneNumber) VALUES (%s, %s, %s, %s)", 
                           (new_id, request.form['name'], email, phone))
            conn.commit()
            flash(f"Đã tạo hồ sơ sinh viên! Mã SV: {new_id}", "success")
        return redirect(url_for('manage_students'))

    page = int(request.args.get('page', 1))
    search = request.args.get('search', '')
    offset = (page - 1) * 10
    cursor.execute("SELECT * FROM LEARNERS WHERE LearnerName LIKE %s LIMIT 10 OFFSET %s", (f'%{search}%', offset))
    students = cursor.fetchall()
    conn.close()
    return render_template('students.html', students=students, page=page, search=search)

@app.route('/courses', methods=['GET', 'POST'])
def manage_courses():
    conn = get_db(); cursor = conn.cursor(dictionary=True)
    if request.method == 'POST' and 'add_course' in request.form:
        new_id = get_next_id(cursor, 'COURSES', 'CourseID', 'crs', 5)
        cursor.execute("INSERT INTO COURSES (CourseID, CourseName, Description) VALUES (%s, %s, %s)", 
                       (new_id, request.form['course_name'], request.form['description']))
        conn.commit()
        flash(f"Mở mã môn học thành công: {new_id}", "success")
        return redirect(url_for('manage_courses'))

    cursor.execute("SELECT * FROM COURSES")
    all_courses = cursor.fetchall()
    
    cursor.execute("SELECT * FROM INSTRUCTORS")
    instructors_list = cursor.fetchall()

    selected_course_id = request.args.get('course_id')
    selected_course = None
    
    if selected_course_id:
        cursor.execute("SELECT * FROM COURSES WHERE CourseID = %s", (selected_course_id,))
        selected_course = cursor.fetchone()
        if selected_course:
            # Dùng View vw_lecture_list
            cursor.execute("SELECT * FROM vw_lecture_list WHERE CourseID = %s", (selected_course_id,))
            selected_course['lectures'] = cursor.fetchall()
            
            # Dùng View vw_assignment_details
            cursor.execute("SELECT * FROM vw_assignment_details WHERE CourseID = %s", (selected_course_id,))
            selected_course['assignments'] = cursor.fetchall()
            
    conn.close()
    return render_template('courses.html', all_courses=all_courses, selected_course=selected_course, instructors_list=instructors_list)

@app.route('/assignments')
def manage_assignments():
    conn = get_db(); cursor = conn.cursor(dictionary=True)
    
    page = int(request.args.get('page', 1))
    offset = (page - 1) * 10
    
    # Dùng View vw_assignment_details
    cursor.execute("SELECT * FROM vw_assignment_details LIMIT 10 OFFSET %s", (offset,))
    assignments_list = cursor.fetchall()
    
    selected_asg_id = request.args.get('assignment_id')
    asg_details = None
    enrolled_students = []
    
    if selected_asg_id:
        cursor.execute("SELECT * FROM vw_assignment_details WHERE AssignmentID = %s", (selected_asg_id,))
        asg_details = cursor.fetchone()
        
        if asg_details:
            # Dùng View vw_enrollment_info
            cursor.execute("SELECT LearnerID, LearnerName, StudentEmail as Email FROM vw_enrollment_info WHERE AssignmentID = %s", (selected_asg_id,))
            enrolled_students = cursor.fetchall()
            
    conn.close()
    return render_template('assignments.html', 
                           assignments_list=assignments_list, 
                           page=page, 
                           asg_details=asg_details, 
                           enrolled_students=enrolled_students)

@app.route('/assign_class', methods=['POST'])
def assign_class():
    conn = get_db(); cursor = conn.cursor(dictionary=True)
    instr_id = request.form['instructor_id']
    shift = request.form['shift']
    
    cursor.execute("SELECT CourseID FROM COURSE_INSTRUCTOR WHERE InstructorID = %s AND Shift = %s", (instr_id, shift))
    if cursor.fetchone():
        flash("Cảnh báo: Giảng viên đã có lịch dạy vào ca này!", "danger")
    else:
        assign_id = get_next_id(cursor, 'COURSE_INSTRUCTOR', 'AssignmentID', 'asg', 7)
        cursor.execute("INSERT INTO COURSE_INSTRUCTOR (AssignmentID, Shift, InstructorID, CourseID) VALUES (%s, %s, %s, %s)", 
                       (assign_id, shift, instr_id, request.form['course_id']))
        conn.commit()
        flash(f"Mở lớp thành công! Mã phân công: {assign_id}", "success")
    conn.close()
    return redirect(url_for('manage_courses'))

@app.route('/enroll', methods=['GET'])
def enroll():
    conn = get_db(); cursor = conn.cursor(dictionary=True)
    learner_id = request.args.get('learner_id')
    student = None
    enrolled_classes = []
    grouped_courses = {}

    if learner_id:
        cursor.execute("SELECT * FROM LEARNERS WHERE LearnerID = %s", (learner_id,))
        student = cursor.fetchone()

        if student:
            # Dùng View vw_enrollment_info lấy TKB
            cursor.execute("SELECT EnrollmentID, CourseName, Shift, InstructorName, AssignmentID FROM vw_enrollment_info WHERE LearnerID = %s", (learner_id,))
            enrolled_classes = cursor.fetchall()

            # Dùng View vw_assignment_details để hiển thị các môn mở
            cursor.execute("SELECT CourseID, CourseName, AssignmentID, Shift, InstructorName FROM vw_assignment_details ORDER BY CourseName, Shift")
            all_classes = cursor.fetchall()

            for cls in all_classes:
                cid = cls['CourseID']
                if cid not in grouped_courses:
                    grouped_courses[cid] = {'CourseName': cls['CourseName'], 'classes': []}
                grouped_courses[cid]['classes'].append(cls)
        else:
            flash(f"Không tìm thấy mã sinh viên: {learner_id}", "danger")

    conn.close()
    return render_template('enroll.html', student=student, grouped_courses=grouped_courses, 
                           enrolled_classes=enrolled_classes, search_id=learner_id)

@app.route('/enroll_action', methods=['POST'])
def enroll_action():
    conn = get_db(); cursor = conn.cursor(dictionary=True)
    learner_id = request.form['learner_id']
    assignment_id = request.form['assignment_id']
    
    cursor.execute("SELECT * FROM ENROLLMENTS WHERE LearnerID = %s AND AssignmentID = %s", (learner_id, assignment_id))
    if cursor.fetchone():
        flash("Sinh viên đã đăng ký lớp học phần này rồi!", "warning")
    else:
        cursor.execute("SELECT Shift FROM COURSE_INSTRUCTOR WHERE AssignmentID = %s", (assignment_id,))
        new_shift = cursor.fetchone()['Shift']
        
        # Dùng View vw_enrollment_info kiểm tra trùng lịch
        cursor.execute("SELECT Shift FROM vw_enrollment_info WHERE LearnerID = %s", (learner_id,))
        enrolled_shifts = [row['Shift'] for row in cursor.fetchall()]
        
        if new_shift in enrolled_shifts:
            flash(f"Lỗi: Trùng lịch! Sinh viên đã có môn khác vào ca '{new_shift}'.", "danger")
        else:
            enroll_id = get_next_id(cursor, 'ENROLLMENTS', 'EnrollmentID', 'enr', 7)
            today = datetime.date.today().strftime('%Y-%m-%d')
            cursor.execute("INSERT INTO ENROLLMENTS (EnrollmentID, EnrollmentDate, LearnerID, AssignmentID) VALUES (%s, %s, %s, %s)", 
                           (enroll_id, today, learner_id, assignment_id))
            conn.commit()
            flash("Ghi nhận đăng ký thành công!", "success")
            
    conn.close()
    return redirect(url_for('enroll', learner_id=learner_id))

@app.route('/unenroll', methods=['POST'])
def unenroll():
    conn = get_db(); cursor = conn.cursor()
    enroll_id = request.form['enroll_id']
    learner_id = request.form['learner_id']
    cursor.execute("DELETE FROM ENROLLMENTS WHERE EnrollmentID = %s", (enroll_id,))
    conn.commit()
    conn.close()
    flash("Đã hủy học phần!", "info")
    return redirect(url_for('enroll', learner_id=learner_id))

if __name__ == '__main__':
    app.run(debug=True, port=5000)