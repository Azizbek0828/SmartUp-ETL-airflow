import pandas as pd
from sqlalchemy import create_engine
from config import db_url

engine = create_engine(db_url)  
def loader(df: pd.DataFrame, table_name, conn=engine):
    if df.empty:
        print('Bu jadval bosh')
        return

    df.to_sql(table_name, conn, if_exists='replace', index=False)

