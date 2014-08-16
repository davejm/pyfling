"""Sends a picture to a list of recipients"""
import pyfling

f = pyfling.Fling("XXX")

recipients = f.get_receivers(50)

img_url = f.upload("test.jpg")
result = f.send_image(recipients, img_url)