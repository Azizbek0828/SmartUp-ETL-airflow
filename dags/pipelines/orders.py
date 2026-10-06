from client import get_data
import pandas as pd
from load import loader
from config import ENDPOINTS

ORDER_COLUMNS = [
    'deal_id', 'filial_id', 'deal_time', 'delivery_date', 'booked_date', 'status',
    'total_amount', 'currency_code', 'person_id', 'sales_manager_id', 'sales_manager_name',
    'expeditor_id', 'expeditor_name', 'room_id', 'room_name', 'payment_type_code',
    'contract_code', 'total_weight_netto', 'self_shipment', 'return_reason_code',
]

NUMBER_WORDS = ('quant', 'price', 'amount', 'margin', 'weight', 'litre', 'volume')


def to_numbers(df):
    for col in df.columns:
        if any(w in col for w in NUMBER_WORDS):
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def to_dates(df):
    for col in df.columns:
        if col.endswith('_date') or col.endswith('_time'):
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
    return df


def extract_order_products(df):
    rows = []
    for _, row in df[['deal_id', 'order_products']].iterrows():
        products = row['order_products']
        if not isinstance(products, list):
            continue
        for p in products:
            if not isinstance(p, dict):
                continue
            flat = {k: v for k, v in p.items() if not isinstance(v, (list, dict))}
            rows.append({'deal_id': row['deal_id'], **flat})
    return pd.DataFrame(rows)


# ===== EXTRACT =====
order_df = get_data(ENDPOINTS['order'], 'order')
order_df = order_df.drop_duplicates(subset='deal_id')

# ===== TRANSFORM =====
# 1-jadval: orders
orders_df = order_df[ORDER_COLUMNS].copy()
orders_df = to_dates(to_numbers(orders_df))

# 2-jadval: order_products (ichma-ich ustundan)
order_products_df = extract_order_products(order_df)
order_products_df = to_dates(to_numbers(order_products_df)).drop_duplicates(ignore_index=True)

print(f"orders: {len(orders_df)} qator")
print(f"order_products: {len(order_products_df)} qator")
print("order_products ustunlari:", order_products_df.columns.tolist())

# ===== LOAD =====
loader(orders_df, 'orders')
if not order_products_df.empty:
    loader(order_products_df, 'order_products')