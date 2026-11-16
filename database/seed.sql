INSERT OR IGNORE INTO Departments VALUES
(1, 'Information Technology'),
(2, 'Computer Science'),
(3, 'Electronics'),
(4, 'Mechanical');

INSERT OR IGNORE INTO Students VALUES
(101, 'Rahul Sharma', 'rahul@example.com', 1, 2),
(102, 'Priya Verma', 'priya@example.com', 2, 3),
(103, 'Aman Gupta', 'aman@example.com', 1, 2),
(104, 'Neha Singh', 'neha@example.com', 3, 1),
(105, 'Rohit Kumar', 'rohit@example.com', 2, 4),
(106, 'Sneha Jain', 'sneha@example.com', 1, 3),
(107, 'Arjun Mehta', 'arjun@example.com', 4, 2),
(108, 'Kavya Rao', 'kavya@example.com', 2, 1),
(109, 'Ishita Das', 'ishita@example.com', 3, 2),
(110, 'Dev Patel', 'dev@example.com', 1, 4);

INSERT OR IGNORE INTO Courses VALUES
(201, 'IT201', 'Database Management Systems', 4),
(202, 'IT202', 'Object Oriented Programming', 4),
(203, 'IT203', 'Data Structures', 4),
(204, 'IT204', 'Operating Systems', 3),
(205, 'IT205', 'Computer Networks', 3);

INSERT OR IGNORE INTO Enrollments VALUES
(301,101,201,'Odd',2026),(302,101,202,'Odd',2026),
(303,102,201,'Odd',2026),(304,102,203,'Odd',2026),
(305,103,201,'Odd',2026),(306,103,204,'Odd',2026),
(307,104,202,'Odd',2026),(308,105,201,'Odd',2026),
(309,105,205,'Odd',2026),(310,106,203,'Odd',2026),
(311,107,204,'Odd',2026),(312,108,201,'Odd',2026),
(313,109,202,'Odd',2026),(314,110,203,'Odd',2026);

INSERT OR IGNORE INTO Marks VALUES
(401,301,88,'A'),(402,302,91,'A+'),
(403,303,78,'B+'),(404,304,85,'A'),
(405,305,95,'A+'),(406,306,72,'B'),
(407,307,89,'A'),(408,308,67,'C'),
(409,309,82,'A'),(410,310,93,'A+'),
(411,311,75,'B'),(412,312,87,'A'),
(413,313,90,'A+'),(414,314,81,'A');
