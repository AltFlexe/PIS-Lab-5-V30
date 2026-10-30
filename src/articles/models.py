from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal


class Article(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    text = models.TextField('Текст')
    created_date = models.DateField('Дата создания', auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}: {self.title}'

    def get_excerpt(self):
        return self.text[:140] + '...' if len(self.text) > 140 else self.text

    get_excerpt.short_description = 'Краткий текст'

    class Meta:
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'


class Space(models.Model):
    number = models.CharField('Номер помещения', max_length=30, unique=True)
    floor = models.IntegerField('Этаж')
    area = models.DecimalField('Площадь, м²', max_digits=8, decimal_places=2,
                               validators=[MinValueValidator(Decimal('0.01'))])
    air_conditioner = models.BooleanField('Кондиционер', default=False)
    daily_price = models.DecimalField('Цена за день', max_digits=10, decimal_places=2,
                                      validators=[MinValueValidator(Decimal('0.01'))])

    @classmethod
    def available(cls, start, end):
        if not start or not end or start > end:
            raise ValidationError('Укажите корректный период аренды.')
        occupied = ContractSpace.objects.filter(
            start_date__lte=end, end_date__gte=start
        ).values('space_id')
        return cls.objects.exclude(pk__in=occupied)

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'помещение'
        verbose_name_plural = 'помещения'


class Tenant(models.Model):
    name = models.CharField('Название', max_length=200)
    address = models.CharField('Адрес', max_length=250)
    phone = models.CharField('Телефон', max_length=50)
    details = models.TextField('Реквизиты')
    contact = models.CharField('Контактное лицо', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'арендатор'
        verbose_name_plural = 'арендаторы'


class Contract(models.Model):
    number = models.CharField('Номер договора', max_length=30, unique=True)
    tenant = models.ForeignKey(Tenant, on_delete=models.PROTECT, verbose_name='Арендатор')
    signed_date = models.DateField('Дата заключения')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'договор'
        verbose_name_plural = 'договоры'


class ContractSpace(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE,
                                 related_name='periods', verbose_name='Договор')
    space = models.ForeignKey(Space, on_delete=models.PROTECT,
                              related_name='periods', verbose_name='Помещение')
    start_date = models.DateField('Начало аренды')
    end_date = models.DateField('Окончание аренды')

    def clean(self):
        super().clean()
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError('Дата окончания должна быть не раньше даты начала.')
        if self.space_id and self.start_date and self.end_date:
            conflicts = ContractSpace.objects.filter(
                space_id=self.space_id, start_date__lte=self.end_date,
                end_date__gte=self.start_date,
            ).exclude(pk=self.pk)
            if conflicts.exists():
                raise ValidationError('Помещение уже занято в этом периоде.')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.contract}: {self.space}'

    class Meta:
        verbose_name = 'период аренды помещения'
        verbose_name_plural = 'периоды аренды помещений'
        constraints = [models.CheckConstraint(condition=models.Q(start_date__lte=models.F('end_date')),
                                              name='valid_rental_dates')]


class Payment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.PROTECT, related_name='payments', verbose_name='Договор')
    month = models.DateField('Месяц платежа')
    paid_date = models.DateField('Дата платежа')
    amount = models.DecimalField('Сумма', max_digits=12, decimal_places=2,
                                 validators=[MinValueValidator(Decimal('0.01'))])

    def __str__(self):
        return f'{self.contract}: {self.month}'

    class Meta:
        verbose_name = 'платёж'
        verbose_name_plural = 'платежи'
