import pandas as pandas
import csv
import numpy as np

# name of data file
data_df_names = ["../output_files/PEPASTO2_1.csv",
                 "../output_files/PEPASTO3_1.csv",
                 "../output_files/PEPASTO3_2.csv",
                 "../output_files/PEPASTO4_1.csv",
                 "../output_files/PEPASTO5_1.csv"]

def main():
    for data_df_name in data_df_names:  
        # load data via pandas
        data_df = pandas.read_csv(data_df_name)

        # sort by AR_Type
        data_df = sort_by_ar_type(data_df)

        data_df.to_csv(data_df_name, index=False)

def sort_by_ar_type(df):
    return df.sort_values(by=['AR_Type'])

if __name__ == "__main__":
    main()