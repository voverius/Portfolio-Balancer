import pandas as pd
import os


def LoadMaster(name, location=1):

    """
    :param name:        name of the stored Master file
    :param location:    1 - Parallel, 0 - Root Folder
    :return:            a pandas dataframe
    """

    # Set the location
    file_path = os.path.dirname(os.getcwd())
    if location == 1:  # For Parallel Folders
        file_path = file_path + '\\stored\\' + name + '.csv'
    elif location == 0:  # For Root Folder
        file_path = file_path + '\\Daft Punk\\stored\\' + name + '.csv'

    df = pd.read_csv(file_path)
    df.date = pd.to_datetime(df.date, format='%d.%m.%Y %H:%M:%S.%f', errors='ignore')
    df = df.set_index(df.date)
    df = df.drop(['date'], axis=1)

    return df


if __name__ == "__main__":
    LoadMaster()


