# Generated by Django 3.2.9 on 2022-01-30 07:46

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AQ', '0004_question_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='body',
            field=ckeditor.fields.RichTextField(blank=True, null=True),
        ),
    ]