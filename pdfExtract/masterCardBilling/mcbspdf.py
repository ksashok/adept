import fitz
import re
import numpy as np
import pandas as pd

filename = "MCBS.pdf"

end_of_Page = "Privacy Policy |  Copyright © 1991–2013 MasterCard. Proprietary. All rights reserved."
table_start = "The following rates apply:\n"
table_header = ["Tier\s+Tier Ending Value\s+Rate", 
                "Customer\s+Rate", 
                "Acquirer\s+Issuer\s+Rate",
                "Acquirer\s+Rate",
                "Issuer\s+Rate",
               "Issuer\s+Destination\s+Rate",
               "Event ID\s+Product\/Program\/Service\s+Rate"]

def extractText(file): 
    doc = fitz.open(file) 
    text = []
    for page in doc: 
        t = page.getText().encode("utf8") 
        text.append(t)
    return text

data = extractText(filename)
data_dc = [page.decode("utf-8") for page in data]
data_dc = [re.sub('\d{1,3}\sof\s\d{3}\\n','',page) for page in data_dc]
data = ''.join(data_dc)
data = (data.split("Billing Events\n")[1])



main_section = re.findall('([A-Z].*—[A-Z][A-Z\d]\\n[\s\S]+?)(?=\\n[A-Z].*—[A-Z][A-Z\d]\\n|'+end_of_Page+')',data,re.MULTILINE)
           
export = []
for topic in main_section:
    billing, sections, billing_name, billing_code = '','','',''
    
    billing = re.findall('([A-Z]?.*—[A-Z][A-Z\d])\\n(.*?)[2TP][A-Z]{1,2}[A-WYZ\d]{2}\d{2}[A-Z]{0,2}',topic, re.DOTALL)
    
    billing_name, billing_code = billing[0][0].rsplit("—",1)
    #sections = re.findall('([2TP][A-Z\d\*]{1,2}[A-WYZ\d]{2}\d{2,4}[A-Z]{0,2}[\\n|\s\s\s].*?)(?=\\n[2TP][A-Z\d\*]{1,2}[A-WYZ\d]{2}\d{2,4}[A-Z]{0,2}.*?'+billing_code+'|$)',topic, re.DOTALL)
    sections = re.findall('([2TP][A-Z\d\*]{1,2}[A-WYZ\d]{2}\d{2,4}[A-Z]{0,2}[\\n|\s\s\s].*?)(?=\\n[2TP][A-Z\d\*]{1,2}[A-WYZ\d]{2}\d{2,4}[A-Z]{0,2}.{,150}?'+billing_code+'|$)',topic,re.DOTALL)
    
    sections = [section for section in sections if len(section)>1]
    
    for section in sections:
        #print(repr(section))
        section_details, table, section_header, section_description,section_code,section_title,table,table2,\
        table_list,table_list2,records,records2 = '','','','','','','','','','','',''
        
        if table_start in section:
            section_details, table  = section.split(table_start)
            section_header, section_description = section_details.rsplit(billing_code,1)
            if "\n" in section_header.strip():
                section_code, section_title = section_header.strip().split("\n",1)
            else:
                section_code, section_title = section_header.strip().split(" ",1)
            
            #table_bool = [sub_str in table for sub_str in table_header]
            table_bool = [re.search(pattern,table)!=None for pattern in table_header]
            if True in table_bool:
                table_head = table_header[table_bool.index(True)]
                table_colsize = len(table_head.split("\s+"))
                #print(repr(table.split("\n")))
                if table_head == table_header[6]:
                    records = re.findall('([2TP][A-Z\d\*]{1,2}[A-WYZ\d]{2}\d{2,4}[A-Z]{0,2})[\\n|\s\s\s](.*?)(?=\\n[2TP][A-Z\d\*]{1,2}[A-WYZ\d]{2}\d{2,4}[A-Z]{0,2}.{,25}?|$)',table,re.DOTALL)
                    table_list = [[line[0],line[1].rsplit("\n",1)[0],line[1].rsplit("\n",1)[1]] for line in records]
                else:
                    records = re.split("\\n|\s{3,}",table)
                    records = [record.strip() for record in records if len(record)>1]
                    table_list = np.array(records).reshape(-1, table_colsize)
                    table_list = ['\t'.join(a) for a in table_list]
    
            
        else:
            #table_bool = [sub_str in section for sub_str in table_header]
            table_bool = [re.search(pattern,section)!=None for pattern in table_header]
            #print(repr(section))
            if True in table_bool:
                table_head = table_header[table_bool.index(True)]
                #print(repr(table_head))

                section_details = re.split(table_head,section)
                if len(section_details) == 2:
                    table = table_head + section_details[1]
                    table_colsize = len(table_head.split("\s+"))
                    records = re.split('\\\s\+|\n',table)
                    records = [record.strip() for record in records if len(record)>0]
                    table_list = np.array(records).reshape(-1, table_colsize)
                    table_list = ['\t'.join(a) for a in table_list]
        
                else:
                    #print(repr(section_details[0]))
                    section2 = (re.findall('(.*)(The Standard Tier.*)',section_details[1],re.DOTALL)[0])
                    table = section2[0]
                    table = table_head + table
                    table_colsize = len(table_head.split("\s+"))
                    records = re.split('\\\s\+|\n',table)
                    records = [record.strip() for record in records if len(record)>0]
                    table_list = np.array(records).reshape(-1, table_colsize)
                    table_list = ['\t'.join(a) for a in table_list]
                    
                    content2 = section2[1]
                    table2 = section_details[2]
                    
                    table2 = table_head + table2
                    table_colsize = len(table_head.split("\s+"))
                    records2 = re.split('\\\s\+|\n',table2)
                    records2 = [record.strip() for record in records2 if len(record)>0]
                    table_list2 = np.array(records2).reshape(-1, table_colsize)
                    table_list2 = ['\t'.join(a) for a in table_list2]
                    

                    
                    
                section_code, section_title, section_billing, section_description = section_details[0].split("\n",3)
                
                
                
                
            
        if(table_list2):
            export.append([billing_name,billing_code,section_code,section_title,section_description,table_list,content2,table_list2])
        else:
            export.append([billing_name,billing_code,section_code,section_title,section_description,table_list])


df = pd.DataFrame(export)
df.to_excel("export2.xlsx", index=False)