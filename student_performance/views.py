from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dashboard.forms import StudentForm
from student_performance.models import ClassGroup, Student, Result, Attendance, RatedAssessment, DisciplinaryRecord, ClassGroup 

@login_required
def teacher_dashboard(request):
    teacher = request.user
    try:
        class_group = ClassGroup.objects.get(teacher=teacher)
        students = Student.objects.filter(class_group=class_group)
    except ClassGroup.DoesNotExist:
        class_group = None
        students = None

    context = {
        'class_group': class_group,
        'students': students,
    }
    return render(request, 'dashboard/teacher_dashboard.html', context)


@login_required
def add_student(request):
    teacher = request.user

    try:
        class_group = ClassGroup.objects.get(teacher=teacher)
    except ClassGroup.DoesNotExist:
        return render(request, 'dashboard/no_class.html')

    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.class_group = class_group
            student.save()
            return redirect('teacher_dashboard')
    else:
        form = StudentForm()

    return render(request, 'dashboard/add_student.html', {'form': form})

