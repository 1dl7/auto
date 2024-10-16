from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from . import models


class CarsForm(forms.Form, forms.ModelForm):
    class Meta:
        model = models.Car
        fields = ['name', 'brand', 'engine', 'transmission', 'body_type', 'color', 'mileage',
                  'rudder', 'price', 'description', 'photo']

    bad_words = re.compile(r'(?iu)(?<![а-яё])(?:(?:(?:у|[нз]а|(?:хитро|не)?вз?[ыьъ]|с[ьъ]'
                           r'|(?:и|ра)[зс]ъ?|(?:о[тб]|п[оа]д)[ьъ]?|(?:\S(?=[а-яё]))+?[оаеи-])'
                           r'-?)?(?:[её](?:б(?!о[рй]|рач)|п[уа](?:ц|тс))|и[пб][ае][тцд][ьъ]).'
                           r'*?|(?:(?:н[иеа]|ра[зс]|[зд]?[ао](?:т|дн[оа])?|с(?:м[еи])?|а[пб]ч'
                           r')-?)?ху(?:[яйиеёю]|л+и(?!ган)).*?|бл(?:[эя]|еа?)(?:[дт][ьъ]?)?|'
                           r'\S*?(?:п(?:[иеё]зд|ид[аое]?р|ед(?:р(?!о)|[аое]р|ик)|охую)|бля(?:'
                           r'[дбц]|тс)|[ое]ху[яйиеё]|хуйн).*?|(?:о[тб]?|про|на|вы)?м(?:анд(?:'
                           r'[ауеыи](?:л(?:и[сзщ])?[ауеиы])?|ой|[ао]в.*?|юк(?:ов|[ауи])?|е[нт]'
                           r'ь|ища)|уд(?:[яаиое].+?|е?н(?:[ьюия]|ей))|[ао]л[ао]ф[ьъ](?:[яиюе]'
                           r'|[еёо]й))|елд[ауые].*?|ля[тд]ь|(?:[нз]а|по)х)(?![а-яё])')


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean_first_name(self):
        car = self.cleaned_data['first_name']
        mask = re.compile(r'^([А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23})$')
        if not mask.match(car):
            raise forms.ValidationError('Неверный формат имени')
        if CarsForm.bad_words.match(car):
            raise forms.ValidationError('Имя содержит недопустимые слова')
        return car

    def clean_last_name(self):
        car = self.cleaned_data['last_name']
        mask = re.compile(r'^([А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23})$')
        if not mask.match(car):
            raise forms.ValidationError('Неверный формат фамилии')
        if CarsForm.bad_words.match(car):
            raise forms.ValidationError('Фамилия содержит недопустимые слова')
        return car

    def clean_email(self):
        car = self.cleaned_data['email']
        if CarsForm.bad_words.match(car):
            raise forms.ValidationError('Почта содержит недопустимые слова')
        return car

    def clean_username(self):
        phone = self.cleaned_data['username']
        if CarsForm.bad_words.match(phone):
            raise forms.ValidationError('Никнейм содержит недопустимые слова')
        return phone


class TestDriveForm(forms.ModelForm):
    class Meta:
        model = models.TestDrive
        fields = ['phone', 'preferred_date', 'comments']

        widgets = {
            'preferred_date': forms.DateInput(attrs={'type': 'date'}),
        }


class CarLoanApplicationForm(forms.ModelForm):
    class Meta:
        model = models.CarLoanApplication
        fields = ['phone_number', 'loan_term', 'annual_income']


class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = models.InsurancePolicy
        fields = ['policy_type', 'start_date', 'end_date']


class PaymentFormForm(forms.ModelForm):
    class Meta:
        model = models.PaymentForm
        fields = ['passport', 'driving_license', 'payment_method', 'address', 'phone', 'card_code',
                  'card_validity_period', 'card_number']

    def clean(self):
        cleaned_data = super().clean()
        payment_method = cleaned_data.get('payment_method')
        address = cleaned_data.get('address')

        if payment_method == 'bank' and not address:
            raise forms.ValidationError('Пожалуйста, укажите адрес для банковского счета.')

        return cleaned_data


class CarLoanPayment(forms.ModelForm):
    class Meta:
        model = models.CarLoanPayment
        fields = ['address', 'card_code', 'card_validity_period', 'payment_method', 'card_number']

        def clean(self):
            cleaned_data = super().clean()
            payment_method = cleaned_data.get('payment_method')
            address = cleaned_data.get('address')

            if payment_method == 'bank' and not address:
                raise forms.ValidationError('Пожалуйста, укажите адрес для банковского счета.')

            return cleaned_data
