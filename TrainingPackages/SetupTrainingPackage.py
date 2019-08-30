import os
from Configurations.LoadConfig import *
from shutil import copyfile


def SetupTrainingPackage(package):

    package_directory = 'D:\\OneDrive\Trade\\Daft Punk\\TrainingPackages\\' + str(package)
    config_directory = package_directory + '\\net_config_original.json'
    copy_over = False

    # Check if the main folder exists
    if os.path.isdir(package_directory):
        if not os.path.exists(config_directory):
            copy_over = True
    else:
        os.mkdir(package_directory)
        copy_over = True

    # Check if tensorflow directories exist
    tensorboad_directoy = package_directory + '\\tensorboard'
    if not os.path.isdir(tensorboad_directoy):
        os.mkdir(tensorboad_directoy)
        os.mkdir(tensorboad_directoy + '\\network')
        os.mkdir(tensorboad_directoy + '\\test')
        os.mkdir(tensorboad_directoy + '\\train')

    # If there's no config in the folder, copy it over from the original
    if copy_over:
        original_directory = 'D:\\OneDrive\Trade\\Daft Punk\\Configurations\\net_config_original.json'
        copyfile(original_directory, config_directory)

    # Load the config file
    config = LoadConfig(package)
    config['package'] = package
    config['package_directory'] = package_directory + '\\'

    return config


if __name__ == "__main__":
    SetupTrainingPackage()












