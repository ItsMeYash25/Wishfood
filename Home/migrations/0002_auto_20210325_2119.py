# Generated by Django 3.1.7 on 2021-03-25 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tablereserve',
            name='username',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
