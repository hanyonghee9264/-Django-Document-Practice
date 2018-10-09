# Generated by Django 2.1.2 on 2018-10-09 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fields', '0002_auto_20181009_1126'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='nickname',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='person',
            name='stars',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='person',
            name='shirt_size',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large')], help_text='S,M,L 중에 선택', max_length=1),
        ),
    ]
