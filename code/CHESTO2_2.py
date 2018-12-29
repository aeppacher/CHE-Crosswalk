import pandas as pandas
import csv

# name of data file
summary_file_name = "../data/Profiles_2018.csv"
exploratory_file_name = "../output_files/CHESTO2_2.csv"

def main():
    # load data via pandas
    summary_df = pandas.read_csv(summary_file_name)

    # creation of exploratory dataframe
    preset_variables = ["BPSHE30_1", "BPSHE30_2"]
    postset_variable = "CHESTO2_2"
    columns = ["School_Name", "School_ID"] + [postset_variable] + preset_variables

    exploratory_df = pandas.DataFrame(columns = columns)

    # initialize empty lists and 0 counts
    compliant_schools = []
    non_compliant_schools = []
    school_count = 0
    compliant_school_count = 0

    summary_df = set_summary_values(summary_df, postset_variable)
    exploratory_df = set_exploratory_values(summary_df, exploratory_df, columns, postset_variable)

    summary_df.to_csv(summary_file_name, index=False)
    exploratory_df.to_csv(exploratory_file_name, index=False)

def set_summary_values(df, postset_variable):
    # add new CHE_STO2_2 column and initialize to blank
    df[postset_variable] = ""

    # set CHE_STO2_2 column
    for index, school in df.iterrows():
        compliance_value = compliance_level(school)

        set_cell(df, compliance_value, index, postset_variable)

    return df

def set_exploratory_values(df_sum, df_explor, columns, postset_variable):
    for index, school in df_sum.iterrows():
        compliance_value = compliance_level(school)

        df_explor = add_row(df_explor, get_row_values(school, columns))

    df_explor = df_explor.sort_values(by=[postset_variable], ascending=False)

    return df_explor

def compliance_level(row):
    BPSHE30_1 = row["BPSHE30_1"]
    BPSHE30_2 = row["BPSHE30_2"]

    if BPSHE30_1 == 1:
        if BPSHE30_2 == 1:
            return 1
        elif BPSHE30_2 == 3:
            return 1
    elif BPSHE30_1 == 3:
        if BPSHE30_2 == 1:
            return 1
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