pyfling
=======

A python library for the Unii Fling API

Installation
------------

Currently there is no formal installation procedure so just copy pyfling.py
to whatever directory you wish to use it in.

Requirements
------------

You must have the python library 'requests' which can easily be downloaded using PIP

Example API usage
-----------------

```python

import pyfling

# Replace XXXXXXXX with your authentication bearer token
f = pyfling.Fling("XXXXXXXX")

img_url = f.upload("test.jpg")

result = f.send_image(img_url)
```

Authentication
-----------------

You must have your unique authentication 'bearer' to use the library.
This can be found by using a debugging proxy such as Fiddler or Wireshark,
and looking at the headers of requests from the Fling app.