# Generated by Django 3.0.7 on 2020-06-19 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id_role', models.AutoField(primary_key=True, serialize=False, verbose_name='idRole')),
                ('name_role', models.CharField(max_length=100, verbose_name='nameRole')),
            ],
        ),
    ]