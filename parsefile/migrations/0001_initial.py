# Generated by Django 4.1.5 on 2023-01-29 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('owner', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(max_length=25)),
                ('data', models.DateTimeField()),
                ('valor', models.CharField(max_length=10)),
                ('cpf', models.CharField(max_length=11)),
                ('cartao', models.CharField(max_length=12)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='parsefile.store')),
            ],
        ),
    ]
