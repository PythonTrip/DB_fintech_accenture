# Generated by Django 3.2 on 2021-09-05 03:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deals', '0003_deal_ticker'),
    ]

    operations = [
        migrations.AddField(
            model_name='deal',
            name='type',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
    ]
