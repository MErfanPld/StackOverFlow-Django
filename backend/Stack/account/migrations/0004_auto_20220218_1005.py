# Generated by Django 3.2.9 on 2022-02-18 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_relation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='relation',
            options={'verbose_name': 'روابط', 'verbose_name_plural': 'روابط ها'},
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, default='Hello World', max_length=500, verbose_name='بیو'),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='شهر'),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='1.jpg', upload_to='', verbose_name='تصویر پروفایل'),
        ),
        migrations.AlterField(
            model_name='user',
            name='label_job',
            field=models.CharField(blank=True, choices=[('A', 'برنامه نویس اندروید'), ('F', 'برنامه نویس فرانت اند'), ('B', 'برنامه نویس بک اند'), ('D', 'طراحی سایت'), ('S', 'توسعه دهنده سرور'), ('E', 'سایر')], max_length=2, null=True, verbose_name='برچسب کاری'),
        ),
    ]
