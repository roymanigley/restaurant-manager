# Generated by Django 5.1.2 on 2025-03-02 11:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='occupation',
            options={'ordering': ('-start',)},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-occupation__start',)},
        ),
        migrations.AlterModelOptions(
            name='restaurantuser',
            options={'ordering': ('first_name', 'last_name')},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'ordering': ('name',)},
        ),
    ]
