import nsepy

from nsetools import Nse
nse = Nse()
print(nse)

all_stock_codes = nse.get_stock_codes(cached=True)
print(all_stock_codes)

index_codes = nse.get_index_list(cached=True)
top_gainers = nse.get_top_gainers()
nse.is_valid_code('infy')


print(index_codes)

