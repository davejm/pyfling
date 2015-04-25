"""Send a picture Fling"""
import pyfling

f = pyfling.Fling("XXXXXXXX")

img_url = f.upload("test.jpg")
#img_url = "http://lorempixel.com/640/1138"

result = f.send_image(img_url)
print(result)