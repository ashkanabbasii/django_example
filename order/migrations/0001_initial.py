from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Cryptocurrency',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField(unique=True)),
                ('balance', models.DecimalField(max_digits=10, decimal_places=2, default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('cryptocurrency', models.ForeignKey(to='orders.Cryptocurrency', on_delete=models.CASCADE)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('total_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('combined', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.IntegerField()),
                ('order', models.ForeignKey(to='orders.Order', on_delete=models.CASCADE)),
                ('action', models.CharField(max_length=50)),
                ('amount', models.DecimalField(max_digits=10, decimal_places=2)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]