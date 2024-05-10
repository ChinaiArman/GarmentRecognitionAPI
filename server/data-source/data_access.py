import pandas as pd
import os

class Database:
    def get_data_frame():
        df = pd.read_csv("server/data-source/data.csv")
        return df

    def get_item_by_id(id):
        df = get_data_frame()
        item = df.loc[df['id'] == id]
        return item
    

