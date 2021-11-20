from django.db import models


class OrderModels(models.Model):
    first_name = models.CharField(max_length=24)
    company = models.CharField(max_length=24)
    phone = models.CharField(max_length=24)
    address = models.CharField(max_length=64)
    product = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.first_name}, {self.company}'

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class ClientModels(models.Model):
      phone_number = models.CharField(max_length=25)

      def __str__(self):
          return f'{self.phone_number}'


class NanoModels(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.name}, {self.email}'


class FeedBackModels(models.Model):
    feed_user = models.CharField(max_length=100)
    feed_mail = models.EmailField(unique=True)
    feed_text = models.CharField(max_length=300)

    def __str__(self):
        return self.feed_user
