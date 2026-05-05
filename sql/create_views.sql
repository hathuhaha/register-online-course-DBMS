CREATE DATABASE IF NOT EXISTS UniversityDB;
USE UniversityDB;

-- 1. Sửa lỗi thiếu cột Phone cho bảng Sinh viên
CREATE TABLE IF NOT EXISTS LEARNERS (
    LearnerID VARCHAR(20) PRIMARY KEY,
    LearnerName VARCHAR(255),
    Email VARCHAR(255),
    Phone VARCHAR(20) -- Đảm bảo có cột này để không bị lỗi View
);

-- 2. Các bảng còn lại
CREATE TABLE IF NOT EXISTS INSTRUCTORS (
    InstructorID VARCHAR(20) PRIMARY KEY,
    InstructorName VARCHAR(255),
    Expertise VARCHAR(255),
    Email VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS COURSES (
    CourseID VARCHAR(20) PRIMARY KEY,
    CourseName VARCHAR(255),
    Description TEXT
);

CREATE TABLE IF NOT EXISTS LECTURES (
    LectureID INT AUTO_INCREMENT PRIMARY KEY,
    CourseID VARCHAR(20),
    Title VARCHAR(255),
    Content TEXT,
    FOREIGN KEY (CourseID) REFERENCES COURSES(CourseID)
);

CREATE TABLE IF NOT EXISTS COURSE_INSTRUCTOR (
    AssignmentID VARCHAR(20) PRIMARY KEY,
    CourseID VARCHAR(20),
    InstructorID VARCHAR(20),
    Shift VARCHAR(50),
    FOREIGN KEY (CourseID) REFERENCES COURSES(CourseID),
    FOREIGN KEY (InstructorID) REFERENCES INSTRUCTORS(InstructorID)
);

CREATE TABLE IF NOT EXISTS ENROLLMENTS (
    EnrollmentID VARCHAR(20) PRIMARY KEY,
    EnrollmentDate DATE,
    LearnerID VARCHAR(20),
    AssignmentID VARCHAR(20),
    FOREIGN KEY (LearnerID) REFERENCES LEARNERS(LearnerID),
    FOREIGN KEY (AssignmentID) REFERENCES COURSE_INSTRUCTOR(AssignmentID)
);

-- 3. Tạo các VIEW thống kê (Đã sửa lỗi cột Phone)
CREATE OR REPLACE VIEW v_StudentFullList AS
SELECT l.*, COUNT(e.AssignmentID) AS EnrolledCount
FROM LEARNERS l
LEFT JOIN ENROLLMENTS e ON l.LearnerID = e.LearnerID
GROUP BY l.LearnerID;

CREATE OR REPLACE VIEW v_InstructorFullList AS
SELECT i.*, COUNT(ci.AssignmentID) AS TeachingClasses
FROM INSTRUCTORS i
LEFT JOIN COURSE_INSTRUCTOR ci ON i.InstructorID = ci.InstructorID
GROUP BY i.InstructorID;

CREATE OR REPLACE VIEW v_DetailedAssignments AS
SELECT ci.AssignmentID, ci.CourseID, c.CourseName, ci.InstructorID, i.InstructorName, ci.Shift
FROM COURSE_INSTRUCTOR ci
JOIN COURSES c ON ci.CourseID = c.CourseID
JOIN INSTRUCTORS i ON ci.InstructorID = i.InstructorID;

-- 4. Procedure Đăng ký (Fix lỗi 1093 & Bỏ Log)
DROP PROCEDURE IF EXISTS sp_EnrollStudent;
DELIMITER //
CREATE PROCEDURE sp_EnrollStudent(IN p_lid VARCHAR(20), IN p_asid VARCHAR(20), OUT p_status VARCHAR(50))
BEGIN
    DECLARE v_shift VARCHAR(50);
    DECLARE v_next_num INT;
    IF EXISTS (SELECT 1 FROM ENROLLMENTS WHERE LearnerID = p_lid AND AssignmentID = p_asid) THEN 
        SET p_status = 'DUPLICATE';
    ELSE
        SELECT Shift INTO v_shift FROM COURSE_INSTRUCTOR WHERE AssignmentID = p_asid;
        IF EXISTS (SELECT 1 FROM ENROLLMENTS e JOIN COURSE_INSTRUCTOR ci ON e.AssignmentID = ci.AssignmentID 
                   WHERE e.LearnerID = p_lid AND ci.Shift = v_shift) THEN 
            SET p_status = 'CONFLICT';
        ELSE
            SELECT IFNULL(MAX(CAST(SUBSTRING(EnrollmentID, 4) AS UNSIGNED)), 0) + 1 INTO v_next_num FROM ENROLLMENTS;
            INSERT INTO ENROLLMENTS (EnrollmentID, EnrollmentDate, LearnerID, AssignmentID) 
            VALUES (CONCAT('enr', LPAD(v_next_num, 7, '0')), CURDATE(), p_lid, p_asid);
            SET p_status = 'SUCCESS';
        END IF;
    END IF;
END //
DELIMITER ;

USE UniversityDB;

-- 1. Vá lỗi thiếu cột Phone (Giải quyết Error 1054 trong ảnh image_1f0f5f.png)
ALTER TABLE LEARNERS ADD COLUMN IF NOT EXISTS Phone VARCHAR(20);

-- 2. View Danh sách lớp tín chỉ (Chi tiết môn và giảng viên)
CREATE OR REPLACE VIEW v_DetailedAssignments AS
SELECT 
    ci.AssignmentID, ci.CourseID, c.CourseName, 
    ci.InstructorID, i.InstructorName, ci.Shift
FROM COURSE_INSTRUCTOR ci
JOIN COURSES c ON ci.CourseID = c.CourseID
JOIN INSTRUCTORS i ON ci.InstructorID = i.InstructorID;

-- 3. View thống kê Sinh viên (Đã có cột Phone)
CREATE OR REPLACE VIEW v_StudentFullList AS
SELECT l.LearnerID, l.LearnerName, l.Email, l.Phone, COUNT(e.AssignmentID) AS EnrolledCount
FROM LEARNERS l
LEFT JOIN ENROLLMENTS e ON l.LearnerID = e.LearnerID
GROUP BY l.LearnerID;

-- 4. View thống kê Giảng viên
CREATE OR REPLACE VIEW v_InstructorFullList AS
SELECT i.InstructorID, i.InstructorName, i.Expertise, i.Email, COUNT(ci.AssignmentID) AS TeachingCount
FROM INSTRUCTORS i
LEFT JOIN COURSE_INSTRUCTOR ci ON i.InstructorID = ci.InstructorID
GROUP BY i.InstructorID;