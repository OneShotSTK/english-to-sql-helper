PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS Departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Students (
    student_id INTEGER PRIMARY KEY,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department_id INTEGER NOT NULL,
    academic_year INTEGER NOT NULL CHECK (academic_year BETWEEN 1 AND 4),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

CREATE TABLE IF NOT EXISTS Courses (
    course_id INTEGER PRIMARY KEY,
    course_code TEXT NOT NULL UNIQUE,
    course_name TEXT NOT NULL,
    credits INTEGER NOT NULL CHECK (credits BETWEEN 1 AND 6)
);

CREATE TABLE IF NOT EXISTS Enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    semester TEXT NOT NULL CHECK (semester IN ('Odd', 'Even')),
    academic_year INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id) REFERENCES Courses(course_id),
    UNIQUE (student_id, course_id, semester, academic_year)
);

CREATE TABLE IF NOT EXISTS Marks (
    mark_id INTEGER PRIMARY KEY,
    enrollment_id INTEGER NOT NULL UNIQUE,
    marks REAL NOT NULL CHECK (marks BETWEEN 0 AND 100),
    grade TEXT,
    FOREIGN KEY (enrollment_id) REFERENCES Enrollments(enrollment_id)
);

CREATE INDEX IF NOT EXISTS idx_students_department ON Students(department_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_student ON Enrollments(student_id);
CREATE INDEX IF NOT EXISTS idx_enrollments_course ON Enrollments(course_id);
CREATE INDEX IF NOT EXISTS idx_marks_enrollment ON Marks(enrollment_id);

CREATE VIEW IF NOT EXISTS StudentPerformance AS
SELECT
    s.student_id,
    s.full_name,
    s.email,
    d.department_name,
    s.academic_year AS student_year,
    c.course_code,
    c.course_name,
    e.semester,
    e.academic_year AS enrollment_year,
    m.marks,
    m.grade
FROM Students AS s
JOIN Departments AS d ON d.department_id = s.department_id
JOIN Enrollments AS e ON e.student_id = s.student_id
JOIN Courses AS c ON c.course_id = e.course_id
JOIN Marks AS m ON m.enrollment_id = e.enrollment_id;
