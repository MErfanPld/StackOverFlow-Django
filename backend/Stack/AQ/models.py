from django.db import models
from account.models import User
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField


# Create your models here.

class Sliders(models.Model):
    image = models.ImageField(default='1.jpg', verbose_name="تصویر")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")

    class Meta:
        verbose_name = "اسلایدر"
        verbose_name_plural = "اسلایدرز"
        ordering = ['created']


class Category(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="ادرس")
    status = models.BooleanField(
        default=True, verbose_name="ایا نمایش داده شود؟")
    position = models.IntegerField(default=0, verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['position']

    def __str__(self):
        return self.title

    def get_absolute_url_cat(self):
        return reverse('home:category', args=(self.slug))


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', verbose_name="کاربر")
    title = models.CharField(max_length=200, verbose_name="عنوان سوال")
    slug = models.SlugField(max_length=200, verbose_name="ادرس")
    category = models.ManyToManyField(Category, related_name="questions", verbose_name="دسته بندی")
    body = RichTextField(blank=True, null=True, verbose_name="متن سوال")
    # body = models.TextField()
    image = models.ImageField(default='1.jpg', verbose_name="تصویر")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")

    class Meta:
        verbose_name = "سوال"
        verbose_name_plural = "سوال ها"
        ordering = ['created']

    def __str__(self):
        return f'{self.user} - {self.title[:20]}'

    def category_to_str(self):
        return "، ".join([category.title for category in self.category.all()])

    category_to_str.short_description = "دسته‌بندی"

    def get_absolute_url(self):
        return reverse('home:detail', args=(self.id, self.slug))
        return reverse('account:dashboard')

    def like_count(self):
        return self.Qvotes.count()

    def user_can_like(self, user):
        user_like = user.uvotes.filter(question=self)
        if user_like.exists():
            return True
        return False


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uanswer', verbose_name="کاربر")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='panswers',
                                 verbose_name="جواب به سوال")
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='ranswers', blank=True, null=True,
                              verbose_name="پاسخ")
    is_reply = models.BooleanField(default=False, verbose_name="پاسخ داده شده؟")
    body = RichTextField(blank=True, null=True, verbose_name="متن جواب")
    created = models.DateTimeField(auto_now_add=True, verbose_name="زمان ساخت")

    class Meta:
        verbose_name = "جواب"
        verbose_name_plural = "جواب ها"
        ordering = ['created']

    def __str__(self):
        return f'{self.user} - {self.body[:20]}'


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uvotes', verbose_name="کاربر")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='Qvotes', verbose_name="سوال")

    class Meta:
        verbose_name = "لایک"
        verbose_name_plural = "لایک ها"

    def __str__(self):
        return f'{self.user} liked {self.question.slug}'
