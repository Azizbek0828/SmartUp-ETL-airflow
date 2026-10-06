from config import ENDPOINTS
from client import get_data
import pandas as pd
from load import loader

# ETL

## EXTRACT
print('Productsni yuklash boshlandi...')
products_df = get_data(ENDPOINTS['inventory'], 'inventory')

## TRANSFORM
df = products_df[products_df['state'] == 'A'][[
    'product_id',
    'name',
    'box_type_code',
    'weight_netto',
    'weight_brutto',
    'litr',
    'box_quant',
    'order_no',
    'barcodes'
]]

int_columns = ['product_id', 'weight_netto', 'weight_brutto', 'litr', 'box_quant', 'order_no']

for col in int_columns:
    df[col] = pd.to_numeric(df[col])


# LOAD
loader(df, 'products')

