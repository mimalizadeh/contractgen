from django.db import models
from ckeditor.fields import RichTextField


class Clause(models.Model):

    title = models.CharField(max_length=255, verbose_name="عنوان ماده")
    content = RichTextField(verbose_name="متن مفاد")

    order = models.PositiveIntegerField(default=0, verbose_name="ترتیب نمایش")

    class Meta:
        ordering = ['order']
        verbose_name = "ماده قرارداد"
        verbose_name_plural = "مفاد قرارداد"

    def __str__(self):
        return self.title


class Presenter(models.Model):
    name = models.CharField(max_length=100, verbose_name='نام مجری')
    parent_name = models.CharField(max_length=100, verbose_name='نام پدر')
    national_code = models.CharField(max_length=13, verbose_name='کد ملی')
    phone_number = models.CharField(max_length=12, verbose_name='شماره همراه')
    address = models.TextField(max_length=1024, verbose_name='آدرس')

    class Meta:
        ordering = ['id']
        verbose_name = 'مجری'
        verbose_name_plural = 'مجری ها'

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class Employer(models.Model):
    name = models.CharField(
        max_length=100, verbose_name='نام کارفرما')
    parent_name = models.CharField(max_length=100, verbose_name='نام پدر' , blank=True)
    national_code = models.CharField(max_length=13, verbose_name='کد ملی')
    phone_number = models.CharField(max_length=12, verbose_name='شماره همراه')
    address = models.TextField(max_length=1024, verbose_name='آدرس')

    class Meta:
        ordering = ['id']
        verbose_name = 'کارفرما'
        verbose_name_plural = 'کارفرما ها'

    def __str__(self):
        return f"{self.name} - {self.phone_number}"

class Contract(models.Model):
    title = models.CharField(max_length=1024 , verbose_name='عنوان قرارداد' ,default='عنوان قرارداد')
    serial = models.CharField(max_length=20 , verbose_name='شماره قرارداد',default='123456')
    employer = models.ForeignKey(Employer, verbose_name='کارفرما', on_delete=models.PROTECT)
    presenter = models.ForeignKey(Presenter, verbose_name='مجری', on_delete=models.PROTECT)
    start_date = models.DateField(verbose_name='تاریخ شروع')
    total_amount = models.PositiveIntegerField(verbose_name='مبلغ کل')
    long_term = models.BooleanField(default=False, verbose_name='بلند مدت')
    monthly_salary = models.PositiveIntegerField(
        null=True, blank=True, verbose_name='حقوق ماهانه')
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='زمان ایجاد قرارداد')
    clauses = models.ManyToManyField(Clause, blank=True, verbose_name='مفاد')

    duration_days = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name='مدت زمان قرارداد',
        help_text="در صورت نیاز، مدت زمان انجام پروژه به روز کاری وارد شود"
    )


    class Meta:
        ordering = ['id']
        verbose_name = 'قرارداد'
        verbose_name_plural = 'قرارداد ها'

    def __str__(self):
        return f"Contract with {self.employer.name}-{self.presenter.name}"
