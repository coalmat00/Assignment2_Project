from django.shortcuts import render, redirect
from kpmbParking.models import Course, Student, Parking, Booking, Review, Class
from django.http import HttpResponseRedirect, HttpResponseNotAllowed
from django.urls import reverse
from datetime import date, datetime
import uuid
from django.db.models import Q

# Create your views here.


def main_menu(request):
    if "studentID" not in request.session:
        return redirect("index")
    else:
        # retrieve the student object from the database using the studentID in the session
        student = Student.objects.get(studentID=request.session["studentID"])
        return render(request, "main_menu.html", {"student": student})


def logout(request):
    request.session.clear()
    return redirect("index")


def index(request):
    dict = {
        "message": "",
    }
    if request.method == "POST":
        # login functionality
        s_id = request.POST.get("s_id")
        password = request.POST.get("s_password")
        student = Student.objects.filter(studentID=s_id)
        if student.exists():
            student = student.first()  # ambik yg first dulu.
            if student.password == password:
                request.session["studentID"] = student.studentID
                # authenticate the user and redirect to main menu
                # auth.login(request, student)
                return redirect("main_menu")

            else:
                dict = {
                    "message": "Invalid password. Please try again.",
                }
        else:
            dict = {
                "message": "You have not registered yet. Please register first.",
            }

    return render(request, "index.html", dict)


def forgot_password(request):
    dict = {"message": ""}
    s_id = request.POST.get("s_id")
    s_password = request.POST.get("s_password")
    s_password_again = request.POST.get("s_password_again")

    if request.method == "POST":
        student = Student.objects.filter(studentID=s_id)
        if student.exists() and s_password == s_password_again:
            Student.objects.filter(studentID=s_id).update(password="")
            Student.objects.filter(studentID=s_id).update(password=s_password_again)
            dict = {
                "message": "Your password has been reset.",
                "message_type": "success",
            }
        else:
            dict = {
                "message": "Error. Either you have not registered or both the entered password don't match.",
                "message_type": "error",
            }
    else:
        pass
    return render(request, "forgot_password.html", dict)


# register functionality, implemented in separate page.
def register(request):
    allCourse = Course.objects.all()
    allclass = Class.objects.all()
    dict = {
        "allclass": allclass,
        "allcourse": allCourse,
        "message": "",
    }
    if request.method == "POST":
        r_id = request.POST.get("r_id")
        r_password = request.POST.get("r_password")
        r_name = request.POST.get("r_name")
        r_course_id = request.POST.get("r_course")
        r_class = request.POST.get("r_class")

        try:
            course = Course.objects.get(courseID=r_course_id)
        except Course.DoesNotExist:
            dict = {
                "allclass": allclass,
                "allcourse": allCourse,
                "message": "Course does not exist.",
                "message_type": "error",
            }
            return render(request, "register.html", dict)

        try:
            student_class = Class.objects.get(classID=r_class)
        except Class.DoesNotExist:
            dict = {
                "allclass": allclass,
                "allcourse": allCourse,
                "message": "Class does not exist.",
                "message_type": "error",
            }
            return render(request, "register.html", dict)

        student = Student.objects.filter(studentID=r_id)
        if student.exists():
            dict = {
                "allclass": allclass,
                "allcourse": allCourse,
                "message": "You already have an account. No need to register anymore.",
                "message_type": "error",
            }

        else:
            data = Student(
                studentID=r_id,
                password=r_password,
                studentName=r_name,
                courseID=course,
                classID=student_class,
            )
            data.save()
            dict = {
                "allclass": allclass,
                "allcourse": allCourse,
                "message": "You are registered. You can proceed to sign-in.",
                "message_type": "success",
            }
    else:
        dict = {
            "allclass": allclass,
            "allcourse": allCourse,
            "message": "",
        }

    return render(request, "register.html", dict)


# for the page of register_vehicle
def register_vehicle(request):
    allstudent = Student.objects.all()
    dict = {
        "allstudent": allstudent,
        "message": "Your vehicle is successfully registered.",
    }

    if request.method == "POST":
        s_id = request.POST.get("s_id")
        plateNo = request.POST.get("plateNo")
        student = Student.objects.get(studentID=s_id)
        student.plateNo = plateNo
        student.save()
        dict = {
            "allstudent": allstudent,
            "message": "Your vehicle is successfully registered.",
            "message_type": "success",
        }

    else:
        dict = {"message": "", "allstudent": allstudent}
    return render(request, "register_vehicle.html", dict)


def book_parking(request):
    allparking = Parking.objects.filter(availability="Available")
    dict = {
        "message": "",
        "allparking": allparking,
        "message_type": "",
    }

    if request.method == "POST":
        # generate a random unique string for the bookingID
        booking_id = str(uuid.uuid4())[:4]
        # get the current student
        currentID = request.session.get("studentID")
        student = Student.objects.get(studentID=currentID)
        parking_slot_id = request.POST.get("parking_slot")
        parking = Parking.objects.get(parkingID=parking_slot_id)
        start_date_str = request.POST.get("startDate")
        end_date_str = request.POST.get("endDate")
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        remark = request.POST.get("remark")
        data = Booking.objects.filter(
            parkingID=parking_slot_id,
            startDate__lte=end_date,
            endDate__gte=start_date,
        )

        if data.exists():
            overlapping_dates = []
            for booking in data:
                overlap = (booking.startDate <= end_date) and (
                    booking.endDate >= start_date
                )
                if overlap:
                    overlapping_dates.append(f"{booking.startDate}- {booking.endDate}")
            dict = {
                "message": "Sorry. Your selected dates cannot be chosen.",
                "allparking": allparking,
                "message_type": "error",
                "overlapping_dates": overlapping_dates,
                "parkingID": parking_slot_id,
            }
        else:
            new_booking = Booking(
                bookingID=booking_id,
                studentID=student,
                startDate=start_date,
                endDate=end_date,
                parkingID=parking,
                remark=remark,
                bookingDate=date.today(),
                bookingTime=datetime.now().time(),
            )
            new_booking.save()
            dict = {
                "message": "You have successfully booked the parking.",
                "allparking": allparking,
                "message_type": "success",
            }

    return render(request, "book_parking.html", dict)


def check_booking(request):
    currentID = request.session.get("studentID")
    allbooking = Booking.objects.all()
    allreview = Review.objects.all()

    dict = {
        "message": "",
        "allbooking": allbooking,
        "studentID": currentID,
        "allreview": allreview,
    }

    if request.method == "GET":
        student_id = request.GET.get("student_id")
        if student_id:
            bookings = Booking.objects.filter(studentID=student_id)
            dict = {
                "message": "",
                "allbooking": bookings,
                "studentID": currentID,
                "allreview": allreview,
            }
        else:
            dict = {
                "message": "",
                "allbooking": allbooking,
                "studentID": currentID,
                "allreview": allreview,
            }

    booking_cancel = request.session.get("booking_cancel")
    if booking_cancel:
        del request.session["booking_cancel"]
        dict["booking_cancel"] = booking_cancel

    return render(request, "check_booking.html", dict)


def update_review(request, booking_id):
    currentID = request.session.get("studentID")
    s_id = Student.objects.get(studentID=currentID)
    try:
        booking = Booking.objects.get(bookingID=booking_id)
    except Booking.DoesNotExist:
        return render(request, "update_review.html")
    if request.method == "POST":
        # generate a random unique string for the bookingID
        review_id = str(uuid.uuid4())[:4]
        review_description = request.POST.get("review")
        try:
            review = Review.objects.get(bookingID=booking_id)
            review.delete()
        except Review.DoesNotExist:
            pass
        review = Review(
            reviewID=review_id,
            studentID=s_id,
            bookingID=booking,
            reviewDescription=review_description,
            reviewDate=date.today(),
            reviewTime=datetime.now().time(),
        )
        review.save()
        return redirect("check_booking")
    else:
        dict = {"message": ""}
    return render(request, "update_review.html", dict)


def personal_information(request):
    currentID = request.session.get("studentID")
    currentuser = Student.objects.get(studentID=currentID)
    message = request.session.get("message")
    if message:
        del request.session["message"]
    dict = {"currentuser": currentuser, "message": message, "message_type": "success"}
    return render(request, "personal_information.html", dict)


def update_personal_info(request):
    if request.method == "POST":
        currentID = request.session.get("studentID")
        currentuser = Student.objects.get(studentID=currentID)
        studentname = request.POST.get("studentName")
        plateno = request.POST.get("plateNo")
        courseid = request.POST.get("courseID")
        course = Course.objects.get(courseID=courseid)
        classid = request.POST.get("classID")
        class_id = Class.objects.get(classID=classid)
        currentuser.studentName = studentname
        currentuser.plateNo = plateno
        currentuser.courseID = course
        currentuser.classID = class_id
        currentuser.save()
        message = "Your personal information is updated."
        request.session["message"] = message
        return redirect("personal_information")
    else:
        pass


def delete_account(request):
    currentID = request.session.get("studentID")
    currentuser = Student.objects.get(studentID=currentID)
    currentuser.delete()
    return redirect(index)


def delete_review(request, booking_id):
    review = Review.objects.get(bookingID=booking_id)
    review.delete()
    return redirect("check_booking")


def cancel_booking(request, booking_id):
    booking = Booking.objects.get(bookingID=booking_id)
    booking.delete()
    request.session["booking_cancel"] = "Your parking booking is cancelled/deleted."
    return redirect("check_booking")
