"""
@author: David Moodie
"""

import json
import os

import requests

flingAPI = "https://api.superfling.com/api/v2/"
amazonAPI = "http://unii-fling.s3.amazonaws.com/"

class Fling(object):
    
    def __init__(self, bearer):
        """Requires authentication bearer to instantiate"""
        #self.bearer = ""
        self.bearer = bearer

    def _request(self, endpoint="", data=None, req_type="post"):
        global flingAPI
        
        if data is None:
            data = {}
        
        user_agent = 'fling/1.6.2 (iPhone; iOS 8.3; Scale/2.00)'
        
        bearer = 'Bearer ' + self.bearer
        headers = {'User-Agent' : user_agent, 'Authorization' : bearer}
        url = flingAPI
        
        if req_type == "post":
            headers['Content-Type'] = 'application/json'
            r = requests.post(url + endpoint, data=data, headers=headers)
        else:
            r = requests.get(url + endpoint, params=data, headers=headers)
        #if raise_for_status:
        #    r.raise_for_status()
        return r
        
    def _request_amazon(self, url, data=None, files=None):
        #global amazonAPI
        if data is None:
            data = {}
        
        user_agent = 'fling/1.6.2 (iPhone; iOS 8.3; Scale/2.00)'
        headers = {'User-Agent' : user_agent}
        #url = amazonAPI
        r = requests.post(url, data=data, files=files, headers=headers)
        return r
    
    def _init_fling_on_server(self):
        """Create slot on fling to store fling data"""
                    
        media_type = "image" #Temporary
        if media_type == "image":
            data = {"uploads": {"extension":".jpg"}}
            data = json.dumps(data)
            r = self._request("uploads", data=data)
            result = r.json()
            uploads = result['uploads']
            return uploads
            
    def _upload_to_amazon(self, path, data):
        """Actually upload media to Amazon S3 so that fling can be downloaded/viewied"""
        #print(data)        
        if not os.path.exists(path):
            raise ValueError('No such file: {0}'.format(path))

        with open(path, 'rb') as f:
            file = f.read()
    
        #Note: Must use tuple value for file data otherwise erroneous 'filename' field is put in request
        files = {'file' : (None, file)}
        
        amazonS3RequestURL = data['url']
        
        if data['static_fields']['content-type'] == None:
            data['static_fields']['content-type'] = ""
        submitdata = data['static_fields']
        
        r = self._request_amazon(amazonS3RequestURL, data=submitdata, files=files)
        
        return r
        
    def get_flings(self, limit=50, page=1):      
        data = {"limit" : limit, "page" : page}
        r = self._request("flings", data=data, req_type="get")
        result = r.json()
        result = result['flings']
        return result
    
    def get_me(self):
        r = self._request("users/me", req_type="get")
        result = r.json()
        result = result['users']
        return result
        
    def upload(self, path):
        """Init a new picture with fling API and
        upload the picture from your harddrive to fling amazon S3 servers"""
        datafromfling = self._init_fling_on_server()
        #result = self._upload_to_amazon(path, datafromfling)
        img_url = datafromfling['final_location']
        return img_url
        
    def send_text(self, text):
        send_type = "Text"
        if len(text) > 140:
            print("Text must be <= 140 chars")
            return "Text must be <= 140 chars"
        else:
            media = {"type" : send_type, "text" : text, "y" : 0}
            data = {"flings": {"media" : media}}
            data=json.dumps(data)
            #print(data)
            r = self._request("flings", data=data)
            result = r.json()
            return result


    def send_image(self, img_url):
        send_type = "Image"        
        media = {"type" : send_type, "url" : img_url, "y" : 0}
        data = {"flings": {"media" : media}}
        data=json.dumps(data)
        #print(data)
        r = self._request("flings", data=data)
        result = r.json()
        return result

    def geocode(self, lat, lng):
        geocode = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng))
        address = geocode.json()
        if len(address['results']) == 0:
            return ""
        address = address['results']
        return address

