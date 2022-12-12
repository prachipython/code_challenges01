import requests
from requests import Session
import logging
from datetime import datetime
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from os import path

# Create and configure logger
logging.basicConfig(filename=f"reqclass{datetime.now()}.log",
                    format='%(asctime)s %(message)s',force=True,
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class RequestClass:
    def __init__(self, url,session,proxies):
        self.url = url
        self.session=session
        self.proxies=proxies

        # self.session=Session()

    def get_req(self,url,proxies=None):  #fuction for get request

        response = self.session.get(url,proxies=self.proxies)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e: # handled all errors
            logger.error(f'Request failed due to {e}')
            return "Error: " + str(e)
        logger.info('Request created successfully')
        return response

    def post_req(self,url,payload,proxies=None): #fuction for post request
        response = self.session.post(url,data=payload,proxies=self.proxies)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e: # handled all errors
            logger.error(f'Request failed due to {e}')
            return "Error: " + str(e)
        logger.info('Request created successfully')
        return response


    def get_payload(self,payload={}): #fuction to pass payload parameters to post request
        if type(payload) is dict:
            logger.info(f"Sending request for payload {payload}")
            return payload
        else:
            raise Exception(r"invalid parameter object {}, data type of object must be dict".format(payload))


    def download_img(self,img_url,img_name): #fuction to download image from website
        try:
            img=self.get_req(img_url)
        except Exception as err: # handled all errors
            logger.error(f"{err}")

        try:
            open(img_name,'wb').write(img.content)
        except Exception as err:
            logger.info(f"Image downloading failed due to: {err}")

    def download_file(self,file_url,file_name,file_extension): ##fuction to download file from website

        img=self.get_req(file_url)
        file_name=f"{file_name}.{file_extension}"
        try:
            open(file_name,'wb').write(img.content)
        except Exception as err: # handled all errors
            logger.info(f"File downloading failed due to: {err}")



# def retry_session(retries=2):
#     session = Session()
#     retries = Retry(total=retries,
#                 backoff_factor=0.1,
#                 status_forcelist=[500, 502, 503, 504],
#                 allowed_methods=frozenset(['GET', 'POST']))

#     session.mount('https://', HTTPAdapter(max_retries=retries))
#     session.mount('http://', HTTPAdapter(max_retries=retries))
#     return session
# session = retry_session()
session=Session()

def get_proxies(proxies=None): #fuction to use proxies
    if type(proxies) is dict:
            logger.info(f"Sending request for payload {proxies}")
    else:
        return None
    return proxies


proxies=get_proxies()
d = RequestClass("https://stackoverflow.com/questions/61855038/python-class-to-request-multiple-websites",session,proxies)
d.get_req('https://requests.readthedocs.io/en/latest/')
parameter=d.get_payload({'act': 'fillTehsil','district_code': '137'})
d.post_req('https://upbhulekh.gov.in/public/public_ror/action/public_action.jsp',parameter)
d.download_img('https://wbregistration.gov.in/(S(1cwzhuthpwvse5f5edaykcrd))/CImage.aspx','captcha.png')
