from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Students, Teacher
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.

def FirstPageController(request):
    return HttpResponse("<h1>My First Django Project Page</h1>")

def IndexPageController(request):
    return HttpResponse("<h1>This is index Page</h1>")

def HtmlPageController(request):
    return render(request,"htmlpage.html")

def HtmlPageControllerwithData(request):
    data = "This is Data is Passing to HTML Page"
    data2 = "This is Data is Passing to HTML Page"
    return render(request, "htmlpage_with_data.html", {'data':data, 'data1':data2})

def PassingDataController(request, url_data):
    return HttpResponse("<h2> This is Data Coming Via URL : " + url_data)

def addData(request):
    return render(request, "add_data.html")

def add_student(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        file=request.FILES['profile']
        fs=FileSystemStorage()
        profile_img=fs.save(file.name, file)
        try:
            student = Students(name=request.POST.get('name', ''), email=request.POST.get('email', ''), standard=request.POST.get('standard', ''), hobbies=request.POST.get('hobbies', ''), roll_no=request.POST.get('roll_no', ''), bio=request.POST.get('bio', ''), profile_image=profile_img)
            student.save()
            messages.success(request, "Added Successfully")
        except:
            messages.error(request, "Failed to Add Student")

        return HttpResponseRedirect("/addData")

def add_teacher(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Now Allowed</h2>")
    else:
        try:
            teacher = Teacher(name=request.POST.get('name', ''), email=request.POST.get('email', ''), department=request.POST.get('department', ''))
            teacher.save()
            messages.success(request, "Added Successfully")
        except:
            messages.error(request, "Failed to Add Student")

        return HttpResponseRedirect("/addData")

def show_all_data(request):
    all_teacher = Teacher.objects.all()
    all_student = Students.objects.all()

    return render(request, "show_data.html", {'student': all_student, 'teacher': all_teacher})

def delete_student(request, student_id):
    student = Students.objects.get(id=student_id)
    student.delete()
    messages.error(request, "Deleted Successfullly")
    return HttpResponseRedirect("/show_all_data")

def update_student(request, student_id):
    student = Students.objects.get(id=student_id)
    if student == None:
        return HttpResponse("Student Not Found")
    else:
        return render(request, "student_edit.html", {'student':student})


def edit_student(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student=Students.objects.get(id=request.POST.get('id'))
        if student==None:
            return HttpResponse("<h2>Student Not Found</h2>")
        else:
            if request.FILES.get('profile')!=None:
                file = request.FILES['profile']
                fs = FileSystemStorage()
                profile_img = fs.save(file.name, file)
            else:
                profile_img = None

            if profile_img!=None:
                student.profile_image=profile_img

            student.name = request.POST.get('name', '')
            student.email = request.POST.get('email', '')
            student.standard = request.POST.get('standard', '')
            student.hobbies = request.POST.get('hobbies', '')
            student.roll_no = request.POST.get('roll_no', '')
            student.bio = request.POST.get('bio', '')
            student.save()

            messages.success(request, "Updated Successfullly")
            return HttpResponseRedirect("update_student/" + str(student.id) + "")

def LoginUser(request):
    return render(request, "login_page.html")

def RegisterUser(request):
    return render(request, "register_page.html")

def SaveUser(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        username=request.POST.get('username', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        if not (User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists()):
            User.objects.create_user(username, email, password)
            messages.success(request, "User Created Successfully")
            return HttpResponseRedirect('/register_user')
        else:
            messages.error(request, "Email or Username Already Exist")
            return HttpResponseRedirect('/register_user')

def DologinUser(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user=authenticate(username=username, password=password)
        login(request, user)

        if user != None:
            return HttpResponseRedirect('/homePage')
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect('/login_user')

def HomePage(request):
    return render(request, "home_page.html")
