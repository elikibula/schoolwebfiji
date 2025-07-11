from django import forms
from student_performance.models import Result, Subject, Exam, Student, ClassGroup, RatedAssessment, DisciplinaryRecord, Attendance

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'attendance_note', 'term', 'year']  # ✅ Only valid fields

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['student'].queryset = Student.objects.filter(class_group__teacher=user)


class DisciplinaryForm(forms.ModelForm):
    class Meta:
        model = DisciplinaryRecord
        fields = ['student', 'incident', 'status', 'reported_by']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            try:
                class_group = ClassGroup.objects.get(teacher=user)
                self.fields['student'].queryset = Student.objects.filter(class_group=class_group)
                self.fields['reported_by'].initial = user.get_full_name()
            except ClassGroup.DoesNotExist:
                self.fields['student'].queryset = Student.objects.none()



class AssessmentForm(forms.ModelForm):
    class Meta:
        model = RatedAssessment
        fields = ['student', 'category', 'area', 'rating', 'remark']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user:
            try:
                class_group = ClassGroup.objects.get(teacher=user)
                self.fields['student'].queryset = Student.objects.filter(class_group=class_group)
            except ClassGroup.DoesNotExist:
                self.fields['student'].queryset = Student.objects.none()


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name',
            'last_name',
            'student_id',
            'date_of_birth',
            'admission_date',
            'address',
            'phone_contact'
        ]

class ResultForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ['student', 'subject', 'exam', 'score', 'grade']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            try:
                class_group = ClassGroup.objects.get(teacher=user)
                self.fields['student'].queryset = Student.objects.filter(class_group=class_group)
                self.fields['subject'].queryset = Subject.objects.filter(class_group=class_group)
                self.fields['exam'].queryset = Exam.objects.all()
            except ClassGroup.DoesNotExist:
                self.fields['student'].queryset = Student.objects.none()
                self.fields['subject'].queryset = Subject.objects.none()


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['student', 'term', 'year', 'attendance_note']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['student'].queryset = Student.objects.filter(class_group__teacher=user)
