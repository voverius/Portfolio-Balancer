import os
import json


def LoadConfig(index=[]):

    """
    :param index:   input index to load from TraingingPackages/, empty loads from Configurations/
    :return:        .json Config file
    """

    path = 'D:\\OneDrive\\Trade\\Daft Punk'

    if index:
        folder_path = path + '\\TrainingPackages\\' + str(index) + '\\net_config_original.json'
    else:
        folder_path = path + '\\Configurations\\' + 'net_config_original.json'

    with open(folder_path) as file:
        config = json.load(file)

    return config


if __name__ == "__main__":
    LoadConfig()

