import pandas as pd
import pymysql
import config


def pd_read_sql(sql_query):
    conn = pymysql.connect(host=config.DB_HOST, user=config.DB_USERNAME, passwd=config.DB_PASSWORD, db=config.DB_NAME)
    # sql_query = "SELECT * FROM " + table_name
    df = pd.read_sql(sql_query, con=conn)

    return df
