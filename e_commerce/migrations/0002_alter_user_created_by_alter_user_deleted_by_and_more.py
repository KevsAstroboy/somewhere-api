# Generated by Django 4.1.2 on 2023-11-26 02:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='deleted_by',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_by',
            field=models.IntegerField(null=True),
        ),
    ]
