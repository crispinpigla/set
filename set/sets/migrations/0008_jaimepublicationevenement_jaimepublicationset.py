# Generated by Django 3.1.6 on 2021-02-12 01:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sets', '0007_auto_20210211_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='JaimePublicationSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('publication_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sets.publicationset')),
            ],
        ),
        migrations.CreateModel(
            name='JaimePublicationEvenement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('publication_evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sets.publicationevenement')),
            ],
        ),
    ]