#"C:/Users/Ashok KS/Anaconda3/python.exe" "c:/Users/Ashok KS/Anaconda3/Scripts/pdf2txt.py"  '.\Downloads\Visa Billing Line Listing (October 2014).pdf' -o test2.html -t html
#Python pdf2txt.py file.pdf -p output.html -t html

left_size = [26,98,260]
ignore = ['Billing Line Listing','Line No.','Invoice Description','Long Description']

from bs4 import BeautifulSoup
import pandas as pd
import re

with open("Downloads/test2.html", "r", encoding="utf8") as f:
    
    contents = f.read()

    soup = BeautifulSoup(contents, 'lxml')

line = [[],[],[]]
for a in soup.find_all('div', style=True):
    left = re.findall('left:(\d+)px',a['style'])
    
    text = a.get_text().replace("\n",' ').rstrip()
    
    if text not in ignore and not text.startswith("Page "):
        
        if left:
            if int(left[0]) == left_size[0]:
                line[0].append(text)
            elif int(left[0]) == left_size[1]:
                line[1].append(text)
            elif int(left[0]) == left_size[2]:
                line[2].append(text)

columns=['Line No.','Invoice Description','Long Description']
df = pd.DataFrame(line).T
df.columns = columns
df.to_excel("visa.xlsx",index=False)
