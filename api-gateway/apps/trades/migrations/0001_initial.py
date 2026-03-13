from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symbol', models.CharField(max_length=20)),
                ('trade_type', models.CharField(choices=[('BUY', 'Buy'), ('SELL', 'Sell')], max_length=4)),
                ('quantity', models.DecimalField(decimal_places=4, max_digits=15)),
                ('price', models.DecimalField(decimal_places=4, max_digits=15)),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('EXECUTED', 'Executed'), ('CANCELLED', 'Cancelled'), ('FAILED', 'Failed')], default='PENDING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('executed_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True)),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
