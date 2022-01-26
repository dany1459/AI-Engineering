from sqlalchemy import create_engine
import pandas as pd


def create_db():

    try:
        engine = create_engine("sqlite:///music.db")
        connection = engine.connect()

        df = pd.read_csv("music.csv")

        df.to_sql("music", connection, if_exists='replace')
        connection.close()
        return 0

    except:
        return 1

def get_music():

    try:
        engine = create_engine("sqlite:///music.db")
        connection = engine.connect()

        df = pd.read_sql_query("SELECT * FROM music", connection)
        connection.close()
        return df.to_dict()

    except:
        return {"ERROR": "No table was found."}

def get_genre(genre):

    try:
        engine = create_engine("sqlite:///music.db")
        connection = engine.connect()

        df = pd.read_sql_query("SELECT name FROM music WHERE genre = '{}'".format(genre), connection)
        connection.close()
        return df.to_dict()
        
    except:
        return {"ERROR": "No genre was found."}

create_db()