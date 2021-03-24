# Generated by Django 3.1.3 on 2021-03-24 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210324_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipingredient',
            name='unit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.units'),
            preserve_default=False,
        ),
    ]