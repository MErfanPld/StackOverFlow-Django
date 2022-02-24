from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    job_CHOICES = (
        ('A', 'برنامه نویس اندروید'),
        ('F', 'برنامه نویس فرانت اند'),
        ('B', 'برنامه نویس بک اند'),
        ('D', 'طراحی سایت'),
        ('S', 'توسعه دهنده سرور'),
        ('E', 'سایر'),
    )
    image = models.ImageField(default='1.jpg', verbose_name="تصویر پروفایل")
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name="شهر")
    label_job = models.CharField(max_length=2, choices=job_CHOICES, blank=True, null=True, verbose_name="برچسب کاری")
    bio = models.TextField(max_length=500, blank=True, default="Hello World", verbose_name="بیو")


class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "روابط"
        verbose_name_plural = "روابط ها"

    def __str__(self):
        return f'{self.from_user} following {self.to_user}'
