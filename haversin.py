import math
def my_haver(point1, point2):
#rad - Радіус Землі
    rad = 6372795

    #Координати двох точок в радіанах
    lat1 = point1[0]*math.pi/180
    long1 = point1[1]*math.pi/180

    lat2 = point2[0]*math.pi/180
    long2 = point2[1]*math.pi/180

    #косинуси і синуси широт і довгот
    cos_lat1 = math.cos(lat1)
    cos_lat2 = math.cos(lat2)
    sin_lat1 = math.sin(lat1)
    sin_lat2 = math.sin(lat2)
    delta = long2 - long1
    cos_delta = math.cos(delta)
    sin_delta = math.sin(delta)

    #Довжина дуги великого кола
    y = math.sqrt(math.pow(cos_lat2*sin_delta,2)+math.pow(cos_lat1*sin_lat2-sin_lat1*cos_lat2*cos_delta,2))
    x = sin_lat1*sin_lat2+cos_lat1*cos_lat2*cos_delta
    ad = math.atan2(y,x)
    dist = ad*rad

    #Початковий азимут
    x = (cos_lat1*sin_lat2) - (sin_lat1*cos_lat2*cos_delta)
    y = sin_delta*cos_lat2
    z = math.degrees(math.atan(-y/x))

    if (x < 0):
        z = z+180.

    z2 = (z+180.) % 360. - 180.
    z2 = - math.radians(z2)
    anglerad2 = z2 - ((2*math.pi)*math.floor((z2/(2*math.pi))) )
    angledeg = (anglerad2*180.)/math.pi

    return int('%.0f' % dist)
