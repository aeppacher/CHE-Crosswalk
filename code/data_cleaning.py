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

    # format variables that excel confuses as text
    data_df = format_to_text(data_df, ["AR_Type"])

    data_df.to_csv(data_df_name, index=False)

def clean_blanks(df):
    return df.replace(r'^\s*$', np.nan, regex=True)

def format_values(df):
    return df.apply(pandas.to_numeric, errors='ignore')

def format_to_text(df, list_of_col):
    # loop through all columns to turn to text
    for col_name in list_of_col:
        # loop through all schools (rows)
        for index, school in df.iterrows():
            pre_value = school[col_name]
            post_value = '="' + pre_value + '"'

            set_cell(df, post_value, index, col_name)

    return df

def set_cell(df, value, row_name, col_name):
    df.at[row_name, col_name] = value

def get_value(row, col_name):
    return row[col_name]

if __name__ == "__main__":
    main()