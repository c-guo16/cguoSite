# Generated by Django 2.1.1 on 2019-02-21 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messageBoard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicmessage',
            name='username',
            field=models.CharField(default='游客', max_length=20),
        ),
    ]
