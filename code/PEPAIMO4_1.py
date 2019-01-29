import pandas as pandas
import csv
import numpy as np

# name of data file
summary_file_name = "../data/Profiles_2018.csv"
exploratory_file_name = "../output_files/PEPAIMO4_1.csv"

# variables
preset_variables =  ["CSPAP1_1", "CSPAP1_2", "CSPAP1_3", "CSPAP1_4",
                    "CSPAP1_5", "CSPAP1_6", "CSPAP1_7", "CSPAP1_8",
                    "CSPAP1_9", "CSPAP1_10"]
preset_variables2 = ["CSPAP2_1", "CSPAP2_2", "CSPAP2_3", "CSPAP2_4",
                    "CSPAP2_5", "CSPAP2_6", "CSPAP2_7", "CSPAP2_8",
                    "CSPAP2_9", "CSPAP2_10"]
preset_variables3 = ["CSPAP3_1", "CSPAP3_2", "CSPAP3_3", "CSPAP3_4",
                    "CSPAP3_5", "CSPAP3_6", "CSPAP3_7", "CSPAP3_8",
                    "CSPAP3_9", "CSPAP3_10"]
preset_variables4 = ["CSPAP4_1", "CSPAP4_2", "CSPAP4_3", "CSPAP4_4",
                    "CSPAP4_5", "CSPAP4_6", "CSPAP4_7", "CSPAP4_8",
                    "CSPAP4_9", "CSPAP4_10"]
preset_variables5 = ["CSPAP5_1", "CSPAP5_2", "CSPAP5_3", "CSPAP5_4",
                    "CSPAP5_5", "CSPAP5_6", "CSPAP5_7", "CSPAP5_8",
                    "CSPAP5_9", "CSPAP5_10"]
postset_variable = "PEPAIMO4_1"
columns = ["School_Name", "School_ID", "AR_Type"] + [postset_variable] + preset_variables + preset_variables2 + preset_variables3 + preset_variables4 + preset_variables5

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
    variables3 = []
    variables4 = []
    variables5 = []

    for pre_var in preset_variables:
        variables.append(row[pre_var])
    for pre_var in preset_variables2:
        variables2.append(row[pre_var])
    for pre_var in preset_variables3:
        variables3.append(row[pre_var])
    for pre_var in preset_variables4:
        variables4.append(row[pre_var])
    for pre_var in preset_variables5:
        variables5.append(row[pre_var])


    count = 0
    null_count = 0
    for idx, variable in enumerate(variables):
        sum = 0
        null_temp_count = 0
        pe_null = False
        recess_null = False

        # recess activity
        if (pandas.isnull(variables[idx]) | (variables[idx] == 1)):
            null_temp_count += 1
            recess_null = True
        else:
            sum += variables[idx]

        # movement break activities
        if (pandas.isnull(variables2[idx]) | (variables2[idx] == 1)):
            null_temp_count += 1
        else:
            sum += variables2[idx]

        # classroom lesson activities
        if (pandas.isnull(variables3[idx]) | (variables3[idx] == 1)):
            null_temp_count += 1
        else:
            sum += variables3[idx]

        # PA promotional activities
        if (pandas.isnull(variables4[idx]) | (variables4[idx] == 1)):
            null_temp_count += 1
        else:
            sum += variables4[idx]

        # PE activities
        if (pandas.isnull(variables5[idx]) | (variables5[idx] == 1)):
            null_temp_count += 1
            pe_null = True
        else:
            sum += variables5[idx]

        if (sum >= 150) & (recess_null == False) & (pe_null == False) & (variables5[idx] >= 45) & (variables[idx] >= 100):
            count += 1 

        if null_temp_count >= 4:
            null_count +=1


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
