"""Gets some potential Fling receivers and prints their formatted address"""

import pyfling

f = pyfling.Fling("XXX")

receivers = f.get_receivers(50)
for receiver in receivers:
    user_id = receiver['id']
    lat = receiver['lat']
    lng = receiver['lng']
    address = f.geocode(lat, lng)
    print("User ID: " + str(user_id))
    print("Address: " + address)
    print("")