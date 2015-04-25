"""
Sends a text Fling and prints the receivers' formatted addresses.
Note that in the new Fling API (v2) the location latitude and longitudes
have been greatly reduced in accuracy (to 1 d.p.). Maybe they saw this example?
"""

import pyfling

f = pyfling.Fling("XXXXXXXX")

receivers = f.send_text("Hey")['receivers']
for receiver in receivers:
    lat = receiver['lat']
    lng = receiver['lng']
    address = f.geocode(lat, lng)
    if address == "":
        print ("No address")
    else:
        # The encoding trickery here is to stop errors in my console which can only print
        # ascii text :/ Feel free to use the raw string if you can support some of the weird
        # unicode characters!
        print(str(address[0]['formatted_address'].encode("ascii", "replace"), encoding="utf-8"))
        #print(address[0]['formatted_address'])
    print("")