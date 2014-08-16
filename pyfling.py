"""
@author: David Moodie
"""

import json
import os
import datetime
import time

import requests

flingAPI = "http://api.superfling.com/api/v1/"
amazonAPI = "http://unii-fling.s3.amazonaws.com/"

class Fling(object):
    
    def __init__(self, bearer):
        """Requires authentication bearer to instantiate"""
        self.bearer = ""
        self.bearer = bearer


    def _request(self, endpoint="", data=None, files=None, req_type="post", amazon=False, overrideurl="", jsonpost=False):
        global flingAPI, amazonAPI
        
        if data is None:
            data = {}
        
        user_agent = 'fling/1.3 (iPhone; iOS 7.0.6; Scale/2.00)'
        
        if not amazon:
            bearer = 'Bearer ' + self.bearer
            headers = {'User-Agent' : user_agent, 'Authorization' : bearer}
            if jsonpost:
                headers = {'User-Agent' : user_agent, 'Authorization' : bearer, 'Content-Type': 'application/json'}
            url = flingAPI
        elif amazon:
            headers = {'User-Agent' : user_agent}
            #url = amazonAPI
            url = overrideurl
        
        if req_type == "post":
            r = requests.post(url + endpoint, data=data, files=files, headers=headers)
        else:
            r = requests.get(url + endpoint, params=data, headers=headers)
        #if raise_for_status:
        #    r.raise_for_status()
        
        return r
    
    def _init_fling_on_server(self):
        """Create slot on fling to store fling data"""
                    
        media_type = "image" #Temporary
        if media_type == "image":
            data = {"extension":".jpg"}
            r = self._request("uploads", data=data)
            result = r.json()
            return result
            
    def _upload_to_amazon(self, path, data):
        """Actually upload media to Amazon S3 so that fling can be downloaded/viewied"""
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
        
        r = self._request(amazon=True, data=submitdata, files=files, overrideurl=amazonS3RequestURL)
        
        return r
        
    def get_receivers(self, size=1):
        """Gets potential recipients of flings and returns user IDs and locations
        Note: Size param may be ignored in favour of 'number_of_flings' param in users/me
        """
        data = {"size" : size}        
        r = self._request("receivers", data=data, req_type="get")
        result = r.json()
        receivers = result['receivers']
        return receivers
        
    def get_flings(self, limit=50, time_updated="", page=1):
        """If you use the time_updated, you may not get any flings outputed. It seems safe to leave this blank"""        
        if time_updated == "now":
            #If the time_updated param is left empty, set to current ISO timestamp in UTC
            time_updated = datetime.datetime.utcfromtimestamp(time.time()).isoformat()
            time_updated = time_updated[0:-7] + "Z"
        data = {"limit" : limit, "page" : page, "q[receivers_updated_at_gt]" : time_updated}
        r = self._request("flings", data=data, req_type="get")
        result = r.json()
        result = result['flings']
        return result
    
    def get_me(self):
        r = self._request("users/me", req_type="get")
        result = r.json()
        result = result['user']
        return result
        
    def upload(self, path):
        datafromfling = self._init_fling_on_server()
        result = self._upload_to_amazon(path, datafromfling)
        #img_url = result.headers['Location']
        img_url = datafromfling['final_location']
        return img_url
        
    def send_text(self, recipients, text):
        """Expects a list of recipients"""
        send_type = "Text"
        if len(text) > 140:
            print("Text must be <= 140 chars")
            return "Text must be <= 140 chars"
        else:
            media = {"type" : send_type, "text" : text, "y" : 0}
            recipient_ids = recipients
            data = {"media" : media, "recipient_ids" : recipient_ids}
            data=json.dumps(data)
            #print(data)
            r = self._request("flings", data=data, jsonpost=True)
            result = r.json()
            return result



    def send_image(self, recipients, img_url):
        """Expects a list of recipients"""
        send_type = "Image"        
        media = {"type" : send_type, "url" : img_url, "y" : 0}
        recipient_ids = recipients
        data = {"media" : media, "recipient_ids" : recipient_ids}
        data=json.dumps(data)
        print(data)
        r = self._request("flings", data=data, jsonpost=True)
        result = r.json()
        return result

    def geocode(self, lat, lng):
        geocode = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(lng))
        address = geocode.json()
        address = address['results'][0]['formatted_address']
        return address

