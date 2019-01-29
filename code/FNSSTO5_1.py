import pandas as pandas
import csv
import numpy as np

# name of data file
summary_file_name = "../data/Profiles_2018.csv"
exploratory_file_name = "../output_files/FNSSTO5_1.csv"

# variables
preset_variables = ["BPSHE31_1_1", "BPSHE31_2_1", "BPSHE31_3_1", "BPSHE31_4_1",
                    "BPSHE31_5_1", "BPSHE31_6_1", "BPSHE31_7_1", "BPSHE31_8_1",
                    "BPSHE31_9_1", "BPSHE31_10_1", "BPSHE31_11_1", "BPSHE31_12_1",
                    "BPSHE31_13_1"]
preset_variables2 = ["BPSHE31_1_9", "BPSHE31_2_9", "BPSHE31_3_9", "BPSHE31_4_9",
                    "BPSHE31_5_9", "BPSHE31_6_9", "BPSHE31_7_9", "BPSHE31_8_9",
                    "BPSHE31_9_9", "BPSHE31_10_9", "BPSHE31_11_9", "BPSHE31_12_9",
                    "BPSHE31_13_9"]
postset_variable = "FNSSTO5_1"
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
    # add new CHE_STO2_2 column and initialize to blank
    df[postset_variable] = ""

    # set CHE_STO2_2 column
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

    count = 0
    null_count = 0
    for idx, variable in enumerate(variables):
        if (variable == 1) & (variables2[idx] != 1):
            count += 1
        elif (variable == 1) & (variables2[idx] == 1):
            return 0
        elif pandas.isnull(variable):
            null_count += 1

    if null_count == len(variables):
        return np.nan
    else:
        if count >= 1:
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
