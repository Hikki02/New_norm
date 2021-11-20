from django.db import models

from users.models import User


class ExcelFileTemplate(models.Model):
    excel_file = models.FileField(upload_to='excel_file_templates')
    file_name = models.CharField(max_length=64, default='')

    def __str__(self):
        return f'{self.excel_file}'


class ExcelFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    excel_file = models.FileField(
        upload_to='excel_files/',
        blank=True,
        null=True
    )
    file_name = models.CharField(max_length=64, default='')
    is_order = models.BooleanField(default=False)
    date_send = models.DateTimeField(auto_now=True)
    CATEGORY = (
        ('clothes', 'Одежда'),
        ('shoes', 'Обувь'),
        ('perfume', 'Парфюм')
    )
    category = models.CharField(max_length=64, choices=CATEGORY, null=True, blank=True,)

    def save(self, *args, **kwargs):
        self.file_name = self.excel_file.name
        super(ExcelFile, self).save(*args, **kwargs)


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    excel_file = models.ForeignKey(ExcelFile, on_delete=models.CASCADE)
    tnved = models.CharField(max_length=64, default='')
    full_product_name = models.CharField(max_length=128, default='')
    trademark = models.CharField(max_length=64, default='')
    article_type = models.CharField(max_length=64, default='')
    article_value = models.CharField(max_length=64, default='')
    product_type = models.CharField(max_length=64, default='')
    color = models.CharField(max_length=64, default='')
    target_gender = models.CharField(max_length=64, default='')
    clothing_type = models.CharField(max_length=64, default='')
    clothing_value = models.CharField(max_length=64, default='')
    composition = models.CharField(max_length=64, default='')
    standard_no = models.CharField(max_length=64, default='')
    status = models.CharField(max_length=64, default='')
    result_treatment_data = models.CharField(max_length=64, default='')

    def __str__(self):
        return f'{self.user}, {self.excel_file}'


class AddProductToExcelFile(models.Model):
    tnved = models.CharField(max_length=64, default='')
    full_product_name = models.CharField(max_length=128, default='')
    trademark = models.CharField(max_length=64, default='')
    article_type = models.CharField(max_length=64, default='')
    article_value = models.CharField(max_length=64, default='')
    product_type = models.CharField(max_length=64, default='')
    color = models.CharField(max_length=64, default='')
    target_gender = models.CharField(max_length=64, default='')
    clothing_type = models.CharField(max_length=64, default=0)
    clothing_value = models.CharField(max_length=64, default=0)
    composition = models.CharField(max_length=64, default='')
    standard_no = models.CharField(max_length=64, default='')
    status = models.CharField(max_length=64, default='')

    def __str__(self):
        return f"{self.full_product_name}"
