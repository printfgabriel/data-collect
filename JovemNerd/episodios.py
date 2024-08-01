# %%
import requests
import pandas as pd
import datetime
import json
import time

# %%
class Collector:
    def __init__(self, url, instance_name):
        self.url = url
        self.instance_name = instance_name

    def get_content(self, **kwargs):  # kwargs let u pass how many parameters u want
        resp = requests.get(self.url, params=kwargs) # using params instead of using premade urls
        return resp

    def save_parquet(self, data):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S.%f")
        df = pd.DataFrame(data)
        df.to_parquet(f"./data/{self.instance_name}/parquet/{now}.parquet", index=False)

    def save_json(self, data, option='json'):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S.%f")
        # with open(f".\\data\\{self.instance_name}\\json\\{now}.json", 'w+') as open_file:
        #     json.dump(data, open_file, indent=4)
        with open(f"./data/{self.instance_name}/json/{now}.json", "w") as open_file:
            json.dump(data, open_file, indent=4)
        
    def save_data(self, data, format='json'):
        if format == 'json':
            self.save_json(data)
        elif format == 'parquet':
            self.save_parquet(data)

    def get_and_save(self, save_format='json',**kwargs):
        resp = self.get_content(**kwargs)
        if resp.status_code == 200:
            data = resp.json()
            self.save_data(data, save_format)
        else:
            data = None
            print(f"Request sem sucesso: {resp.status_code}", resp.json())
        return data

    def auto_exec(self, date_stop='2000-01-01'):
        page = 1
        while True:
            data = self.get_and_save(save_format=save_format, page=page, per_page=10000 )
            if data == None:
                print("Erro ao coletar dados. Aguardando...")
                time.sleep()

            else:
                date_last = pd.to_datetime(data[-1]["published_at"]).date()
                if date_last < pd.to_datetime(date_stop).date():
                    break
                elif len(data)<1000:
                    break
                time.sleep(5)

# %%

url = "https://api.jovemnerd.com.br/wp-json/jovemnerd/v1/nerdcasts/"
collect = Collector(url, "episodios")

# %%
collect.get_and_save()

# %%
