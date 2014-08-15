pyfling
=======

A python library for the Unii Fling API

Installation
------------

Currently there is no formal installation procedure so just copy pyfling.py
to whatever directory you wish to use it in.

Example API usage
-----------------

```python

import pyfling

f = pyfling.Fling("XXX") #Replace XXX with your authentication bearer

recipients = f.get_receivers(50)

img_url = f.upload("test.jpg")
result = f.send_image(recipients, img_url)
```
