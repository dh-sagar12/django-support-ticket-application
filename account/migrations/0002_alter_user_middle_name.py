# Generated by Django 4.0.4 on 2022-05-24 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='middle_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
