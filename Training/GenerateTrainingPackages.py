import json
import os


def GenerateTrainingPackages(config, count=1):
    path = os.path.dirname(os.getcwd())
    folder_path = path + '\\TrainingPackages\\'

    # Checking for existing sub-directories
    SubDirectories = [int(s) for s in os.listdir(folder_path) if os.path.isdir(folder_path+"/"+s)]

    if SubDirectories:
        MaxNum = max(SubDirectories)
    else:
        MaxNum = 0

    for i in range(count):
        MaxNum += 1
        NewDirectory = folder_path + str(MaxNum)
        config["random_seed"] = i
        os.makedirs(NewDirectory)

        with open(NewDirectory + "/" + "net_config_original.json", 'w') as outfile:
            json.dump(config, outfile, indent=4, sort_keys=True)


if __name__ == "__main__":
    GenerateTrainingPackages()

