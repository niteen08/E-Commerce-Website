# Generated by Django 5.0 on 2024-02-28 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderplaced',
            name='discounted_price',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='orderplaced',
            name='selling_price',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.CharField(max_length=500),
        ),
    ]