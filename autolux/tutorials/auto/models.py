from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date


class Engine(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    volume = models.CharField(max_length=20, verbose_name='Объем')
    power = models.CharField(max_length=20, verbose_name='Мощность')

    def __str__(self):
        return f"{self.name} ({self.volume}, {self.power} л.с)"

    class Meta:
        verbose_name_plural = 'Двигатель'
        ordering = ['name']


class Transmission(models.Model):
    type = models.CharField(max_length=40)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = 'Коробка передач'
        ordering = ['type']


class Rudder(models.Model):
    type = models.CharField(max_length=20)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = 'Руль'
        ordering = ['type']


class BodyType(models.Model):
    type = models.CharField(max_length=30)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name_plural = 'Тип Кузова'
        ordering = ['type']


class Car(models.Model):
    name = models.CharField(max_length=50, verbose_name='Модель')
    brand = models.CharField(max_length=40, verbose_name='Брэнд')
    engine = models.ForeignKey(Engine, on_delete=models.CASCADE, verbose_name='Двигатель')
    transmission = models.ForeignKey(Transmission, on_delete=models.CASCADE, verbose_name='Коробка передач')
    body_type = models.ForeignKey(BodyType, on_delete=models.CASCADE, verbose_name='Тип кузова')
    color = models.CharField(max_length=20, verbose_name='Цвет')
    mileage = models.CharField(max_length=40, verbose_name='Пробег')
    rudder = models.ForeignKey(Rudder, on_delete=models.CASCADE, verbose_name='Руль')
    price = models.DecimalField(max_digits=19, decimal_places=2, verbose_name='Цена')
    description = models.TextField(default='No description', verbose_name='Описание')
    photo = models.ImageField(upload_to='cars/', null=False, blank=False, verbose_name='Фото')

    def __str__(self):
        return f"{self.name} - {self.brand}"

    class Meta:
        verbose_name_plural = 'Автомобиль'
        ordering = ['name']


class TestDrive(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('approved', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    car = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name='Модель')
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    phone = models.CharField(max_length=20, verbose_name='Номер Телефона')
    preferred_date = models.DateField(verbose_name='Дата')
    comments = models.TextField(blank=True, null=True, verbose_name='Комментарии')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='Создано в:')

    def __str__(self):
        return f"Тест-драйв на машине {self.car.name} для {self.user} в {self.preferred_date}"

    class Meta:
        verbose_name_plural = 'Тест Драйвы'


class CarLoanApplication(models.Model):
    STATUS_CHOICES_LOAN = [
        ('pending', 'Ожидание'),
        ('approved', 'Принято'),
        ('rejected', 'Отклонено'),
    ]
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Пользователь')
    phone_number = models.CharField(max_length=20, verbose_name='Номер Телефона')
    car = models.ForeignKey('Car', on_delete=models.CASCADE, verbose_name='Модель')
    loan_term = models.IntegerField(verbose_name='Срок кредита в месяцах')
    annual_income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Годовой доход')
    approved = models.CharField(max_length=10, choices=STATUS_CHOICES_LOAN, default='pending',
                                verbose_name='Статус')

    def __str__(self):
        return f'{self.user} - {self.car.name}'

    class Meta:
        verbose_name_plural = 'Автокредит'


class CarLoanPayment(models.Model):
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Наличные'), ('bank', 'Банковский счет')],
                                      verbose_name='Тип оплаты')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    card_number = models.CharField(max_length=16, blank=True, null=True)  # Номер карты
    card_validity_period = models.CharField(max_length=5, blank=True, null=True)  # Срок действия карты
    card_code = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.payment_method}'

    class Meta:
        verbose_name_plural = 'Оплата автокредита'


class InsurancePolicy(models.Model):
    POLICY_TYPE_CHOICES = [
        ('full', 'Полное покрытие'),
        ('partial', 'Частичное покрытие'),
        ('liability', 'Ответственность перед третьими лицами'),
    ]

    STATUS_CHOICES_INSURANCE = [
        ('pending', 'Ожидание'),
        ('approved', 'Принято'),
        ('rejected', 'Отклонено'),
    ]

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Страховщик')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Модель')
    policy_type = models.CharField(max_length=10, choices=POLICY_TYPE_CHOICES, verbose_name='Тип полиса')
    start_date = models.DateField(verbose_name='Начало срока')
    end_date = models.DateField(verbose_name='Конец срока')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES_INSURANCE, default='pending', verbose_name='Статус')

    def __str__(self):
        return f"Полис: {self.policy_type} для {self.user} на {self.car}"

    class Meta:
        verbose_name_plural = 'Страховки'


class PaymentForm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Модель')
    passport = models.CharField(max_length=20, verbose_name='Паспорт')
    driving_license = models.CharField(max_length=20, verbose_name='Водительская права')
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Наличные'), ('bank', 'Банковский счет')],
                                      verbose_name='Тип оплаты')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    stripe_payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name='ID платежа Stripe')
    card_number = models.CharField(max_length=16, blank=True, null=True)  # Номер карты
    card_validity_period = models.CharField(max_length=5, blank=True, null=True)  # Срок действия карты
    card_code = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.payment_method}'

    class Meta:
        verbose_name_plural = 'Оплата'
