# Films map
It is a project which create web html interactive map of films with information: which year and where they were shooted.
# Important
There is a problem with the 
~~~bash
from geopy.geocoders import Nominatim
~~~
geopy finds coords very slowly (1 place at 1 second)
I couldn't left my computer for the night to create csv file like
~~~bash
Name, year, coordinates
~~~
because of some troubles at home, and I didn't have enough time per day to do it.
As a result of geopy speed program works long if there are a lot of films in some years. (I've checked mostly for 1890 (It takes 1-2 minutes), and for 2020(It took 3 min))

## Description
In this module user give us inforamtion about which year he wants to see and location where he is right now (or location fro, where he want to see 10 nearest films). We take this info using argparse, and then read file with all films inforamtion and choose only those, which we need.(According to year) Then we look for coordinates where this film was shooted. After that, we check all of the distances between user's point and locations, using haversine,and choose only 10 nearest. And the latest step is to use folium and put needed coordinates to the map.

## Map description
On the map you can see 3 layers:

1. ![image](https://user-images.githubusercontent.com/91532556/153668343-57c9bef0-54bf-4ec2-870a-bb8c2bd45f62.png)
 It is the map without anything
  ![image](https://user-images.githubusercontent.com/91532556/153668277-d2c5bc90-0d13-49f6-a90c-e523090e5e47.png)


2.![image](https://user-images.githubusercontent.com/91532556/153668491-ac11b3f5-45fc-4e68-95db-3a8757582996.png)
It is the map with films which were shot in the given year(For example, here we have 1980 year, in NY were produced 3 films
![image](https://user-images.githubusercontent.com/91532556/153668573-7b036fcb-f253-4d85-a9bb-e30baca95324.png)

3.![image](https://user-images.githubusercontent.com/91532556/153668680-4bb081fa-3242-4a55-bf83-b5079e35bcec.png)
 It is the map with films which were shot in Lviv region.
 ![image](https://user-images.githubusercontent.com/91532556/153668829-dd151bef-66ff-498f-ad93-ce8e3cd7ddca.png)

Also in this window ![image](https://user-images.githubusercontent.com/91532556/153668867-4c81cd40-5879-4f10-9449-28dd99957f79.png)
we always have text "Films made in" and year which user give us.

## How to use the program
In your terminal you should write:
~~~bash
python path_to_module year latitude longitude path_to_file_with_data
~~~
for example:
~~~bash
python main.py 2017 49.83826 24.02324 locations.list 
~~~
And then just wait, your file will be created in your folder with name "Map.html"
Open it in your browser.

## Additional modules
Also I've created a module which is called "haversin.py"
It works. There is one function in this module which is called "my_haver"
to use it you should call it and put arguments:
~~~bash
print(haversin.my_haver(location1, location2))
~~~
And you will have the result which is distance between locations in meters.

## Example
You can see here the map for 2020 year where "my point" is Collegium UCU:
![image](https://user-images.githubusercontent.com/91532556/153671271-077f324b-76f8-429d-b07f-ba8c033c788d.png)
