# Generated by Django 5.1.4 on 2025-01-15 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_cartitem_quanity_delete_orderitem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='quanity',
            new_name='quantity',
        ),
    ]
