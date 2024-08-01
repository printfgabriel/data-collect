# %%
import requests
import pandas as pd
import datetime
import json
import time

# %%

def get_response(**kwargs):  # kwargs let u pass how many parameters u want
    url = "https://www.tabnews.com.br/api/v1/contents/"
    resp = requests.get(url, params=kwargs) # using params instead of using premade urls
    return resp

def save_data(data, option='json'):

    # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%F")
    now = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S.%f")

    if option == 'json':
        # with open(".\\data\\{now}.json", 'w') as open_file:
        with open(f"./data/contents/json/{now}.json", 'w') as open_file:
            json.dump(data, open_file, indent=4)

    elif option == 'dataframe':
        df = pd.DataFrame(data)
        df.to_parquet(f"data/contents/parquet/{now}.parquet", index=False)

# %%
page = 1
while True:
    print(page)
    resp = get_response(page=page, per_page=100, strategy="new")
    print(resp.status_code)
    if resp.status_code == 200:
        data = resp.json()
        save_data(data)

        if len(data) < 100:
            break

        page += 1
        time.sleep(2)
    else:
        time.sleep(60*15)


# %%
# %%
