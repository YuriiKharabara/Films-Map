"""Creates interactive web map of Films"""


import argparse
import folium
from geopy.geocoders import Nominatim
# Функція гаверсинуса написана в додатковому модулі
from haversin import my_haver
import haversine


def info_get(path_to_file):
    """Read file and put them into list of rows

    Args:
        path_to_file (str): Path to file with films

    Returns:
        list: All the rows from the file in list
    """
    with open(path_to_file, 'r') as file:
        data = file.readlines()
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
    i = 0
    try:
        while not data[i].startswith('='):
            i += 1
        i += 1
    except IndexError:
        i = 0
    films = []
    for j in range(i, len(data)-1):
        name = data[j].split('(')[0]
        year = data[j].split('(')[1][:4]
        row_for_location = data[j].split('\t')
        amount = row_for_location.count('')
        for i in range(amount):
            row_for_location.remove('')
        locations = row_for_location[1:]
        location = ' '.join(locations)
        location = location[:-1]
        films.append((name, year, location))
    return films


def get_coords(place):
    """Returns tuple with coords or "None" if nothing was found

    Args:
        place (str): place (for example Los Angeles, California, USA)

    Returns:
        tuple: (latitude, longitude) 
    >>> get_coords('Los Angeles, California, USA')
    (34.0536909, -118.242766)
    >>> get_coords('Alessandria, Piedmont, Italy	(italy)')
    (44.83495335, 8.745030418605868)
    """
    geolocator = Nominatim(user_agent="main.py", timeout=10)
    location = geolocator.geocode(place)
    try:
        try:
            try:
                try:
                    return (location.latitude, location.longitude)
                except AttributeError:
                    city = place.split(',')[0]
                    location = geolocator.geocode(city)
                    return (location.latitude, location.longitude)
            except AttributeError:
                try:
                    higher = place.split(',')[1]
                    location = geolocator.geocode(higher)
                    return (location.latitude, location.longitude)
                except IndexError:
                    higher = place.split(',')[-1]
                    location = geolocator.geocode(higher)
                    return (location.latitude, location.longitude)
        except AttributeError:
            higher = place.split(',')[-1]
            location = geolocator.geocode(higher)
            return (location.latitude, location.longitude)
    except AttributeError:
        return None


def choose_places(data, year):
    """Chooses from file only those which are needed(By year and Lviv)

    Args:
        data (list): data from file
        year (int): year which should be choosen

    Returns:
        tuple: List of data of films (from one year, from Lviv)
    >>> choose_places(convert_info(info_get('locations.list')[15:50]), 2006)
    ([('"#1 Single" ', '2006', 'New York City, New York, USA')], [])
    >>> choose_places(convert_info(info_get('locations.list')[937000:937200]), 2006)
    ([('Nagyaty�r�l ', '2006', 'Odorheiu Secuiesc, Transylvania, Romania (exteriors)'), \
('Naiching�ro ', '2006', 'Japan'), ('Nail Polish ', '2006', 'New Jersey, USA'), ('Nailed ',\
 '2006', 'Belfast, County Antrim, Northern Ireland, UK'), ('Nailed ', '2006', \
'Compton, California, USA'), ('Nailed! ', '2006', 'USA')], [('Najmilszy ze zlodziei ',\
 '1913', 'Lviv, Ukraine')])
    """
    data_of_year = []
    data_of_lviv_films = []
    for i in range(len(data)):
        try:
            if int(data[i][1]) == year:
                data_of_year.append(data[i])
            # if ('Lviv' in data[i][2]) and ('Kyiv' not in data[i][2]) and ('''Miners' Stories''' or 'Delirium' not in data[i][0]):
            if 'Lviv' in data[i][2]:
                data_of_lviv_films.append(data[i])
        except ValueError:
            continue
    for i in data_of_lviv_films:
        coords_of_place = get_coords(i[2])
        if coords_of_place != None:
            if haversine.haversine((49.841952, 24.0315921), coords_of_place) > 300:
                data_of_lviv_films.remove(i)
    return (data_of_year, data_of_lviv_films)


def create_coords_dictionary_with(data_of_year):
    """Creates dictionary of coordinates, where coordinates are keys and films are values

    Args:
        data_of_year (list): all films from one year

    Returns:
        dict: dictionary of coordinates
    >>> create_coords_dictionary_with([('Nagyaty�r�l ', '2006', 'Odorheiu Secuiesc, Transylvania, Romania (exteriors)'), \
('Naiching�ro ', '2006', 'Japan'), ('Nail Polish ', '2006', 'New Jersey, USA'), ('Nailed ',\
 '2006', 'Belfast, County Antrim, Northern Ireland, UK'), ('Nailed ', '2006', \
'Compton, California, USA'), ('Nailed! ', '2006', 'USA')])
    {(46.3047462, 25.2950261): ['Nagyaty�r�l '], (36.5748441, 139.2394179): ['Naiching�ro ']\
, (40.0757384, -74.4041622): ['Nail Polish '], (54.596391, -5.9301829): ['Nailed '],\
 (33.894927, -118.226624): ['Nailed '], (39.7837304, -100.445882): ['Nailed! ']}
    """
    used_coords = {}
    for i in range(len(data_of_year)):
        try:
            coords = get_coords(data_of_year[i][2])
            if coords == None:
                continue
            if coords not in used_coords:
                used_coords[coords] = [data_of_year[i][0]]
            else:
                used_coords[coords].append(data_of_year[i][0])

        except TypeError:
            continue
    return used_coords


def choose_ten_nearest(used_coords, latitude, longitude):
    """Choose ten nearest coords from the dictionary of coords

    Args:
        used_coords (dict): Coordinates of possible popups
        latitude (float): latitude of point from which we should count
        longitude (float): longitude of point from which we should count

    Returns:
        list: list of coordinates which are suitable
    >>> choose_ten_nearest({(34.0536909, -118.242766): 3746204,(36.1622767, -86.7742984)\
: 24005170,(30.272271000000003, -97.76893453598484): 151794832,(40.7127281, -74.0060152): 352256730,(4\
0.7127281, -74.0060152): 705885356,(41.31611085, -74.12629189225156): 1506099870,(41.7065539,\
 -73.9283672): 2472923936,(43.648366800000005, -79.37439532076982): 4857462984,(42.1859079, -7\
6.6699493): 7072726190,(42.1859079, -76.6699493): 9971121196,(40.6526006, -73.9497211): 13680460674,(35.960\
3948, -83.9210261): 18339524720}, 41.31616, -74.126295)
    [(34.0536909, -118.242766), (36.1622767, -86.7742984), (30.272271000000003, -97.76893453598484), \
(40.7127281, -74.0060152), (41.31611085, -74.12629189225156), (41.7065539, -73.9283672), (43.648366800000005, \
-79.37439532076982), (42.1859079, -76.6699493), (40.6526006, -73.9497211), (35.9603948, -83.9210261)]
    """
    nearest_10 = []
    if len(used_coords) <= 10:
        for i in used_coords:
            nearest_10.append(i)
        return nearest_10
    distances = []
    coords_for_distances = []
    for i in used_coords:
        distances.append(haversine.haversine((latitude, longitude), i))
        coords_for_distances.append(i)
    while len(nearest_10) != 10:
        try:
            min_distance_index = distances.index(min(distances))
        except ValueError:
            min_distance_index = 0
        nearest_10.append(coords_for_distances[min_distance_index])
        distances[min_distance_index] += 9999999999999
    return nearest_10


def lviv_places(data_of_lviv):
    """Creates dictionary with films shot in Lviv Region

    Args:
        data_of_lviv (list): List with films shot in Lviv

    Returns:
        dict: dictionary of coordinates
    >>> lviv_places([('Najmilszy ze zlodziei ', '1913', 'Lviv, Ukraine')])
    {(49.841952, 24.0315921): ['Najmilszy ze zlodziei ']}
    """
    used_coords_for_lviv = {}
    for i in range(len(data_of_lviv)):
        try:
            coords = get_coords(data_of_lviv[i][2])
            if coords == None:
                continue
            if coords not in used_coords_for_lviv:
                used_coords_for_lviv[coords] = [data_of_lviv[i][0]]
            else:
                used_coords_for_lviv[coords].append(data_of_lviv[i][0])
        except TypeError:
            continue
    return used_coords_for_lviv


def parser():
    """Parse arguments

    Returns:
        parser: Namespace of arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "year", type=int, help='In what year you want to see films on the map in format ####   (2004 for example)')
    parser.add_argument("latitude", type=float,
                        help='latitude of the point from wich you want to start in format ##.####...')
    parser.add_argument("longitude", type=float,
                        help='longitude of the point from wich you want to start in format ##.####...')
    parser.add_argument("path_to_dataset", type=str,
                        help='Path to the file with data of films')
    return parser.parse_args()


def main():
    args = parser()

    data = convert_info(info_get(args.path_to_dataset))
    choosed_places = choose_places(data, args.year)
    data_of_year = choosed_places[0]
    data_of_lviv = choosed_places[1]

    # print(len(data_of_year))
    # print(len(data_of_lviv))

    used_coords = create_coords_dictionary_with(data_of_year)

    map = folium.Map(location=[args.latitude, args.longitude])
    markers_of_year = folium.FeatureGroup(name=f'Films made in {args.year}')

    nearest_10 = choose_ten_nearest(used_coords, args.latitude, args.longitude)

    for i in nearest_10:
        markers_of_year.add_child(folium.Marker(
            location=[i[0], i[1]], popup=str(used_coords[i])[1:-1], icon=folium.Icon()))

    lviv_films = folium.FeatureGroup(name="films shot in Lviv")
    used_coords_for_lviv = lviv_places(data_of_lviv)

    for i in used_coords_for_lviv:
        lviv_films.add_child(folium.Marker(location=[i[0], i[1]], popup=str(
            used_coords_for_lviv[i])[1:-1], icon=folium.Icon()))

    map.add_child(markers_of_year)
    map.add_child(lviv_films)
    map.add_child(folium.LayerControl())
    map.save('Map.html')


main()
