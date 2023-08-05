# pybarry

Python3 library for [Barry](https://barry.energy/dk).

Get electricity consumption price.

## Install

```
pip3 install pybarry
```

## Example:

```python
from pybarry import Barry

access_token = '<your barry token>'
barry_connection = Barry(access_token=access_token)
# Get price_code from where your metering point is located
spot_price = barry_connection.update_spot_price(price_code=price_code)
print(spot_price)
# Get your mpid from selected metering point
total_price = barry_connection.update_total_price(mpid=mpid)
print(total_price)
```