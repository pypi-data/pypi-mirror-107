# Generated by Django 3.2 on 2021-05-12 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djtezos', '0002_contract_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='account',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='Amount in xTZ'),
        ),
    ]
