# Generated by Django 4.2 on 2023-05-03 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_productcategory_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
