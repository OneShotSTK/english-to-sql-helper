"""Small examples used to teach the model the expected SQL style."""

FEW_SHOT_EXAMPLES = [
    {
        "question": "Show all students in Information Technology.",
        "sql": """
SELECT s.student_id, s.full_name, d.department_name
FROM Students AS s
JOIN Departments AS d
  ON d.department_id = s.department_id
WHERE d.department_name = 'Information Technology';
""".strip(),
    },
    {
        "question": "Find students who scored above 80 in DBMS.",
        "sql": """
SELECT s.full_name, c.course_name, m.marks
FROM Students AS s
JOIN Enrollments AS e ON e.student_id = s.student_id
JOIN Courses AS c ON c.course_id = e.course_id
JOIN Marks AS m ON m.enrollment_id = e.enrollment_id
WHERE c.course_name = 'Database Management Systems'
  AND m.marks > 80
ORDER BY m.marks DESC;
""".strip(),
    },
    {
        "question": "Show the average marks for each course.",
        "sql": """
SELECT c.course_name, ROUND(AVG(m.marks), 2) AS average_marks
FROM Courses AS c
JOIN Enrollments AS e ON e.course_id = c.course_id
JOIN Marks AS m ON m.enrollment_id = e.enrollment_id
GROUP BY c.course_id, c.course_name
ORDER BY average_marks DESC;
""".strip(),
    },
]
