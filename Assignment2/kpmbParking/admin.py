from django.contrib import admin

# Register your models here.
from .models import Course, Student, Parking, Booking, Review, Class

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Parking)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(Class)
