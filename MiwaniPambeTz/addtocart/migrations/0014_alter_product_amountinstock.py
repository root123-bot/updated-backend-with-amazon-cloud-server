# Generated by Django 3.2 on 2022-09-16 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addtocart', '0013_auto_20220916_0927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='amountInStock',
            field=models.PositiveIntegerField(default=100),
        ),
    ]
