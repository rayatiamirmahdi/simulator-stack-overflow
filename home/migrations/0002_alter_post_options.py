# Generated by Django 4.0.6 on 2022-07-15 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-create']},
        ),
    ]
