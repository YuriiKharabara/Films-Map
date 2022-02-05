import pandas


def info_get(path_to_file):
    with open(path_to_file, 'r') as file:
        data=file.readlines()
    return data




if __name__ == '__main__':
    data=info_get('locations.list')
    print(data)
