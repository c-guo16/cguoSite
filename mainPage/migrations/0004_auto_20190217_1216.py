# Generated by Django 2.1.1 on 2019-02-17 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainPage', '0003_activate'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Activate',
        ),
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
