from django.contrib import admin
from . import models

admin.site.register(models.Car)
admin.site.register(models.Engine)
admin.site.register(models.BodyType)
admin.site.register(models.Rudder)
admin.site.register(models.Transmission)
admin.site.register(models.TestDrive)
admin.site.register(models.CarLoanApplication)
admin.site.register(models.InsurancePolicy)
admin.site.register(models.PaymentForm)
admin.site.register(models.CarLoanPayment)
