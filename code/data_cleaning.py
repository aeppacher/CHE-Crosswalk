import pandas as pandas
import csv
import numpy as np

# name of data file
data_df_name = "../data/Profiles_2018.csv"

def main():
    # load data via pandas
    data_df = pandas.read_csv(data_df_name)

    # replace blank fields with nan
    data_df = clean_blanks(data_df)

    # replace all numbers formatted as strings as floats
    data_df = format_values(data_df)

    data_df.to_csv(data_df_name, index=False)

def clean_blanks(df):
    return df.replace(r'^\s*$', np.nan, regex=True)

def format_values(df):
    return df.apply(pandas.to_numeric, errors='ignore')

if __name__ == "__main__":
    main()