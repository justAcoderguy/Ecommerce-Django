# Generated by Django 4.0.5 on 2022-06-30 14:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_productattributevalue'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductAttributeValues',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attributevalues', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attributevaluess', to='inventory.productattributevalue')),
            ],
        ),
        migrations.AddField(
            model_name='productinventory',
            name='attribute_values',
            field=models.ManyToManyField(related_name='product_attribute_values', through='inventory.ProductAttributeValues', to='inventory.productattributevalue'),
        ),
        migrations.AddField(
            model_name='productattributevalues',
            name='productinventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='productattributevaluess', to='inventory.productinventory'),
        ),
        migrations.AlterUniqueTogether(
            name='productattributevalues',
            unique_together={('attributevalues', 'productinventory')},
        ),
    ]
