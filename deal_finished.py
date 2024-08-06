import pandas as pd

# Load the data

path_finished="/Users/pro/Documents/pdf/all/finished_book.txt"

path_all="/Users/pro/Documents/pdf/all/res_book_index.xlsx"


finished_book=[]
with open(path_finished, 'r') as f:
    all=f.readlines()[0]
    print(len(all))
    x=[i+"}" for i in all.split("}") if i]
    for j in x:
        finished_book.append(eval(j))

data=pd.read_excel(path_all)
data["download_url"]=data["detail_url"].str.replace("detail","download")

finished=pd.DataFrame(finished_book)

all=pd.merge(data,finished,left_on="download_url",right_on="downloadUrl",how="left")

all.to_excel("/Users/pro/Documents/pdf/all/res_book_index_finished.xlsx",index=False)
        

