import folium
import math
from geopy.geocoders import Nominatim
from hypersin import my_hyper    #Функція гаверсинуса написана в додатковому модулі
import random
import haversine


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
    geolocator = Nominatim(user_agent="main.py")
    location = geolocator.geocode(place)
    try:
        try:
            try:
                try:
                    return (location.latitude, location.longitude)
                except AttributeError:
                    city=place.split(',')[0]
                    location = geolocator.geocode(city)
                    return (location.latitude, location.longitude)
            except AttributeError:
                try: 
                    higher=place.split(',')[1]
                    location = geolocator.geocode(higher)
                    return (location.latitude, location.longitude)
                except IndexError:
                    higher=place.split(',')[-1]
                    location = geolocator.geocode(higher)
                    return (location.latitude, location.longitude)
        except AttributeError:
            higher=place.split(',')[-1]
            location = geolocator.geocode(higher)
            return (location.latitude, location.longitude)
    except AttributeError:
        return None

def choose_places(data, year):
    data_of_year=[]
    data_of_lviv_films=[]
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
        coords_of_place=get_coords(i[2])
        if coords_of_place!=None:
            if haversine.haversine((49.841952, 24.0315921), coords_of_place) > 300:
                data_of_lviv_films.remove(i)
    return (data_of_year, data_of_lviv_films)


def main():
    location1=float(input('Корди 1: '))
    location2=float(input('Корди 2: '))
    year=int(input('Рік: '))
    path_to_file='locations.list'
    data=convert_info(info_get(path_to_file))
    choosed_places=choose_places(data, year)
    data_of_year=choosed_places[0]
    data_of_lviv=choosed_places[1]
    print(len(data_of_year))
    print(len(data_of_lviv))


    used_coords={}
    for i in range(len(data_of_year)):
        try:
            coords=get_coords(data_of_year[i][2])
            if coords==None:
                continue
            if coords not in used_coords:
                used_coords[coords]=[data_of_year[i][0]]
            else:
                used_coords[coords].append(data_of_year[i][0])
            
        except TypeError:
            continue
    map=folium.Map(location=[location1, location2])
    markers_of_year=folium.FeatureGroup(name=f'Films made in {year}')

    distances=[]    
    coords_for_distances=[]
    nearest_10=[]
    for i in used_coords:
        distances.append(haversine.haversine((location1, location2), i))
        coords_for_distances.append(i)
    while len(nearest_10)!=10:
        min_distance_index=distances.index(min(distances))
        nearest_10.append(coords_for_distances[min_distance_index])
        distances[min_distance_index]+=9999999999999

    for i in nearest_10:
        markers_of_year.add_child(folium.Marker(location=[i[0], i[1]], popup=str(used_coords[i])[1:-1], icon=folium.Icon()))

    used_coords_for_lviv={}
    lviv_films=folium.FeatureGroup(name="films shot in Lviv")
    for i in range(len(data_of_lviv)):
        try:
            coords=get_coords(data_of_lviv[i][2])
            if coords==None:
                continue
            if coords not in used_coords_for_lviv:
                used_coords_for_lviv[coords]=[data_of_lviv[i][0]]
            else:
                used_coords_for_lviv[coords].append(data_of_lviv[i][0])
        except TypeError:
            continue
    for i in used_coords_for_lviv:
        lviv_films.add_child(folium.Marker(location=[i[0], i[1]], popup=str(used_coords_for_lviv[i])[1:-1], icon=folium.Icon()))
    map.add_child(markers_of_year)
    map.add_child(lviv_films)
    map.add_child(folium.LayerControl())
    map.save('map1.html')
    
    




main()












# # if __name__ == '__main__':
# #     point=(49.83826, 24.02324)
# #     print(point)
# #     data=info_get('locations.list')
# #     films=convert_info(data)
# import doctest
# print(doctest.testmod())