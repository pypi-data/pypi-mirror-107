import numpy as np
from urllib.parse import urlencode
import pycurl
import json
import certifi

def haversine(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    """
    Calculate the great circle distance between two points on the 
    earth (specified in decimal degrees), returns the distance in
    meters.
    All arguments must be of equal length.
    :param lon1: longitude of first place
    :param lat1: latitude of first place
    :param lon2: longitude of second place
    :param lat2: latitude of second place
    :return: distance in meters between the two sets of coordinates
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2,lat2])
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    km = 6367 * c
    return km * 1000

def logmlmodel(apikey,mlMonitorId) -> object:

    apikey = "probyto-ai-apikey: " + apikey
    print(apikey)

    curl = pycurl.Curl()
    curl.setopt(pycurl.CAINFO, certifi.where())
    curl.setopt(curl.URL, 'https://aiapi-test.probyto.com/api/v1/client/mlMonitorFeedback')
    curl.setopt(pycurl.HTTPHEADER, ['Accept: application/json',
                                    'Content-Type: application/json',
                                    apikey])
    curl.setopt(pycurl.POST, 1)
    ml_monitor_body = {
        'apiPath': 'https://functions.probyto.com/insurance-prediction',
        'ipAddress': '127.0.0.1',
        'inParams': 'test_params',
        'predictedValue': 'test_predicted_value',
        'feedbackValue': None,
        'apiResponseStatusCode': 200,
        'apiResponseMessage': 'test_apiresponse',
        'mlMonitorId': mlMonitorId
    }
    body_as_json_string = json.dumps(ml_monitor_body) # dict to json
    
    # postfields = urlencode(ml_monitor_body)
    curl.setopt(curl.POSTFIELDS, body_as_json_string)
    # If you want to set a total timeout, say, 3 seconds
    curl.setopt(pycurl.TIMEOUT_MS, 3000)
    
    curl.perform()
    
    # you may want to check HTTP response code, e.g.
    status_code = curl.getinfo(pycurl.RESPONSE_CODE)
    if status_code != 201:
        print("Aww Snap :( Server returned HTTP status code {}".format(status_code))
    
    # don't forget to release connection when finished
    curl.close()

    return status_code