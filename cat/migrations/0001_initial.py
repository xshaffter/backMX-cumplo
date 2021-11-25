# Generated by Django 3.2.9 on 2021-11-24 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.SmallIntegerField(choices=[(0, 'UDIS'), (1, 'USD')], default=0)),
                ('value', models.DecimalField(decimal_places=10, max_digits=15)),
                ('date', models.DateField()),
            ],
            options={
                'unique_together': {('type', 'date')},
            },
        ),
    ]