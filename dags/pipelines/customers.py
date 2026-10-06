# from client import get_data
# import pandas as pd
# from load import loader
# from config import ENDPOINTS

# ## legal_person
# # EXTRACT
# legal_entity_df = get_data(ENDPOINTS['legal_person'], 'legal_person')

# # TRANSFORM
# # customers
# legal_df = legal_entity_df.loc[
#     legal_entity_df['state'] == 'A',
#     ['person_id', 'name', 'main_phone', 'telegram', 'address']
# ]

# legal_df = legal_entity_df.rename(columns={'name': 'full_name'})

# legal_df.drop_duplicates(inplace=True)

# legal_df['type'] = 'legal_entity'

# # customer_groups
# rows = []
# for _, row in legal_entity_df[['person_id', 'groups']].iterrows():
#     # print(row)
#     for group in row['groups']:
#         rows.append({
#             'person_id': row['person_id'],
#             'group_id': group.get('group_id'),
#             'group_code': group.get('group_code'),
#             'type_id': group.get('type_id'),
#             'type_code': group.get('type_code')
#         })

# legal_entity_groups_df = pd.json_normalize(rows)

# ## natural_person
# # EXTRACT
# natular_person_df = get_data(ENDPOINTS['natural_person'], 'natural_person')

# # TRANSFORM
# rows = []
# for _, row in natular_person_df[['person_id', 'groups']].iterrows():
#     # print(row)
#     for group in row['groups']:
#         rows.append({
#             'person_id': row['person_id'],
#             'group_id': group.get('group_id'),
#             'group_code': group.get('group_code'),
#             'type_id': group.get('type_id'),
#             'type_code': group.get('type_code')
#         })

# natular_person_groups_df = pd.json_normalize(rows)

# natular_person_df['full_name'] = natular_person_df['first_name'] + ' ' + natular_person_df['last_name']

# natular_person_df = natular_person_df.loc[
#     natular_person_df['state'] == 'A',
#     ['person_id', 'full_name', 'main_phone', 'telegram', 'address']
# ]

# natular_person_df.drop_duplicates(inplace=True)

# natular_person_df['type'] = 'natural_person'

# customers_df = pd.concat([legal_df, natular_person_df])
# customer_groups_df = pd.concat([legal_entity_groups_df, natular_person_groups_df])
# # LOAD
# loader(customers_df, 'customers')
# loader(customer_groups_df, 'customer_groups')








from client import get_data
import pandas as pd
from load import loader
from config import ENDPOINTS

CUSTOMER_COLUMNS = ['person_id', 'full_name', 'main_phone', 'telegram', 'address']
GROUP_COLUMNS = ['person_id', 'group_id', 'group_code', 'type_id', 'type_code']


def extract_groups(df):
    """Har bir mijozning 'groups' ro'yxatini alohida jadvalga ajratadi:
    1 qator = 1 mijoz + 1 guruh."""
    rows = []
    for _, row in df[['person_id', 'groups']].iterrows():
        groups = row['groups']
        if not isinstance(groups, list):      # None yoki NaN bo'lsa - o'tkazib yuboramiz
            continue
        for group in groups:
            rows.append({
                'person_id': row['person_id'],
                'group_id': group.get('group_id'),
                'group_code': group.get('group_code'),
                'type_id': group.get('type_id'),
                'type_code': group.get('type_code'),
            })
    return pd.DataFrame(rows, columns=GROUP_COLUMNS)


## ================= legal_person =================
# EXTRACT
legal_entity_df = get_data(ENDPOINTS['legal_person'], 'legal_person')

# TRANSFORM
legal_active = legal_entity_df[legal_entity_df['state'] == 'A']     # faqat faol mijozlar

# customers
legal_df = legal_active.rename(columns={'name': 'full_name'})[CUSTOMER_COLUMNS].copy()
legal_df['full_name'] = legal_df['full_name'].str.strip()
legal_df = legal_df.drop_duplicates(subset='person_id')
legal_df['type'] = 'legal_entity'

# customer_groups
legal_groups_df = extract_groups(legal_active)


## ================= natural_person =================
# EXTRACT
natural_person_df = get_data(ENDPOINTS['natural_person'], 'natural_person')

# TRANSFORM
natural_active = natural_person_df[natural_person_df['state'] == 'A'].copy()

# customers
natural_active['full_name'] = (
    natural_active['first_name'].fillna('').str.strip() + ' ' +
    natural_active['last_name'].fillna('').str.strip()
).str.strip()

natural_df = natural_active[CUSTOMER_COLUMNS].copy()
natural_df = natural_df.drop_duplicates(subset='person_id')
natural_df['type'] = 'natural_person'

# customer_groups
natural_groups_df = extract_groups(natural_active)


## ================= BIRLASHTIRISH =================
customers_df = pd.concat([legal_df, natural_df], ignore_index=True)
customer_groups_df = pd.concat(
    [legal_groups_df, natural_groups_df], ignore_index=True
).drop_duplicates(ignore_index=True)

print(f"customers: {len(customers_df)} qator | customer_groups: {len(customer_groups_df)} qator")

# LOAD
loader(customers_df, 'customers')
loader(customer_groups_df, 'customer_groups')
