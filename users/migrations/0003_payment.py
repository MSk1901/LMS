# Generated by Django 5.0.4 on 2024-04-11 15:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0002_lesson'),
        ('users', '0002_alter_user_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='дата оплаты')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19, verbose_name='сумма оплаты')),
                ('method', models.CharField(choices=[('cash', 'наличными'), ('transfer', 'переводом по номеру счета')], verbose_name='способ оплаты')),
                ('course_subject', models.ForeignKey(blank=True, null=True, on_delete=models.SET('Удаленный курс'), related_name='payments', to='lms.course')),
                ('lesson_subject', models.ForeignKey(blank=True, null=True, on_delete=models.SET('Удаленный урок'), related_name='payments', to='lms.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'оплата',
                'verbose_name_plural': 'оплаты',
            },
        ),
    ]
