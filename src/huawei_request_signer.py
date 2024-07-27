import datetime
import hashlib
import hmac
from urllib.parse import urlparse

class HuaweiRequestSigner(object):
    '''
    LINK: https://support.huaweicloud.com/eu/devg-apisign/devg-apisign.pdf
    '''
    def __init__(self) -> None:
        '''
        '''
        self.__request_time = datetime.datetime.now(datetime.UTC).strftime('%Y%m%dT%H%M%SZ')

    @property
    def request_time(self) -> str:
        '''
        '''
        return self.__request_time

    def __get_standard_header(self, request_url: str, method: str, payload: str) -> str:
        '''
        '''
        request_parts = list()
        uri = urlparse(request_url)
        #host = uri.hostname
        #path = uri.path
        #query = uri.query

        # step 1 (method)
        request_parts.append(method)

        # step 2 (path)
        uri_path = uri.path
        if not uri_path.endswith('/'):
            uri_path += '/'
        request_parts.append(uri_path)

        # step 3 (query string)
        request_parts.append(uri.query)

        # step 4
        ## All letters in a header are converted to lowercase letters, and all spaces before and after the header are deleted.
        ## All headers are sorted in alphabetically ascending order.
        headers = {
            'host' : uri.hostname,
            'x-sdk-date' : self.__request_time 
        }
        headers_list = [f"{key.lower()}:{value}" for key, value in headers.items()]
        headers_list.sort()
        canonical_headers = '\n'.join(headers_list)
        request_parts.append(canonical_headers)

        # step 5 (Signed Headers)
        request_parts.append('')
        signed_headers = 'host;x-sdk-date'
        request_parts.append(signed_headers)

        # step 6 - Request Payload
        ## (HexEncode(Hash(RequestPayload))
        request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        request_parts.append(request_payload)

        return '\n'.join(request_parts)
    
    def __get_signed_string(self, standard_request: str) -> str:
        '''
        StringToSign = 
            Algorithm + \\n +
            RequestDateTime + \\n +
            HashedCanonicalRequest
        '''

        algorithm = 'SDK-HMAC-SHA256'
        request_payload = hashlib.sha256(standard_request.encode("utf-8")).hexdigest()
        string_to_sign = f'{algorithm}\n{self.__request_time}\n{request_payload}'

        return string_to_sign

    def get_signature(self, request_url: str, secret_key: str, method: str = 'GET', payload: str = '') -> str:
        '''
        '''
        standard_request = self.__get_standard_header(request_url, method, payload)
        string_to_sign = self.__get_signed_string(standard_request)
        signature = hmac.new(secret_key.encode('utf-8'), string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
        
        return signature
    
    def get_authorization(self, access_key: str, signature: str) -> str:
        '''
        '''
        authorization = f'SDK-HMAC-SHA256 Access={access_key}, SignedHeaders=host;x-sdk-date, Signature={signature}'

        return authorization
    
    def get_headers(self, request_url: str, access_key: str, secret_key: str,\
                    method: str = 'GET', payload: str = '') -> dict:
        '''
        '''
        signature = self.get_signature(request_url, secret_key, method, payload)
        authorization = self.get_authorization(access_key, signature)

        headers = {
            'Content-Type' : 'application/json',
            'x-sdk-date' : self.__request_time,
            'Authorization': authorization
        }
        
        return headers