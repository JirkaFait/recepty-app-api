# Generated by Django 3.1.3 on 2021-03-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20210324_1649'),
    ]

    operations = [
        migrations.AddField(
            model_name='units',
            name='title',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='units',
            name='name',
            field=models.CharField(max_length=15),
        ),
    ]
