from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from core.models import Course, Session, CustomUser, Student, Student_Notification, Student_Feedback, Attendance, Attendance_Report, Result
from django.contrib import messages
from django.db.models import Q

@login_required(login_url='/')
def HOME(request):
    student_count = Student.objects.all().count()
    student_gender_male = Student.objects.filter(gender='Male').count()
    student_gender_female = Student.objects.filter(gender='Female').count()
    context = {
        'student_count': student_count,
        'student_gender_male': student_gender_male,
        'student_gender_female': student_gender_female,
    }
    return render(request, 'hod/home.html', context)

def ADD_STUDENT(request):
    courses = Course.objects.all()
    sessions = Session.objects.all()

    if request.method == 'POST':
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        address = request.POST.get('address')
        password = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
            messages.warning(request, 'Email is already taken')
            return redirect('add_student')
        if CustomUser.objects.filter(username=username).exists():
            messages.warning(request, 'Username is already taken')
            return redirect('add_student')
        else:
            user = CustomUser(
                first_name = first_name,
                last_name = last_name,
                username = username,
                email = email,
                profile_pic = profile_pic,
                user_type = 3
            )
            user.set_password(password)
            user.save()
            course = Course.objects.get(id=course_id)
            session = Session.objects.get(id=session_id)
            student = Student(
                admin = user,
                address = address,
                session_id = session,
                course_id = course,
                gender = gender,
            )
            student.save()
            messages.success(request, user.first_name + " " + user.last_name + 'Are Successfully added !')
            return redirect('add_student')
        
    context = {
        'courses': courses,
        'sessions': sessions,
    }
    return render(request, 'hod/add_student.html', context)

def VIEW_STUDENT(request):
    students = Student.objects.all()
    context = {
        'students': students,
    }
    return render(request, 'hod/view_student.html', context)

def EDIT_STUDENT(request, id):
    student = Student.objects.get(id=id)
    courses = Course.objects.all()
    sessions = Session.objects.all()
    context = {
        'student': student,
        'courses': courses,
        'sessions': sessions,
    }
    return render(request, 'hod/edit_student.html', context)

def UPDATE_STUDENT(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        profile_pic = request.FILES.get('profile_pic')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        gender = request.POST.get('gender')
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        address = request.POST.get('address')
        password = request.POST.get('password')
        user = CustomUser.objects.get(id=student_id)
        if profile_pic != None and profile_pic != "":
            user.profile_pic = profile_pic
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        if password != None and password != "":
            user.set_password(password)
        user.save()
        student = Student.objects.get(admin=student_id)
        student.address = address
        if gender != None and gender != "":
            student.gender = gender
        if course_id != None and course_id != "":
            course = Course.objects.get(id=course_id)
            student.course_id = course
        if session_id != None and session_id != "":
            session = Session.objects.get(id=session_id)
            student.session_id = session
        student.save()
        messages.success(request, "Records are successfully updated !")
        return redirect('view_student')
    return render(request, 'hod/edit_student.html')

def DELETE_STUDENT(request, id):
    user = CustomUser.objects.get(id=id)
    user.delete()
    messages.success(request, "Record is successfully deleted!")
    return redirect('view_student')

def STUDENT_SEND_NOTIFICATION(request):
    student = Student.objects.all()
    notification = Student_Notification.objects.all()
    context = {
        'students': student,
        'notification': notification,
    }
    return render(request, 'hod/student_notification.html', context)

def STUDENT_SAVE_NOTIFICATION(request):
    if request.method == "POST":
        message = request.POST.get('message')
        student_id = request.POST.get('student_id')
        student = Student.objects.get(admin=student_id)
        stud_notification = Student_Notification(
            student_id = student,
            message = message,
        )
        stud_notification.save()
        messages.success(request, "Student Notification is Successfully Sent")
        return redirect('student_send_notification')
    
def STUDENT_FEEDBACK(request):
    feedback = Student_Feedback.objects.all()
    feedback_history = Student_Feedback.objects.all().order_by('-id')[0:5]
    context = {
        'feedback': feedback,
        'feedback_history': feedback_history,
    }
    return render(request, 'hod/student_feedback.html', context)

def REPLY_STUDENT_FEEDBACK(request):
    if request.method == 'POST':
        feedback_id = request.POST.get('feedback_id')
        feedback_reply = request.POST.get('message')
        feedback = Student_Feedback.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_reply
        feedback.save()
        messages.success(request, "Feedback sent successfully")
        return redirect('hod_student_feedback')
    
def HOD_TAKE_ATTENDANCE(request):
    hod = CustomUser.objects.get(email=request.user.email)
    course = Course.objects.all()
    session = Session.objects.all()
    action = request.GET.get('action')
    get_course = None
    get_session = None
    student = None
    if action is not None:
        if request.method == 'POST':
            course_id = request.POST.get('course_id')
            session_id = request.POST.get('session_id')
            get_course = Course.objects.get(id=course_id)
            get_session = Session.objects.get(id=session_id)
            student = Student.objects.filter(Q(course_id=course_id) & Q(session_id=session_id)) 
    context = {
        'course': course,
        'session': session,
        'get_course': get_course,
        'get_session':get_session,
        'action': action,
        'student': student,
    }
    return render(request, 'hod/take_attendance.html', context)

def HOD_SAVE_ATTENDANCE(request):
    if request.method == 'POST':
        course_id = request.POST.get('course_id')
        session_id = request.POST.get('session_id')
        attendance_date = request.POST.get('attendance_date')
        student_id = request.POST.getlist('student')
        get_course = Course.objects.get(id=course_id)
        get_session = Session.objects.get(id=session_id)

        attendance = Attendance(
            course_id = get_course,
            session_id = get_session,
            attendance_date = attendance_date,
        )
        attendance.save()
        for i in student_id:
            stud_id = i
            int_stud = int(stud_id)
            p_student = Student.objects.get(id=int_stud)
            attendance_report = Attendance_Report(
                student_id = p_student,
                attendance_id = attendance,
            )
            attendance_report.save()
    return redirect('hod_take_attendance')

def HOD_VIEW_ATTENDANCE(request):
    course = Course.objects.all()
    session = Session.objects.all()
    action = request.GET.get('action')
    get_course = None
    get_session = None
    attendance_date = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            course_id = request.POST.get('course_id')
            session_id = request.POST.get('session_id')
            attendance_date = request.POST.get('attendance_date')
            get_course = Course.objects.get(id=course_id)
            get_session = Session.objects.get(id=session_id)
            attendance = Attendance.objects.get(course_id=get_course, attendance_date=attendance_date)
            attendance_id = attendance.id
            attendance_report = Attendance_Report.objects.filter(attendance_id=attendance_id)
    context = {
        'course': course,
        'session': session,
        'action': action,
        'get_course': get_course,
        'get_session': get_session,
        'attendance_date': attendance_date,
        'attendance_report': attendance_report,
    }
    return render(request, 'hod/view_attendance.html', context)

def HOD_ADD_RESULT(request):
    subject = Course.objects.all()
    session_year = Session.objects.all()
    action = request.GET.get('action')
    get_subject = None
    get_session_year = None
    students = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            session_year_id = request.POST.get('session_year_id')
            get_subject = Course.objects.get(id=subject_id)
            get_session_year = Session.objects.get(id=session_year_id)
            subject = Course.objects.get(id=subject_id)
            student_id = subject.id
            students = Student.objects.filter(course_id = student_id)
    context = {
        'subjects': subject,
        'session_year': session_year,
        'action': action,
        'get_subject': get_subject,
        'get_session': get_session_year,
        'students': students,
    }
    return render(request, 'hod/add_result.html', context)

def HOD_SAVE_RESULT(request):
    if request.method == "POST":
        subject_id = request.POST.get('subject_id')
        session_year_id = request.POST.get('session_year_id')
        student_id = request.POST.get('student_id')
        assignment_mark = request.POST.get('assignment_mark')
        exam_mark = request.POST.get('Exam_mark')

        get_student = Student.objects.get(admin=student_id)
        get_subject = Course.objects.get(id=subject_id)
        check_exists = Result.objects.filter(subject_id=get_subject, student_id=get_student).exists()
        if check_exists:
            result = Result.objects.get(subject_id=get_subject, student_id=get_student)
            result.assignment_mark = assignment_mark
            result.exam_mark = exam_mark
            messages.success(request, "Result Updated Successfully")
            result.save()
            return redirect('hod_add_result')
        else:
            result = Result(
                student_id = get_student,
                subject_id = get_subject,
                exam_mark = exam_mark,
                assignment_mark = assignment_mark,
            )
            messages.success(request, "Result Added Successfully")
            result.save()
            return redirect('hod_add_result')