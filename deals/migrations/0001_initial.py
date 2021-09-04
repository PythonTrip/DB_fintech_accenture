# Generated by Django 3.2 on 2021-09-04 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_id', models.IntegerField()),
                ('adj', models.FloatField()),
                ('volume', models.IntegerField()),
                ('deal_date', models.DateField()),
            ],
        ),
    ]