from django.db import models
from django.contrib.auth.models import User

class ClassGroup(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "Form 1A"
    teacher = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_groups')

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    student_id = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    class_group = models.ForeignKey(ClassGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    admission_date = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    phone_contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    class_group = models.ForeignKey('ClassGroup', on_delete=models.CASCADE, related_name='subjects', null=True)  # NEW

    def __str__(self):
        return f"{self.name} ({self.class_group.name})"



class Exam(models.Model):
    name = models.CharField(max_length=100)  # e.g., "Midterm 2025"
    date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.date}"


class Result(models.Model):
    GRADE_CHOICES = [
        ('A', 'Advanced'),
        ('P', 'Proficient'),
        ('B', 'Basic'),
        ('N', 'Needs Improvement'),
        ('AB', 'Absent'),
        ('NA', 'Not Applicable'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='results')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True, null=True)
    

    def __str__(self):
        return f"{self.student} | {self.subject} | {self.exam} | {self.score} | {self.get_grade_display()}"


class DisciplinaryRecord(models.Model):
    STATUS_CHOICES = [
        ('counselled', 'Counselled'),
        ('warning', 'Last Warning'),
        ('fas', 'Find Another School'),  
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    incident = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    reported_by = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.get_status_display()} on {self.date}"


class RatedAssessment(models.Model):
    RATING_CHOICES = [
        (3, 'Excellent'),
        (2, 'Satisfactory'),
        (1, 'Needs Improvement'),
    ]

    CATEGORY_CHOICES = [
        ('general', 'General'),
        ('co_curricular', 'Co-Curricular'),
        ('extra_curricular', 'Extra-Curricular'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    area = models.CharField(max_length=100)  # e.g. "Music", "Behavior", "Football"
    rating = models.IntegerField(choices=RATING_CHOICES)
    remark = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('student', 'category', 'area')

    def __str__(self):
        return f"{self.student} | {self.area} ({self.get_rating_display()}) [{self.get_category_display()}]"



class Attendance(models.Model):
    TERM_CHOICES = [
        ('Term 1', 'Term 1'),
        ('Term 2', 'Term 2'),
        ('Term 3', 'Term 3'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    term = models.CharField(max_length=10, choices=TERM_CHOICES,null=True)
    year = models.PositiveIntegerField(null=True)
    attendance_note = models.CharField(max_length=100)  # e.g. "85/90 days"
    date_recorded = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'term', 'year')

    def __str__(self):
        return f"{self.student} - {self.attendance_note} ({self.term} {self.year})"

