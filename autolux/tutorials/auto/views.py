from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from . import models
from . import forms
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy


class CarLoanPaymentView(LoginRequiredMixin, View):
    template_name = 'payment_car_loan.html'

    def get(self, request):
        form = forms.CarLoanPayment()
        user = request.user

        return render(request, self.template_name, {'form': form, 'user': user})

    def post(self, request):
        form = forms.CarLoanPayment(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.save()

            payment_method = form.cleaned_data.get('payment_method')

            if payment_method == 'cash':
                messages.success(request, 'Оплата наличными успешно оформлена.')
            else:
                messages.success(request, 'Оплата банковским счетом успешно выполнена.')
                return redirect('success_payment')

        return render(request, self.template_name, {'form': form})


class PaymentView(LoginRequiredMixin, View):
    template_name = 'payment_form.html'

    def get(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.PaymentFormForm()
        user = request.user

        return render(request, self.template_name, {'car': car, 'form': form, 'user': user})

    def post(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.PaymentFormForm(request.POST)

        if form.is_valid():
            payment = form.save(commit=False)
            payment.car = car
            payment.user = request.user
            payment.save()

            payment_method = form.cleaned_data.get('payment_method')

            if payment_method == 'cash':
                messages.success(request, 'Оплата наличными успешно оформлена.')
            else:
                messages.success(request, 'Оплата банковским счетом успешно выполнена.')
                return redirect('success_payment')

        return render(request, self.template_name, {'car': car, 'form': form})

    @staticmethod
    def success_payment(request):
        return render(request, 'success_message_payment.html')


class InsurancePolicyStatus(LoginRequiredMixin, View):
    template_name = 'policy_status.html'

    def get(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        user = request.user
        insurance = models.InsurancePolicy.objects.filter(car=car, user=user).first()
        if not insurance:
            messages.error(request, "У вас нет соглашение на страхование.")
            return redirect('car_detail', pk=pk)
        return render(request, self.template_name, {'car': car, 'insurance': insurance, 'user': user})

    @staticmethod
    def post(request, pk):
        insurance = get_object_or_404(models.InsurancePolicy, id=pk)
        if 'approve' in request.POST:
            insurance.status = 'approved'
        elif 'reject' in request.POST:
            insurance.status = 'rejected'

        insurance.save()
        return redirect('policy_status', pk=pk)


class InsurancePolicy(LoginRequiredMixin, View):
    template_name = 'policy.html'

    def get(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.InsurancePolicyForm()
        user = request.user
        return render(request, self.template_name, {'car': car, 'form': form, 'user': user})

    def post(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.InsurancePolicyForm(request.POST)

        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.car = car
            insurance.user = request.user
            insurance.save()
            return redirect('success')
        return render(request, self.template_name, {'car': car, 'form': form})


class ApplicationLoanStatus(LoginRequiredMixin, View):
    template_name = 'loan_status.html'

    def get(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        user = request.user
        loan = models.CarLoanApplication.objects.filter(car=car, user=user).first()
        if not loan:
            messages.error(request, "У вас нет заявки на автокредит.")
            return redirect('car_detail', pk=pk)
        return render(request, self.template_name, {'car': car, 'loan': loan, 'user': user})

    @staticmethod
    def post(request, pk):
        loan = get_object_or_404(models.CarLoanApplication, id=pk)
        if 'approve' in request.POST:
            loan.approved = 'approved'
        elif 'reject' in request.POST:
            loan.approved = 'rejected'

        loan.save()
        return redirect('loan_status', pk=pk)


class ApplyForLoan(LoginRequiredMixin, View):
    template_name = 'apply.html'

    def get(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.CarLoanApplicationForm()
        user = request.user
        return render(request, self.template_name, {'car': car, 'form': form, 'user': user})

    def post(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.CarLoanApplicationForm(request.POST)

        if form.is_valid():
            loan = form.save(commit=False)
            loan.car = car
            loan.user = request.user
            loan.save()
            return redirect('success')
        return render(request, self.template_name, {'car': car, 'form': form})


class CarsTestDriveStatus(LoginRequiredMixin, View):
    template_name = 'test_status.html'

    def get(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        user = request.user
        test_drive = models.TestDrive.objects.filter(car=car, user=user).first()
        if not test_drive:
            messages.error(request, "У вас нет заявки на тест-драйв.")
            return redirect('car_detail', pk=pk)
        return render(request, self.template_name, {'car': car, 'test_drive': test_drive, 'user': user})

    @staticmethod
    def post(request, pk):
        test_drive = get_object_or_404(models.TestDrive, id=pk)
        if 'approve' in request.POST:
            test_drive.status = 'approved'
        elif 'reject' in request.POST:
            test_drive.status = 'rejected'

        test_drive.save()
        return redirect('test_status', pk=pk)


class CarsTestDrive(LoginRequiredMixin, View):
    template_name = 'test_drive.html'

    def get(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.TestDriveForm()
        user = request.user
        return render(request, self.template_name, {'car': car, 'form': form, 'user': user})

    def post(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.TestDriveForm(request.POST)

        if form.is_valid():
            test_drive = form.save(commit=False)
            test_drive.car = car
            test_drive.user = request.user
            test_drive.save()
            return redirect('success')
        return render(request, self.template_name, {'car': car, 'form': form})

    @staticmethod
    def success(request):
        return render(request, 'success_message_test_drive.html')


class CarsListView(View):
    template_name = 'cars.html'

    def get(self, request):
        form = models.Car.objects.all()
        return render(request, self.template_name, {'cars': form})


class CarDetailView(View):
    template_name = 'cars.detail.html'

    def get(self, request, pk):
        form = get_object_or_404(models.Car, id=pk)
        return render(request, self.template_name, {'car': form})


class CarCreateView(LoginRequiredMixin, View, PermissionRequiredMixin):
    template_name = 'cars_create.html'
    permission_required = 'auto.add_car'

    def get(self, request):
        form = forms.CarsForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = forms.CarsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cars')
        return render(request, self.template_name, {'form': form})

    def handle_no_permission(self):
        return redirect(reverse_lazy('cars'))


class CarUpdateView(LoginRequiredMixin, View, PermissionRequiredMixin):
    template_name = 'cars_update.html'
    permission_required = 'auto.change_car'

    def get(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.CarsForm(instance=car)
        return render(request, self.template_name, {'form': form, 'car': car})

    def post(self, request, pk):
        car = get_object_or_404(models.Car, id=pk)
        form = forms.CarsForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('cars')
        return render(request, self.template_name, {'form': form})

    def handle_no_permission(self):
        return redirect(reverse_lazy('cars'))


class CarDeleteView(LoginRequiredMixin, View, PermissionRequiredMixin):
    car: models.Car
    permission_required = 'auto.delete_car'

    def get(self, request, pk):
        self.car = get_object_or_404(models.Car, id=pk)
        return render(request, {'car': self.car})

    def post(self, _, pk):
        self.car = get_object_or_404(models.Car, id=pk)
        self.car.delete()
        return redirect('cars')

    def handle_no_permission(self):
        return redirect(reverse_lazy('cars'))


class SignUp(View):
    template_name = 'sign_up.html'

    def get(self, request):
        form = forms.UserForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = forms.UserForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                login(request, new_user)
                return redirect('cars')
            else:
                return render(request, self.template_name, {'form': form})


class SignIn(View):
    template_name = 'sign_in.html'

    def get(self, request):
        form = AuthenticationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('cars')
        return render(request, self.template_name, {'form': form})


class SignOut(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('cars')
