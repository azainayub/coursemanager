# Generated by Django 3.2.9 on 2022-03-02 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assistor', '0005_auto_20220301_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instructor',
            name='title',
            field=models.CharField(choices=[('DR', 'Dr.'), ('HO', 'Hon.'), ('JR', 'Jr.'), ('MR', 'Mr.'), ('MS', 'Mrs.'), ('MI', 'Ms.'), ('PR', 'Prof.'), ('SR', 'Sr.')], default='PR', max_length=2),
        ),
    ]
