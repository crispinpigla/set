# Generated by Django 3.1.6 on 2021-02-10 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sets', '0003_auto_20210210_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sets',
            name='image_couverture',
            field=models.FileField(upload_to='media'),
        ),
    ]