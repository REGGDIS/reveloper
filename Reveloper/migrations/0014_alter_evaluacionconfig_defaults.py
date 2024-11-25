from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        # Asegúrate de que este sea el archivo de migración correcto.
        ('Reveloper', '0013_evaluacionconfig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluacionconfig',
            name='tiempo_entrega',
            field=models.DecimalField(
                decimal_places=1, default=25.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='evaluacionconfig',
            name='complejidad_tarea',
            field=models.DecimalField(
                decimal_places=1, default=25.0, max_digits=4),
        ),
    ]
