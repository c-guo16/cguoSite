# Generated by Django 2.1.1 on 2019-03-02 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messageBoard', '0003_privatemessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='publicmessage',
            name='reply',
            field=models.IntegerField(default=-1),
        ),
    ]