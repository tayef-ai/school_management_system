from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    USER = (
        ('1','HOD'),
        ('2','STAFF'),
        ('3','STUDENT'),
    )
    user_type = models.CharField(choices=USER, max_length=50, default=1)
    profile_pic = models.ImageField(upload_to='media/profile_pic')

class Course(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Session(models.Model):
    session_start = models.CharField(max_length=100)
    session_end = models.CharField(max_length=100)
    def __str__(self):
        return self.session_start + " To " + self.session_end
    

class Student(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.TextField()
    gender = models.CharField(max_length=100)
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    session_id = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.admin.first_name + ' ' + self.admin.last_name
    
class Student_Notification(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True)
    status = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.student_id.admin.first_name
    
class Student_Feedback(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add = True, null=True)
    updated_at = models.DateTimeField(auto_now_add = True, null=True)

    def __str__(self):
        return self.student_id.admin.first_name + " " + self.student_id.admin.last_name

class Attendance(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    session_id = models.ForeignKey(Session, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.course_id.name

class Attendance_Report(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.student_id.admin.first_name
    
class Result(models.Model):
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment_mark = models.IntegerField()
    exam_mark = models.IntegerField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.student_id.admin.first_name
    
    