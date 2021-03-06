# Generated by Django 3.1.6 on 2021-02-09 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evenements',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PublicationSet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu_text', models.CharField(max_length=200)),
                ('media1', models.FileField(upload_to='')),
                ('media2', models.FileField(upload_to='')),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.utilisateurs')),
            ],
        ),
        migrations.CreateModel(
            name='Sets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('image_couverture', models.FileField(upload_to='')),
                ('type0', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('publication', models.ManyToManyField(related_name='publication_sets', through='sets.PublicationSet', to='user.Utilisateurs')),
            ],
        ),
        migrations.CreateModel(
            name='SetUtilisateurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statut', models.CharField(max_length=200)),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('set0', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sets.sets')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.utilisateurs')),
            ],
        ),
        migrations.AddField(
            model_name='sets',
            name='utilisateur',
            field=models.ManyToManyField(related_name='sets', through='sets.SetUtilisateurs', to='user.Utilisateurs'),
        ),
        migrations.AddField(
            model_name='publicationset',
            name='set0',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sets.sets'),
        ),
        migrations.CreateModel(
            name='PublicationEvenement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenu_text', models.CharField(max_length=200)),
                ('media1', models.FileField(upload_to='')),
                ('media2', models.FileField(upload_to='')),
                ('date', models.DateTimeField(auto_now=True, null=True)),
                ('auteur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.utilisateurs')),
                ('evenement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sets.evenements')),
            ],
        ),
        migrations.AddField(
            model_name='evenements',
            name='publication',
            field=models.ManyToManyField(through='sets.PublicationEvenement', to='user.Utilisateurs'),
        ),
        migrations.AddField(
            model_name='evenements',
            name='set0',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sets.sets'),
        ),
    ]
