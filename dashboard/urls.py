from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),

    path('add-student/', views.add_student, name='add_student'),
    path('add-result/', views.add_result, name='add_result'),
    path('add-assessment/', views.add_assessment, name='add_assessment'),
    path('add-disciplinary/', views.add_disciplinary, name='add_disciplinary'),
    path('add-attendance/', views.add_attendance, name='add_attendance'),

    path('student/<int:pk>/results/', views.student_results_modal, name='student_results_modal'),
    path('student/<int:pk>/assessments/', views.student_assessment_modal, name='student_assessment_modal'),
    path('student/<int:pk>/disciplinary/', views.student_disciplinary_modal, name='student_disciplinary_modal'),
    path('student/<int:pk>/attendance/', views.student_attendance_modal, name='student_attendance_modal'),
    path('student/<int:pk>/export-pdf/', views.export_student_report_pdf, name='export_student_report_pdf'),

]
