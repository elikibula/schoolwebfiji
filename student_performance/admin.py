from django.contrib import admin
from .models import (
    ClassGroup,
    Student,
    Subject,
    Exam,
    Result,
    DisciplinaryRecord,
    RatedAssessment,
    Attendance
)

@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher')
    search_fields = ('name',)
    list_filter = ('teacher',)

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name', 'class_group')
    search_fields = ('first_name', 'last_name', 'student_id')
    list_filter = ('class_group',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'date')
    search_fields = ('name',)

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'exam', 'score', 'grade')
    list_filter = ('exam', 'subject', 'grade')
    search_fields = ('student__first_name', 'student__last_name', 'subject__name')

@admin.register(DisciplinaryRecord)
class DisciplinaryRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status', 'reported_by')
    list_filter = ('status',)
    search_fields = ('student__first_name', 'student__last_name', 'incident')

@admin.register(RatedAssessment)
class RatedAssessmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'category', 'area', 'rating')
    list_filter = ('category', 'rating')
    search_fields = ('student__first_name', 'student__last_name', 'area')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'attendance_note', 'date_recorded')
    search_fields = ('student__first_name', 'student__last_name', 'attendance_note')
    list_filter = ('date_recorded',)
