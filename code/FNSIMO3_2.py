import pandas as pandas
import csv
import numpy as np

# name of data file
summary_file_name = "../data/Profiles_2018.csv"
exploratory_file_name = "../output_files/FNSIMO3_2.csv"

# variables
preset_variables = ["P30_1", "P30_2", "P30_3", "P30_4", "P30_5", "P30_6", "P30_7", "P30_9", "P30_10", "P30_11",
                    "P30_12", "P30_14", "P30_16"]
preset_variables2 = ["P30_1", "P30_2", "P30_3", "P30_4", "P30_5", "P30_6", "P30_7", "P30_8", "P30_9", "P30_10",
                    "P30_11", "P30_12", "P30_14", "P30_16"]
postset_variable = "FNSIMO3_2"
columns = ["School_Name", "School_ID", "AR_Type"] + [postset_variable] + preset_variables + preset_variables2

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

    df_explor = df_explor.sort_values(by=["School_Name", postset_variable], ascending=False)

    return df_explor

def compliance_level(row):
    variables = []
    variables2 = []

    for pre_var in preset_variables:
        variables.append(row[pre_var])

    for pre_var in preset_variables2:
        variables2.append(row[pre_var])

    AR_Type = row["AR_Type"]
    BPSP77_7 = row["BPSP77_7"]
    BPSP77_8 = row["BPSP77_8"]

    if (AR_Type == '="K-12"') | (AR_Type == '="6-12"') | (AR_Type == '="9-12"'):
        count = 0
        null_count = 0
        else_count = 0
        for variable in variables:
            if (variable == 1):
                count += 1
            elif pandas.isnull(variable):
                null_count += 1

        if null_count == len(variables):
            return np.nan
        else:
            if count >= 13:
                return 1
            else:
                return 0
    elif(AR_Type == '="K-5"') | (AR_Type == '="K-8"') | (AR_Type == '="6-8"'):
        count = 0
        null_count = 0
        for variable in variables2:
            if (variable == 1) | (variable == 3):
                count += 1
            elif pandas.isnull(variable):
                null_count += 1

        if null_count == len(variables):
            return np.nan
        else:
            if count >= 14:
                return 1
            else:
                return 0
    else:
        return np.nan


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