# Generated by Django 5.0.4 on 2024-04-23 09:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0007_customer_store_custo_last_na_e6a359_idx_and_more"),
    ]

    operations = [
        # the command below is to make custme sql commands and takes two args
        # first is to upgrade, second is to downgrade
        migrations.RunSQL("""
            INSERT INTO store_collection (title)
            VALUES ("collection1")
        """, """
            DELETE FROM store_collection
            WHERE title = "collection1"
        """)
    ]
