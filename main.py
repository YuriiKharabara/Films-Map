import folium
from geopy.geocoders import Nominatim

def info_get(path_to_file):
    """Read file and put them into list of rows

    Args:
        path_to_file (str): Path to file with films

    Returns:
        list: All the rows from the file in list
    """
    with open(path_to_file, 'r') as file:
        data=file.readlines()
    return data


def convert_info(data):
    """Convert data into list of tuples

    Args:
        data (list): all the rows from the file in list

    Returns:
        list: List of tuples, where: (film name, year, location)
    >>> convert_info(info_get('locations.list')[15:17])
    [('"#1 Single" ', '2006', 'New York City, New York, USA')]
    """
    i=0
    try:
        while not data[i].startswith('='):
            i+=1
        i+=1
    except IndexError:
        i=0
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

def get_coords(place):
    geolocator = Nominatim(user_agent="main.py")
    location = geolocator.geocode(place)
    return (location.latitude, location.longitude)



    pass

if __name__ == '__main__':
    data=info_get('locations.list')
    films=convert_info(data)
    get_coords('New York City, New York, USA')
