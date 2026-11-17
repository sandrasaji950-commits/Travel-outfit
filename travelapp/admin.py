from django.contrib import admin
from .models import CustomUser, User, Supplier, Product, Booking, Feedback

admin.site.register(CustomUser)
admin.site.register(User)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Booking)
admin.site.register(Feedback)

# Register your models here.
