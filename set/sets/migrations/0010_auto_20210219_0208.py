# Generated by Django 3.1.6 on 2021-02-19 02:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20210219_0208'),
        ('sets', '0009_auto_20210212_0151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evenements',
            name='publication',
        ),
        migrations.AddField(
            model_name='evenements',
            name='administrateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user.utilisateurs'),
        ),
    ]
