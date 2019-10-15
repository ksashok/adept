# MasterCard Consolidated Billing pdf to excel

This project is a Python application which takes the MasterCard Consolidated Billing pdf file and extracts it's contents to an excel output

Language used   : Python 3.7
Modules used    : pyMuPdf, pandas, numpy , re

# Customisations
  - The string at the end of the page is noted as 
  "Privacy Policy |  Copyright © 1991–2013 MasterCard. Proprietary. All rights reserved." and it should be updated at the variable end_of_page in case there is a change. This is needed to ignore the contents and not have these values in the tables.

    ```
    end_of_Page = "Privacy Policy |  Copyright © 1991–2013 MasterCard. Proprietary. All rights reserved."
    ```
- The start of the table is seen as any text starting with "The following rates apply:\n". If there is any change the below variable needs to be updated.

    ```python
    table_start = "The following rates apply:\n"
    ```
- The headers of the table vary and needs to be tracked. The below are the seen table headers. If there is any addition, the below variable should be updated accordingly. The headers should be seperated with "\s+" to accomodate for space or any character the table might have.
    ```
    table_header = ["Tier\s+Tier Ending Value\s+Rate", 
                "Customer\s+Rate", 
                "Acquirer\s+Issuer\s+Rate",
                "Acquirer\s+Rate",
                "Issuer\s+Rate",
               "Issuer\s+Destination\s+Rate",
               "Event ID\s+Product\/Program\/Service\s+Rate"]
    ```
# Running the project locally

  - Clone the repository
    ```sh
    git clone 
    ```
  - Go to the project folder and execute the below script to convert the pdf into excel file.
    ```sh
    python mcbspdf.py
    ```

# Limitations
- The project would not work the start of the tables are not consistent.
