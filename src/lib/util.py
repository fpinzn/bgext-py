import numpy as np

# expects a dict with the form {key: numpy array,...}

def format_csv(counter):
    assert type(counter) == dict
    # checks all arrays in the dict are the same size
    assert len(set(map(lambda k: counter[k].size, counter.keys()))) == 1

    file_content = 'frame'
    number_of_frames = counter[list(counter.keys())[0]].size
    for k in counter.keys():
        file_content += ',' + str(k)

    for i in range(number_of_frames):
        file_content += '\n' + str(i)
        for k in counter.keys():
            file_content += ',' + str(counter[k][i])

    return file_content

def calc_diffs(counter):
    assert type(counter) == dict
    # checks all arrays in the dict are the same size
    assert len(set(map(lambda k: counter[k].size, counter.keys()))) == 1

    result = {}
    for k in counter.keys():
        # displaces the values one position and deletes the last one
        print(counter)
        displaced = np.insert(counter[k][:-1], 0, counter[k][0])
        print(displaced, counter[k])
        print(counter[k] - displaced)
        result[k] = np.absolute(counter[k] - displaced)

    return result

def prefix_dict_keys(dictionary, prefix):
    assert type(dictionary) == dict

    result = {}
    for k in dictionary.keys():
        result[prefix+k] = dictionary[k]
    return result

def write_to_file(data, file_name):
    output_file = open(file_name, 'w')
    output_file.write(str(data))
    output_file.close()
