import requests
import hashlib
import json

from base64 import b64encode


def _get_basic_auth(client_id, password):
    base64_string = b64encode(str.encode(client_id + ":" + password)).decode("ascii")
    return base64_string


def generate_hash(hash_params):
    """
    Generates hash based on passed
          args
          ----------
          hash_params : string
              A concatenated string of parameters be hashed
    """
    return hashlib.sha512(str(hash_params.strip()).encode("utf-8")).hexdigest().strip()


def post_request(headers, json_data, url):
    """
    Posts request to given url with the given payload
          args
          ----------
          headers : dict
                Holds authentication data for the request
          json_data : json
                The request payload
          url : boolean
                The api url
    """
    return requests.request(method="POST", url=url, headers=headers, data=json_data)


class Collect(object):
    """
    Base class for paga Collect api library
    """

    _CONTENT_TYPE = "application/json"
    test_server = "https://beta-collect.paga.com"
    live_Server = "https://collect.paga.com"

    def __init__(self, client_id, password, api_key, is_test_env):
        """
              args
              ----------
              client_id : string
                  your public ID gotten from Paga
              password : string
                  your account password
              is_test_env : boolean
                  indicates whether application is in test or live mode
              """
        self.client_id = client_id
        self.password = password
        self.api_key = api_key
        self.is_test_env = is_test_env

    def build_header(self, hash_params):
        """
        Builds the HTTP request header 
              args
              ----------
              hash_params : string
                  A concatenated string of parameters be hashed
        """
        basic_auth = _get_basic_auth(self.client_id, self.password)

        hash_params = hash_params + self.api_key
        hash_data = generate_hash(hash_params)

        headers = {
            "Content-Type": self._CONTENT_TYPE,
            "Authorization": "Basic " + basic_auth,
            "hash": hash_data
        }

        return headers

    def get_url(self, is_test_env):
        """
        Gets the api url   
              args
              ----------
              is_test_env : boolean
                  A flag to determine if the requested url is test or live
        """
        if is_test_env:
            return self.test_server
        else:
            return self.live_Server

    def get_history(self, payload):
        """
        Calls Collect API to get the history of transactions done over time  
              args
              ----------
              payload : json
                  A request body for the history endpoint of the Collect API
        """
        endpoint = "/history"
        hash_params = ''

        if payload.get("referenceNumber"):
            hash_params += payload["referenceNumber"]

        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        json_data = json.dumps(payload)
        response = post_request(headers, json_data, server_url)
        return response.text

    def get_status(self, payload):
        """
        Calls Collect API to get the status of a transaction
              args
              ----------
              payload : json
                  A request body for the status endpoint of the Collect API
        """
        endpoint = "/status"
        hash_params = ''

        if payload.get("referenceNumber"):
            hash_params += payload["referenceNumber"]

        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        json_data = json.dumps(payload)
        response = post_request(headers, json_data, server_url)
        return response.text

    def get_banks(self, payload):
        """
        Calls Collect API to get all banks   
              args
              ----------
              payload : json
                  A request body for the getBanks endpoint of the Collect API
        """
        endpoint = "/banks"
        hash_params = payload["referenceNumber"]

        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        json_data = json.dumps(payload)
        response = post_request(headers, json_data, server_url)
        return response.text

    def payment_request(self, payload):
        """
        Calls Collect API to make a payment request   
              args
              ----------
              payload : json
                  A request body for the paymentRequest endpoint of the Collect API
        """
        endpoint = "/paymentRequest"
        hash_params = ''

        if payload.get("referenceNumber"):
            hash_params += payload["referenceNumber"]

        if payload.get("amount"):
            hash_params += payload["amount"]

        if payload.get("currency"):
            hash_params += payload["currency"]

        if payload.get("payer").get("phoneNumber"):
            hash_params += payload["payer"]["phoneNumber"]

        if payload.get("payer").get("email"):
            hash_params += payload["payer"]["email"]

        if payload.get("payee").get("accountNumber"):
            hash_params += payload["payee"]["accountNumber"]

        if payload.get("payee").get("phoneNumber"):
            hash_params += payload["payee"]["phoneNumber"]

        if payload.get("payee").get("bankId"):
            hash_params += payload["payee"]["bankId"]

        if payload.get("payee").get("bankAccountNumber"):
            hash_params += payload["payee"]["bankAccountNumber"]

        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        json_data = json.dumps(payload)
        response = post_request(headers, json_data, server_url)
        return response.text

    def register_persistent_payment_account(self, payload):
        """
        Calls Collect API to create persistent payment account
              args
              ----------
              payload : json
                  A request body for the register payment persistent account endpoint of the Collect API
        """
        endpoint = "/registerPersistentPaymentAccount"
        hash_params = ''

        if payload.get("referenceNumber"):
            hash_params += payload["referenceNumber"]

        if payload.get("accountReference"):
            hash_params += payload["accountReference"]

        if payload.get("financialIdentificationNumber"):
            hash_params += payload["financialIdentificationNumber"]

        if payload.get("creditBankId"):
            hash_params += payload["creditBankId"]

        if payload.get("creditBankAccount"):
            hash_params += payload["creditBankAccount"]

        if payload.get("callbackUrl"):
            hash_params += payload["callbackUrl"]

        url = self.get_url(self.is_test_env)
        server_url = url + endpoint

        headers = self.build_header(hash_params)

        json_data = json.dumps(payload)
        response = post_request(headers, json_data, server_url)
        return response.text
