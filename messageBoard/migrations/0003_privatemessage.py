# Generated by Django 2.1.1 on 2019-02-22 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messageBoard', '0002_auto_20190221_1500'),
    ]

    operations = [
        migrations.CreateModel(
            name='privateMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='游客', max_length=20)),
                ('content', models.CharField(max_length=140)),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]