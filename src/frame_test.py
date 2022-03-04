import json
from random import sample
import numpy as np
import frame as pd
import argparse


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-f", type=str, required=True,  help='Path to json file')
    args = parser.parse_args()

    #read and load maze
    json_path = args.file

    with open(json_path, "r") as f:
        json_constants = json.load(f)



    sample_df = pd.DataFrame(
                    json_constants[0]['path'], 
                    columns = json_constants[0]['header_columns'],
                    dtypes = json_constants[0]['data_types']
                )

    customer_df = pd.DataFrame(
                    json_constants[1]['path'], 
                    columns = json_constants[1]['header_columns'],
                    dtypes = json_constants[1]['data_types']
                )


    merged1 = customer_df.merge(sample_df, sample_df.columns[0])
    merged1.to_csv("customer_merged.csv")

    invoice_df = pd.DataFrame(
                    json_constants[2]['path'], 
                    columns = json_constants[2]['header_columns'],
                    dtypes = json_constants[2]['data_types']
                )

    merged2 = invoice_df.merge(customer_df, customer_df.columns[0])
    merged2.to_csv("invoice_merged.csv")

    item_df = pd.DataFrame(
                    json_constants[3]['path'], 
                    columns = json_constants[3]['header_columns'],
                    dtypes = json_constants[3]['data_types']
                )

    merged3 = item_df.merge(invoice_df, invoice_df.columns[1])
    merged3.to_csv("item_merged.csv")
