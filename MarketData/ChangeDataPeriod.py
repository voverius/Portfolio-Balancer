import os
import numpy as np
from os import listdir
from os.path import isfile, join


def ChangeDataPeriod(original_loc, new_loc, pairs=[], exchange='Poloniex'):

    '''
    :param original_loc:    Location from which to take data
    :param new_loc:         Location where to put new data
    :param pairs:           List of specific pairs to update
    :param exchange:        Exchange used for updating
    :return:                Longer time period matrix.

    !!! SO FAR THIS CAN ONLY CONVERT FROM MINUTES TO ANYTHING ELSE !!!
    '''

    original_file_path = os.path.dirname(os.getcwd())
    original_file_path = original_file_path + '\\ExchangeData\\' + exchange + '\\' + original_loc + '\\'
    original_file_list = [f for f in listdir(original_file_path) if isfile(join(original_file_path, f))]

    if len(pairs) > 0:
        temp = original_file_list.copy()
        original_file_list = []

        for pair in pairs:
            for address in temp:
                if pair == address.split(' ')[0]:
                    original_file_list.append(address)
                    break

    if new_loc[-1] == 'M':
        period = int(new_loc[:-1]) * 60
        offset = int(int(new_loc[:-1]) / int(original_loc[:-1]))
    elif new_loc[-1] == 'H':
        period = int(new_loc[:-1]) * 60 * 60
        offset = int(int(new_loc[:-1]) * 60 / int(original_loc[:-1]))
    elif new_loc[-1] == 'D':
        period = int(new_loc[:-1]) * 60 * 60 * 24
        offset = int(int(new_loc[:-1]) * 60 * 24 / int(original_loc[:-1]))

    start_position = 0
    finish_position = 1

    # Save the file
    save_path = os.path.dirname(os.getcwd())
    save_path = save_path + '\\ExchangeData\\' + exchange + '\\' + new_loc + '\\'
    new_file_list = [f for f in listdir(save_path) if isfile(join(save_path, f))]

    print(f'Calculating {exchange} - {len(original_file_list)} pairs for {new_loc} period')

    for name in original_file_list:

        flag = False  # False - new file, True - Update existing file
        original = np.load(original_file_path + name)
        data = name.split(' ')
        beginning = 0

        for target_name in new_file_list:
            if name.split(' ')[0] == target_name.split(' ')[0]:
                flag = True
                target = np.load(save_path + target_name)
                beginning = np.where(original[:, 0] == target[-1, 0])[0][0]
                break

        # Cutting off the start and end to have divisible time periods
        for i in range(beginning, (beginning + 100)):
            if original[i, 0] % period == 0:
                start_position = i
                break
        for i in range(1, 100):
            if original[-i, 0] % period == 0:
                finish_position = i
                break

        count = int((original[-finish_position, 0] - original[start_position, 0]) / period)

        if count > 0:

            new = np.zeros((count, 6))
            for i in range(0, count):

                start = i*offset + (start_position + 1)
                finish = i*offset + (start_position + 1) + (offset - 1)

                # Time
                new[i, 0] = original[finish, 0]

                # OHLC
                new[i, 1] = original[start, 1]
                new[i, 2] = max(original[start:(finish+1), 2])
                new[i, 3] = min(original[start:(finish+1), 3])
                new[i, 4] = original[finish, 4]

                # Volume
                new[i, 5] = sum(original[start:(finish+1), 5])

            # Saving the files
            new_file_name = data[0] + ' ' + new_loc + ' ' + str(int(new[-1, 0])) + '.npy'

            if flag:
                if not original[-finish_position, 0] == target[-1, 0]:
                    updated = np.concatenate((target, new), axis=0)
                    np.save((save_path + target_name), updated)
                    os.rename((save_path + target_name), (save_path + new_file_name))

            else:
                np.save((save_path + new_file_name), new)


if __name__ == "__main__":
    ChangeDataPeriod()

