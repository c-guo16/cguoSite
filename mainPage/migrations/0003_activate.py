# Generated by Django 2.1.1 on 2019-02-15 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainPage', '0002_user_isactive'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('random_id', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
            ],
        ),
    ]
