-- 1. TẠO CƠ SỞ DỮ LIỆU VÀ CÁC BẢNG (Giữ nguyên cấu trúc gốc của bạn)
CREATE DATABASE IF NOT EXISTS UniversityDB;
USE UniversityDB;

CREATE TABLE IF NOT EXISTS INSTRUCTORS (
    InstructorID VARCHAR(15) PRIMARY KEY,
    InstructorName VARCHAR(100) NOT NULL,
    Expertise VARCHAR(50),
    Email VARCHAR(100) UNIQUE
);

CREATE TABLE IF NOT EXISTS COURSES (
    CourseID VARCHAR(15) PRIMARY KEY,
    CourseName VARCHAR(150) NOT NULL,
    Description TEXT
);

CREATE TABLE IF NOT EXISTS LEARNERS (
    LearnerID VARCHAR(15) PRIMARY KEY,
    LearnerName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE,
    PhoneNumber VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS COURSE_INSTRUCTOR (
    AssignmentID VARCHAR(15) PRIMARY KEY,
    Shift VARCHAR(20),
    InstructorID VARCHAR(15),
    CourseID VARCHAR(15),
    FOREIGN KEY (InstructorID) REFERENCES INSTRUCTORS(InstructorID),
    FOREIGN KEY (CourseID) REFERENCES COURSES(CourseID)
);

CREATE TABLE IF NOT EXISTS LECTURES (
    LectureID VARCHAR(15) PRIMARY KEY,
    Title VARCHAR(255),
    Content TEXT,
    CourseID VARCHAR(15),
    FOREIGN KEY (CourseID) REFERENCES COURSES(CourseID)
);

CREATE TABLE IF NOT EXISTS ENROLLMENTS (
    EnrollmentID VARCHAR(15) PRIMARY KEY,
    EnrollmentDate DATE,
    LearnerID VARCHAR(15),
    AssignmentID VARCHAR(15),
    FOREIGN KEY (LearnerID) REFERENCES LEARNERS(LearnerID),
    FOREIGN KEY (AssignmentID) REFERENCES COURSE_INSTRUCTOR(AssignmentID)
);

-- ==========================================
-- 2. TẠO CÁC VIEWS ĐỂ TỐI ƯU HÓA TRUY VẤN
-- ==========================================

-- View 1: Thống kê số GV và lớp học của từng môn (Cho Dashboard)
CREATE OR REPLACE VIEW vw_course_summary AS
SELECT 
    c.CourseID, 
    c.CourseName, 
    COUNT(DISTINCT ci.InstructorID) AS TotalInstructors,
    COUNT(ci.AssignmentID) AS TotalClasses
FROM COURSES c
LEFT JOIN COURSE_INSTRUCTOR ci ON c.CourseID = ci.CourseID
GROUP BY c.CourseID, c.CourseName;

-- View 2: Chi tiết lớp tín chỉ (Cho phần Assignments và Courses)
CREATE OR REPLACE VIEW vw_assignment_details AS
SELECT 
    ci.AssignmentID, 
    ci.Shift, 
    ci.CourseID,
    c.CourseName, 
    ci.InstructorID,
    i.InstructorName
FROM COURSE_INSTRUCTOR ci
JOIN COURSES c ON ci.CourseID = c.CourseID
JOIN INSTRUCTORS i ON ci.InstructorID = i.InstructorID;

-- View 3: Thông tin sinh viên đăng ký học (Cho phần Enroll)
CREATE OR REPLACE VIEW vw_enrollment_info AS
SELECT 
    e.EnrollmentID,
    e.EnrollmentDate,
    e.LearnerID,
    l.LearnerName,
    l.Email AS StudentEmail,
    ad.AssignmentID,
    ad.CourseName,
    ad.Shift,
    ad.InstructorName
FROM ENROLLMENTS e
JOIN LEARNERS l ON e.LearnerID = l.LearnerID
JOIN vw_assignment_details ad ON e.AssignmentID = ad.AssignmentID;

-- View 4: Danh sách bài giảng kèm thông tin môn học
CREATE OR REPLACE VIEW vw_lecture_list AS
SELECT 
    l.LectureID, 
    l.Title, 
    l.Content, 
    c.CourseID, 
    c.CourseName
FROM LECTURES l
JOIN COURSES c ON l.CourseID = c.CourseID;

-- View 5: Thống kê Giảng viên kèm số lớp đang dạy
CREATE OR REPLACE VIEW vw_instructor_stats AS
SELECT 
    i.InstructorID, 
    i.InstructorName, 
    i.Expertise, 
    i.Email,
    COUNT(ci.AssignmentID) AS TotalClasses
FROM INSTRUCTORS i
LEFT JOIN COURSE_INSTRUCTOR ci ON i.InstructorID = ci.InstructorID
GROUP BY i.InstructorID, i.InstructorName, i.Expertise, i.Email;