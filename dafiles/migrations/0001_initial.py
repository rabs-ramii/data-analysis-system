# Generated by Django 4.1.7 on 2024-08-02 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('file', models.FileField(max_length=250, upload_to='csvfiles')),
            ],
        ),
    ]
