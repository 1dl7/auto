from django.urls import path
from . import views

urlpatterns = [
    path('test/drive/<int:pk>', views.CarsTestDrive.as_view(), name='test_drive'),
    path('', views.CarsListView.as_view(), name='cars'),
    path('car/detail/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('car/create/', views.CarCreateView.as_view(), name='car_create'),
    path('car/update/<int:pk>/', views.CarUpdateView.as_view(), name='car_update'),
    path('car/delete/<int:pk>/', views.CarDeleteView.as_view(), name='car_delete'),
    path('sign_up/', views.SignUp.as_view(), name='sign_up'),
    path('sign_in/', views.SignIn.as_view(), name='sign_in'),
    path('sign_out/', views.SignOut.as_view(), name='sign_out'),
    path('test_status/<int:pk>/', views.CarsTestDriveStatus.as_view(), name='test_status'),
    path('success/drive', views.CarsTestDrive.success, name='success'),
    path('loan/<int:pk>/', views.ApplyForLoan.as_view(), name='loan'),
    path('loan/status/<int:pk>/', views.ApplicationLoanStatus.as_view(), name='loan_status'),
    path('policy/<int:pk>/', views.InsurancePolicy.as_view(), name='policy'),
    path('policy/status/<int:pk>/', views.InsurancePolicyStatus.as_view(), name='policy_status'),
    path('payment/<int:pk>/', views.PaymentView.as_view(), name='payment'),
    path('success/payment/', views.PaymentView.success_payment, name='success_payment'),
    path('payment/loan/', views.CarLoanPaymentView.as_view(), name='loan_payment')
]
