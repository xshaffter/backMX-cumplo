# Generated by Django 3.2.9 on 2021-11-25 03:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cat', '0004_auto_20211124_1939'),
    ]

    operations = [
        migrations.CreateModel(
            name='TIIESearch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('init_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.AlterField(
            model_name='exchangevalue',
            name='type',
            field=models.SmallIntegerField(choices=[(0, 'UDIS'), (1, 'USD'), (2, 'TIIE 4 semanas'), (3, 'TIIE 13 semanas'), (4, 'TIIE 26 semanas')], default=0),
        ),
        migrations.AddField(
            model_name='search',
            name='tiie_search',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='searches', to='cat.tiiesearch'),
        ),
    ]