from django.db import models
import datetime

# Create your models here.
class Course(models.Model):
    courseID = models.CharField(max_length=4, primary_key=True)
    courseName = models.TextField()
    courseDescription = models.TextField()


class Class(models.Model):
    classID = models.CharField(max_length=5, primary_key=True)


class Student(models.Model):
    studentID = models.CharField(max_length=11, primary_key=True)
    password = models.TextField(default=studentID)
    studentName = models.TextField()
    plateNo = models.CharField(max_length=7, default="Null")
    courseID = models.ForeignKey(Course, on_delete=models.CASCADE)
    classID = models.ForeignKey(Class, on_delete=models.CASCADE)


class Parking(models.Model):
    parkingID = models.CharField(max_length=4, primary_key=True)
    location = models.TextField()
    availability = models.CharField(max_length=len("Not available"))


class Booking(models.Model):
    bookingID = models.CharField(max_length=4, primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE, default="")
    parkingID = models.ForeignKey(Parking, on_delete=models.CASCADE, default="")
    bookingDate = models.DateField()
    bookingTime = models.TimeField()
    remark = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField()


class Review(models.Model):
    reviewID = models.CharField(max_length=4, primary_key=True)
    studentID = models.ForeignKey(Student, on_delete=models.CASCADE)
    bookingID = models.ForeignKey(Booking, on_delete=models.CASCADE)
    reviewDescription = models.TextField(null=True)
    reviewDate = models.DateField()
    reviewTime = models.TimeField()
