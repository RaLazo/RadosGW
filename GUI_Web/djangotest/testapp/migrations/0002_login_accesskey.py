# Generated by Django 2.0.1 on 2018-03-22 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='accesskey',
            field=models.CharField(default='0000', max_length=100),
        ),
    ]