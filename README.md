# stonebranch-assignment



A Python library for parsing effieciently csv files. It supports I/O and merge operations.
Folder **`/src`** contains the source code of the project, while folder **`/input`** some csv files to run the test script. 

## Installation


The package does not have any dependencies besides Python itself.



## Usage

To test the code run

```bash
python3 frame_test.py -f ../data.json
```


## Input output.
The test scripy **`frame_test`** expects an argument of the path to a json file. 
This JSON file has the following structure and contains path, column names and data type( for each column), for each csv file.

**`data.jsojn`**:

```python
[
    {
        "path": "../input/CUSTOMER_SAMPLE.csv",
        "header_columns" : ["CUSTOMER_CODE"],
        "data_types" : ["CHAR"]   
    },
    {
        "path": "../input/CUSTOMER.csv",
        "header_columns" : [
                            "CUSTOMER_CODE",
                            "FIRSTNAME",
                            "LASTNAME"
                        ],
        "data_types" : ["CHAR","CHAR","CHAR" ]   
    },
    {
        "path": "../input/INVOICE.csv",
        "header_columns" : [
                            "CUSTOMER_CODE",
                            "INVOICE_CODE",
                            "AMOUNT",
                            "DATE"
                        ],
        "data_types" : ["CHAR","CHAR","FLOAT", "DATE" ]   
    }, 
    ....
    ....
]
```
This way it can support more csv file just by adding the required info. Parent folder also contains an **`/input folder`** that stores the csv files used for testing.

## License
[MIT](https://choosealicense.com/licenses/mit/)
