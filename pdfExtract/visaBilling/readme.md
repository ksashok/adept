# Visa Billing Line pdf to excel

This project is a Python application which takes the Visa Billing Line pdf file and extracts it's contents to an excel output

Language used   : Python 3.7
Modules used    : pdfminer.six, pandas, BeautifulSoup, re

# Customisations
  - The html file can be seen to check the column starting values. Check the 'left:xxpx' values for each row and confirm it is consistent. The previous file had the values 26, 98 and 260 respectively as seen below.
      ```html
        <br></span></div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:26px; top:1236px; width:49px; height:12px;"><span style="font-family: b'Tahoma'; font-size:12px">1B1106003
        <br></span></div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:98px; top:1236px; width:152px; height:12px;"><span style="font-family: b'Tahoma'; font-size:12px">VISANET PROCESSING DISCOUNT
        <br></span></div><div style="position:absolute; border: textbox 1px solid; writing-mode:lr-tb; left:260px; 
      ```
    
    If there is any change in these values the variable in the program need to be updated.
      ```python
        left_size = [26,98,260]
      ```

- The table headers are consistent and are stored as variable 'ignore'. If there is any change in the table headers, the below variable in the program need to be updated.

    ```python
    ignore = ['Billing Line Listing','Line No.','Invoice Description','Long Description']
    ```
# Running the project locally

  - Clone the repository
    ```sh
    git clone 
    ```
  - Go to the project folder and execute the below script to convert the pdf into html
    ```sh
    python pdf2txt.py file.pdf -p output.html -t html
    ```
  - The below command takes the converted html file and convert it into excel file
    ```sh
    python visaBilling.py
    ```

# Limitations
- The project would not work if the left tags of the rows are not following any consistent order
- The project would not work if the table headers not consistent throughtout the document
