import pandas


def info_get(path_to_file):
    with open(path_to_file, 'r') as file:
        data=file.readlines()
    return data


def convert_info(data):
    i=0
    while not data[i].startswith('='):
        i+=1
    i+=1
    films=[]
    for j in range(i, len(data)-1):    
        name=data[j].split('(')[0]
        year=data[j].split('(')[1][:4]
        row_for_location=data[j].split('\t')
        amount=row_for_location.count('')
        for i in range(amount):
            row_for_location.remove('')
        locations=row_for_location[1:]
        location=' '.join(locations)
        location=location[:-1]
        films.append((name, year, location))
    return films


if __name__ == '__main__':
    data=info_get('locations.list')
    films=convert_info(data)
    print(films)
