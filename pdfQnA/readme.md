# PDF QnA

This project is a Python application which takes in any pdf document and tries to respond to matching sentences for a given question phrase.

Language used   : Python 3.7
Modules used    : flask, pandas, numpy , re, spacy, nltk

# Running the live project
The project has been hosted at https://anzqna.herokuapp.com/ which has been trained with the "ANZ Breakfree Terms and Conditions" pdf document dated 2 September 2019.

# Running the project locally

  - Clone the repository
    ```sh
    git clone 
    ```
  - Go to the project folder and execute the below script to convert the pdf into excel file.
    ```sh
    python app.py
    ```

# Making the program work for any pdf document
To make the program work for any pdf document, please follow the below process

 - Program processFile.py is used to covert any pdf document into a dataframe pickle which would be used by the program.
 - Update the location of the pdf filepath in place of the below variable in the program processFile.py
     ```python
     filepath = "TO BE UPDATED"
    ```
 - Execute the program by running the below command.
      ```python
      python processFile.py
      ```
 - Executing the program would update the pickle file which would be used by the app.py
 - Restart app.py and run again
    ```python
    python app.py
    ```
 - Now open the below link in the browser to see the live application running locally which can be used to ask any question related to the new document.
    ```html
    http://127.0.0.1:5000
    ```
 
# Improvements
- Have file upload in the browser to make the program adaptable for any pdf document which would avoid using the processFile.py seperately.
