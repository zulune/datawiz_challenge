import json
import pandas as pd
import datetime
from dwapi import datawiz



class DatawizInfo:

    dw = None
    client_id = ""
    client_secret = ""
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.dw = datawiz.DW(client_id, client_secret)

    def get_client_info(self):
        client_info = self.dw.get_client_info()
        return client_info

    def get_shops(self):
        shops = self.dw.get_shops()
        return shops

    def get_products_sale(self, **kwargs):
        print(kwargs)
        products = kwargs['products']
        products.append('sum')
        products_sale = self.dw.get_products_sale(
            products=products,
            shops=shops,
            date_from=date_from,
            date_to=date_to,
            interval=datawiz.WEEKS
        )
        return products_sale
    