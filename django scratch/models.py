from django.db import models

# Create your models here.

#Create Ticker Table

class Tickers(models.Model):
    symbol = models.CharField(max_length= 20)

    def __str__(self):
        return self.ticker_name

#Create NSE_Historic Data Table

class nse_historic(models.Model):
    date = models.DateField()
    symbol = models.CharField(max_length=20)
    series = models.CharField(max_length=9)
    pre_close = models.FloatField(max_length=15)
    open = models.FloatField(max_length=15)
    high = models.FloatField(max_length=15)
    low = models.FloatField(max_length=15)
    close = models.FloatField(max_length=15)
    vwap = models.FloatField(max_length=15)
    volume = models.FloatField(max_length=15)
    turnover = models.FloatField(max_length=20)
    trade = models.FloatField(max_length=15)
    deliverable_vol = models.FloatField(max_length=15)
    percent_deliverable = models.FloatField(max_length=15)
    fk_symbol = models.ForeignKey(Tickers, on_delete=models.CASCADE)

#Create NSE_future Data Table

class nse_future(models.Model):
    date = models.DateField()
    symbol = models.CharField(max_length=20)
    expiry = models.DateField()
    open = models.FloatField(max_length=15)
    high = models.FloatField(max_length=15)
    low = models.FloatField(max_length=15)
    close = models.FloatField(max_length=15)
    last = models.FloatField(max_length=15)
    settle_price = models.FloatField(max_length=10)
    no_of_contracts = models.FloatField(max_length=8)
    turnover = models.FloatField(max_length=20)
    open_interest = models.FloatField(max_length=20)
    change_in_oi = models.FloatField(max_length=20)
    underlying = models.FloatField(max_length=20)
    fk_symbol = models.ForeignKey(Tickers, on_delete=models.CASCADE)

