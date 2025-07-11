from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.db.models import Count

from student_performance.models import (
    ClassGroup, Student, Result, RatedAssessment,
    DisciplinaryRecord, Attendance
)

from .forms import StudentForm, ResultForm, AssessmentForm, DisciplinaryForm, AttendanceForm
from weasyprint import HTML
import tempfile

@login_required
def export_student_report_pdf(request, pk):
    student = get_object_or_404(Student, pk=pk)
    try:
        class_group = ClassGroup.objects.get(teacher=request.user)
    except ClassGroup.DoesNotExist:
        class_group = None

    results = Result.objects.filter(student=student)
    assessments = RatedAssessment.objects.filter(student=student)
    disciplinary = DisciplinaryRecord.objects.filter(student=student)
    attendance = Attendance.objects.filter(student=student)

    context = {
        'student': student,
        'class_group': class_group,
        'term': 'Term 2',  # You can dynamically pass this or fetch from model
        'year': 2025,      # Likewise for year
        'teacher': request.user,
        'results': results,
        'assessments': assessments,
        'disciplinary': disciplinary,
        'attendance': attendance,
    }

    html_string = render_to_string('reports/student_report.html', context)
    html = HTML(string=html_string)

    # Create PDF in memory
    result = html.write_pdf()

    # Send the PDF as a response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=student_{student.pk}_report.pdf'
    response.write(result)

    return response


# 🔁 Reusable annotated student query
def get_annotated_students(class_group):
    return Student.objects.filter(class_group=class_group).annotate(
        result_count=Count('results'),
        disciplinary_count=Count('disciplinaryrecord'),
        assessment_count=Count('ratedassessment'),
        attendance_count=Count('attendance')
    )


# 🧑‍🏫 Dashboard View
@login_required
def teacher_dashboard(request):
    teacher = request.user
    student_form = StudentForm()

    try:
        class_group = ClassGroup.objects.get(teacher=teacher)
        students = get_annotated_students(class_group)
    except ClassGroup.DoesNotExist:
        class_group = None
        students = Student.objects.none()

    context = {
        'class_group': class_group,
        'students': students,
        'student_form': student_form
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)


# ➕ Add Student
@login_required
def add_student(request):
    data = dict()
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            try:
                class_group = ClassGroup.objects.get(teacher=request.user)
                student.class_group = class_group
                student.save()
                data['form_is_valid'] = True

                # Refresh student list
                students = get_annotated_students(class_group)
                data['html_student_list'] = render_to_string(
                    'dashboard/includes/partial_student_list.html',
                    {'students': students}
                )
            except ClassGroup.DoesNotExist:
                data['form_is_valid'] = False
                data['error'] = "You are not assigned to any class."
        else:
            data['form_is_valid'] = False
            data['html_form'] = render_to_string(
                'dashboard/includes/partial_student_create.html',
                {'student_form': form},
                request=request
            )
    else:
        form = StudentForm()

    if 'html_form' not in data:
        context = {'student_form': form}
        data['html_form'] = render_to_string(
            'dashboard/includes/partial_student_create.html',
            context,
            request=request
        )

    return JsonResponse(data)


# 📝 Add Result
@login_required
def add_result(request):
    data = dict()
    if request.method == 'POST':
        form = ResultForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = ResultForm(user=request.user)

    context = {'result_form': form}
    data['html_form'] = render_to_string(
        'dashboard/includes/partial_result_create.html',
        context,
        request=request
    )
    return JsonResponse(data)


# ✏️ Add Assessment
@login_required
def add_assessment(request):
    data = dict()
    if request.method == 'POST':
        form = AssessmentForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = AssessmentForm(user=request.user)

    context = {'assessment_form': form}
    data['html_form'] = render_to_string(
        'dashboard/includes/partial_assessment_create.html',
        context,
        request=request
    )
    return JsonResponse(data)


# 🚨 Add Disciplinary Record
@login_required
def add_disciplinary(request):
    data = dict()
    if request.method == 'POST':
        form = DisciplinaryForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = DisciplinaryForm(user=request.user)

    context = {'disciplinary_form': form}
    data['html_form'] = render_to_string(
        'dashboard/includes/partial_disciplinary_create.html',
        context,
        request=request
    )
    return JsonResponse(data)


# 📄 Student Results Modal View
@login_required
def student_results_modal(request, pk):
    student = get_object_or_404(Student, pk=pk)
    results = Result.objects.filter(student=student)
    return render(request, 'dashboard/modals/student_results.html', {
        'student': student,
        'results': results,
    })


# 🟡 Assessment Modal View
@login_required
def student_assessment_modal(request, pk):
    student = get_object_or_404(Student, pk=pk)
    assessments = RatedAssessment.objects.filter(student=student)
    return render(request, 'dashboard/modals/student_assessment.html', {
        'student': student,
        'assessments': assessments,
    })


# 🔴 Disciplinary Modal View
@login_required
def student_disciplinary_modal(request, pk):
    student = get_object_or_404(Student, pk=pk)
    disciplinary = DisciplinaryRecord.objects.filter(student=student)
    return render(request, 'dashboard/modals/student_disciplinary.html', {
        'student': student,
        'disciplinary': disciplinary,
    })


# ⚪ Attendance Modal View
@login_required
def student_attendance_modal(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendance = Attendance.objects.filter(student=student)
    return render(request, 'dashboard/modals/student_attendance.html', {
        'student': student,
        'attendance': attendance,
    })

@login_required
def add_attendance(request):
    data = dict()
    if request.method == 'POST':
        form = AttendanceForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False
    else:
        form = AttendanceForm(user=request.user)

    context = {'attendance_form': form}
    data['html_form'] = render_to_string(
        'dashboard/includes/partial_attendance_create.html',
        context,
        request=request
    )
    return JsonResponse(data)

@login_required
def student_attendance_modal(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendances = Attendance.objects.filter(student=student)
    return render(request, 'dashboard/modals/student_attendance.html', {
        'student': student,
        'attendances': attendances,
    })

