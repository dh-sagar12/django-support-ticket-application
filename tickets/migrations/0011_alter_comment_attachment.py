# Generated by Django 4.0.4 on 2022-06-01 18:20

from django.db import migrations, models
import tickets.models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_comment_attachment_alter_ticket_issued_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='attachment',
            field=models.ImageField(blank=True, null=True, upload_to=tickets.models.Comment.avatar_directory_path),
        ),
    ]
