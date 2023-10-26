import pandas as pd

def read_urls_from_excel(file_path, url_column_name, url_id_column_name):
    df = pd.read_excel(file_path)
    urls = df[url_column_name].tolist()
    url_ids = df[url_id_column_name].tolist()
    return urls, url_ids