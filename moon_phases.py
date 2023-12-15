import ephem
from geopy import Photon
# import elevation
import requests
import matplotlib.pyplot as plt
def moon_phase_and_position(observer_lat,  observer_long, observer_elev, date_str):
    observer=ephem.Observer()
    observer.lat=str(observer_lat)
    observer.lon=str(observer_long)
    observer.elev=observer_elev
    # Calculating moon phases
    moon=ephem.Moon()
    moon.compute(observer)
    phase=moon.phase

    # Calculates moon's position (Ra, dec)
    constellation_name = ephem.constellation(moon)[1]
    constellation_abbr = ephem.constellation(moon)[0]
    print("\n***********************************************************************")
    print(f"Constellation: {constellation_name}; Abbr.: {constellation_abbr}")
    ra= moon.ra
    dec= moon.dec

    return phase, ra, dec
def user_inputs_date():
    # user inputs
    try:
        year    =int(input("Year (YYYY): "))
        month   =int(input("Month (MM): "))
        day     =int(input("Day (DD): "))
        time    =input("Enter time (HH:mm:ss): ")
        date_str=str(f'{year}:{month}:{day} {time}')
        return date_str
    except:
        print("Error!\nKindly enter integer values in a 24-hour format")
# print(date_str)
def observer_location():
    # User location --> lat/long
    try:
        loc         =input("Enter location: ")
        location    =f'{loc}'
        locator     =Photon(user_agent='myGeocoder')
        location    =locator.geocode(location)
        observer_lat,observer_long    =location.latitude, location.longitude

        return observer_lat, observer_long
    except AttributeError:
        print("Location not found. Please enter a valid location.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
# def get_elevation(location):
#     # To get observer elevation
#     elevation_data=elevation.batch(location)
#     return elevation_data['elevation']
def get_elevation(lat, long):
    url         = f'https://api.open-elevation.com/api/v1/lookup?locations={lat},{long}'
    response    = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            elevation = data['results'][0]['elevation']
            return elevation
        else:
            print("Error: Unable to retrieve elevation. Response structure is unexpected.")
            return None
    else:
        print(f"Error: Unable to retrieve elevation. Status code: {response.status_code}")
        return None

date_str                    =user_inputs_date()
observer_lat, observer_long =observer_location()
observer_location           =[(observer_lat,observer_long)]
elevation                   =get_elevation(observer_lat, observer_long)

# if elevation is None:
#     print("Elevation data not available")

observer_elev=elevation
moon_phase, moon_ra, moon_dec = moon_phase_and_position(observer_lat, observer_long, observer_elev, date_str)

def moon_phase_display(phase):
    if phase<45:
        return "New Moon"
    elif phase<135:
        return "First Quarter Waxing Crescent"
    elif phase<225:
        return "Full Moon Waxing Gibbous"
    elif phase<315:
        return"Last Quarter Waning Gibbous"
    else:
        return "New Moon Waning Crescent"
    
print(f"Longitude: {observer_long}\nLatitude: {observer_lat}\nElevation: {observer_elev}\n")
print(f"Moon phase: {moon_phase} degrees, {moon_phase_display(moon_phase)}")
print(f"Moon Position (RA): {moon_ra}")
print(f"Moon Position (Dec): {moon_dec}")
print("\n***********************************************************************")
