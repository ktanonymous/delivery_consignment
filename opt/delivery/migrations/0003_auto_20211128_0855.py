# Generated by Django 3.2.9 on 2021-11-27 23:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_rename_reservation_baggage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carrybus',
            name='end_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='end_station', to='delivery.busstop'),
        ),
        migrations.AlterField(
            model_name='carrybus',
            name='start_station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='start_station', to='delivery.busstop'),
        ),
    ]
