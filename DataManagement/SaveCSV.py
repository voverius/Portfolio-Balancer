import csv
import os


def SaveCSV(name, location='stored'):

    """
    :param file:        Pass the file to be saved as CSV
    :param name:        The name for file 'xxx.csv'
    :param location:
    :return:
    """

    # Setting the Raw Data file direction
    path = os.path.dirname(os.getcwd())
    path = path + '\\' + location + '\\' + name + '.csv'

    # Saving the file

    return path










