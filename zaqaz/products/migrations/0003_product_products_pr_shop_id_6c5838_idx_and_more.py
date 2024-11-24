# Generated by Django 5.1.2 on 2024-10-20 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_product_products_pr_shop_id_6c5838_idx_and_more'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['shop'], name='products_pr_shop_id_6c5838_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['category'], name='products_pr_categor_9edb3d_idx'),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['shop', 'category'], name='products_pr_shop_id_08d945_idx'),
        ),
    ]