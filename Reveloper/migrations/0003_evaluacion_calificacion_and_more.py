# Generated by Django 5.1.3 on 2024-11-13 13:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reveloper', '0002_remove_evaluacion_calificacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evaluacion',
            name='calificacion',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True),
        ),
        migrations.AlterField(
            model_name='evaluacion',
            name='fecha_vencimiento',
            field=models.DateTimeField(default=datetime.datetime(2024, 12, 13, 13, 16, 37, 249057, tzinfo=datetime.timezone.utc)),
        ),
    ]
