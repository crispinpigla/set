# Generated by Django 5.0.3 on 2024-03-30 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_alter_utilisateurs_statut_activation_compte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateurs',
            name='statut_activation_compte',
            field=models.BooleanField(default=False),
        ),
    ]
