import csv
import pandas as pd
import requests
from PIL import Image
from io import BytesIO
import os



csv_file = 'KF_HF_train_dataset.csv'
download_folder = 'AHOVA AKAROD HOGY LETOLTSE'
lp = pd.DataFrame()

with open(csv_file, 'r') as file:
    lp = pd.read_csv(file, index_col=0)

lp_links = lp.iloc[:,2]
# Ezekből csak a User-Agenttel értem el áttörést, ki tudjátok másolni Chrome -> Inspect / Vizsgálat -> Network -> Fejlécek
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
          "Cookie" : "_ga=GA1.1.454708434.1695737815; _ga_HJ9CCY4MCD=GS1.1.1695741775.2.1.1695742002.34.0.0; cf_chl_rc_i=1; cf_chl_2=79fe3487d12a9db",
          "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
          "authority" : "img03.platesmania.com",
          "Referer" : "http://img03.platesmania.com/220605/inf/1923338914b553.png?__cf_chl_tk=8fD5CgrU4oEs_.ECZx6YikWR94NhBhc0Krhp.EYS0As-1696772851-0-gaNycGzNB1A"
          }
for url in lp_links:
    base_url = os.path.basename(url)
    save_path = os.path.join(download_folder, base_url)
    statuscode = 0
    response = requests.get(url, headers = header)
    statuscode = response.status_code    
    if not os.path.exists(save_path):
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.save(save_path)
        else:
            print(f"Failed to download image. {url} {statuscode}")