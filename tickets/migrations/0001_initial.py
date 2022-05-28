# Generated by Django 4.0.4 on 2022-05-21 17:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketPriority',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
                'db_table': 'ticket_priority',
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('is_opened', models.BooleanField()),
                ('is_closed', models.BooleanField()),
                ('opened_at', models.DateTimeField()),
                ('closed_at', models.DateTimeField()),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='assigned_to', to=settings.AUTH_USER_MODEL)),
                ('issued_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='issued_by', to=settings.AUTH_USER_MODEL)),
                ('opened_by', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='opened_by', to=settings.AUTH_USER_MODEL)),
                ('priority_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tickets.ticketpriority')),
            ],
            options={
                'db_table': 'ticket',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('comment', models.TextField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('ticket_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tickets.ticket')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'comments',
            },
        ),
    ]
