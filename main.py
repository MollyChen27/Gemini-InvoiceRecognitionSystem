import google.generativeai as genai
import os
import PIL.Image
import pandas as pd
# from datetime import datetime

from analyze import *
from sendEmail import *

# 指定目录路径
directory = 'receipt'
# 获取目录中的所有文件列表
files = os.listdir(directory)
# 统计文件数量
file_count = len(files)

# 创建数据框
# df = pd.read_excel("output.xlsx")
df = pd.DataFrame(columns=['store', 'date', 'total', "type"])


genai.configure(api_key=os.environ['Gemini_API_KEY'])

model_vision = genai.GenerativeModel('gemini-pro-vision')
model_text = genai.GenerativeModel('gemini-pro')

for i in range(1,file_count+1):
    image_path = f"receipt\\{i}.jpg"
    img = PIL.Image.open(image_path)

    
    response = model_vision.generate_content(["請依照圖片中的文字 給我店名、消費年份和月份、消費金額，自行從店名判斷\
                                        是以下哪個產業,必須以英文當tag:Restaurants, retail, healthcare, tourism, education, transportation 且依照\
                                        以下格式 以逗號分開三者 ex: 福利中心, 2022-07, 50, retail ex: 馬偕醫院, 2024-08, 250, healthcare \
                                        ", img])


    result = response.text
    # 将提取的数据存入 DataFrame
    text = [item.strip() for item in result.split(",")]
    store = text[0]
    date = text[1]
    total = int(text[2])
    type = text[3]
    df.loc[i-1] = [store, date , total, type]

# 數據分析
amountPerMonth(df)
typeUnique(df)

# 年度總結每月每個項目支出 是否超出預算
checkbudget(df)

df_sorted = df.sort_values(by='date')
df_sorted.to_excel('output.xlsx', index=False)


