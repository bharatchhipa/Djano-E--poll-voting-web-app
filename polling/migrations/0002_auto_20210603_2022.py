# Generated by Django 3.2.3 on 2021-06-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='city',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AddField(
            model_name='candidate',
            name='ward',
            field=models.CharField(default='', max_length=15),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='name',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='party',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='candidate',
            name='sno',
            field=models.AutoField(default='', primary_key=True, serialize=False),
        ),
    ]
