# Generated by Django 3.0.4 on 2020-03-16 04:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subtype',
            options={'verbose_name': '题目类型表', 'verbose_name_plural': '题目类型表'},
        ),
        migrations.AlterModelTable(
            name='subtype',
            table='sub_type',
        ),
    ]