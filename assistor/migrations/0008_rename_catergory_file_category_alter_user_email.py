# Generated by Django 4.0.2 on 2022-03-04 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistor', '0007_auto_20220303_2149'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='catergory',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]