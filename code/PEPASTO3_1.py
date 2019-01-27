import pandas as pandas
import csv
import numpy as np

# name of data file
summary_file_name = "../data/Profiles_2018.csv"
exploratory_file_name = "../output_files/PEPASTO3_1.csv"

# variables
preset_variables = ["CSPAP1_1", "CSPAP1_2", "CSPAP1_3", "CSPAP1_4", "CSPAP1_5",
                    "CSPAP1_6", "CSPAP1_7"]
postset_variable = "PEPASTO3_1"
columns = ["School_Name", "School_ID", "AR_Type"] + [postset_variable] + preset_variables

def main():
    # load data via pandas
    summary_df = pandas.read_csv(summary_file_name)

    # creation of exploratory dataframe
    exploratory_df = pandas.DataFrame(columns = columns)

    # initialize empty lists and 0 counts
    compliant_schools = []
    non_compliant_schools = []
    school_count = 0
    compliant_school_count = 0

    summary_df = set_summary_values(summary_df)
    exploratory_df = set_exploratory_values(summary_df, exploratory_df)

    summary_df.to_csv(summary_file_name, index=False)
    exploratory_df.to_csv(exploratory_file_name, index=False)

def set_summary_values(df):
    # add new CHESTO3_1 column and initialize to blank
    df[postset_variable] = ""

    # set CHESTO3_1 column
    for index, school in df.iterrows():
        compliance_value = compliance_level(school)

        set_cell(df, compliance_value, index)

    return df

def set_exploratory_values(df_sum, df_explor):
    for index, school in df_sum.iterrows():
        compliance_value = compliance_level(school)

        df_explor = add_row(df_explor, get_row_values(school))

    df_explor = df_explor.sort_values(by=[postset_variable], ascending=False)

    return df_explor

def compliance_level(row):
    variables = []

    for pre_var in preset_variables:
        variables.append(row[pre_var])

    # change this for different compliances
    null_count = 0
    count = 0
    for variable in variables:
        if (variable / 5) >= 20:
            count = count + 1
        elif pandas.isnull(variable) or variable == -999:
            null_count += 1

    if null_count == len(variables):
        return np.nan
    else:
        if count + null_count == len(variables):
            return 1
        else:
            return 0

def set_cell(df, value, row_name):
    df.at[row_name, postset_variable] = value

def get_row_values(row):
    values = []
    for column in columns:
        values.append(row[column])

    return values

def add_row(df, row_values):
    df.loc[-1] = row_values
    df.index = df.index + 1
    return df.sort_index()

if __name__ == "__main__":
    main()