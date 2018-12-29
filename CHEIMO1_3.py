import pandas as pandas
import csv

# name of data file
summary_file_name = "Profiles_2018.csv"
exploratory_file_name = "CHEIMO1_3.csv"

def main():
    # load data via pandas
    summary_df = pandas.read_csv(summary_file_name)

    # creation of exploratory dataframe
    preset_variables = ["BPSHE32_11", "BPSHE32_12", "BPSHE32_13", "BPSHE32_14"]
    postset_variable = "CHEIMO1_3"
    columns = ["School_Name", "School_ID"] + [postset_variable] + preset_variables

    exploratory_df = pandas.DataFrame(columns = columns)

        # initialize empty lists and 0 counts
    compliant_schools = []
    non_compliant_schools = []
    school_count = 0
    compliant_school_count = 0

    summary_df = set_summary_values(summary_df, postset_variable, preset_variables)
    exploratory_df = set_exploratory_values(summary_df, exploratory_df, columns, postset_variable, preset_variables)

    summary_df.to_csv(summary_file_name, index=False)
    exploratory_df.to_csv(exploratory_file_name, index=False)

def set_summary_values(df, postset_variable, preset_variables):
    # add new CHESTO3_1 column and initialize to blank
    df[postset_variable] = ""

    # set CHESTO3_1 column
    for index, school in df.iterrows():
        compliance_value = compliance_level(school, preset_variables)

        set_cell(df, compliance_value, index, postset_variable)

    return df

def set_exploratory_values(df_sum, df_explor, columns, postset_variable, preset_variables):
    for index, school in df_sum.iterrows():
        compliance_value = compliance_level(school, preset_variables)

        df_explor = add_row(df_explor, get_row_values(school, columns))

    df_explor = df_explor.sort_values(by=[postset_variable], ascending=False)

    return df_explor

def compliance_level(row, preset_variables):
    variables = []

    for pre_var in preset_variables:
        variables.append(row[pre_var])

    count = 0
    for variable in variables:
        if variable == 1:
            count += 1

    if count >= 1:
        return 1
    else:
        return 0

def set_cell(df, value, row_name, col_name):
    df.at[row_name, col_name] = value

def get_row_values(row, columns):
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