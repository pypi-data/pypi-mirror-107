import requests
import json
from urllib.parse import urljoin
from dataclasses import dataclass
from typing import List
from .models import Miner, Transaction, Balance, Statistics
from .filters import Filter, Sort, Limit


#
# This is the main class used for connecting to the Duino Coin
# REST API.
#
@dataclass(frozen=True, eq=False, order=False)
class DUCO:
    server_address: str = 'https://server.duinocoin.com/'
    miners_endpoint: str = server_address + 'miners'
    balances_endpoint: str = server_address + 'balances'
    transactions_endpoint: str = server_address + 'transactions'
    statistics_endpoint: str = server_address + 'statistics'
    user_endpoint: str = server_address + 'users'

    #
    # An internal function used to make a `GET` request to `url`.
    #
    # Arguments:
    # - `url`: The endpoint to call
    # - `params`: The parameters that make up the query string. (Optional)
    #
    # Returns: 
    # - a JSON representation of the response from the server.
    # 
    def __get_request(self, url: str, params: dict = None):
        response = requests.get(url, params=params)
        
        json_response = json.loads(response.text)

        if not json_response.get('success', False):
            raise Exception(json_response.get('message', 'An error occured'))

        result = json_response.get('result', None)

        if not result:
            raise Exception('No result returned')

        return result

    #
    # An internal function used to create a single set of parameters from multiple filters,
    # sort, or limit objects
    #
    # Arguments:
    # - `filters`: a list of `Filter` objects. (Optional)
    # - `sort`: a single `Sort` object. (Optional)
    # - `limit`: a single `Limit` object. (Optional)
    #
    # Returns:
    # - a flattened dict object containing all params for a query string
    #
    def __compile_query(self, filters: List[Filter]=None, sort: Sort=None, limit: Limit=None):
        params = {}

        if filters:
            for f in filters:
                params.update(f.compiled())

        if sort:
            params.update(sort.compiled())

        if limit:
            params.update(limit.compiled())

        return params

    #
    # The function used to retrieve all miners from the REST API.
    #
    # Arguments:
    # - `filters`: a list of `Filter` objects used to narrow down results. (Optional)
    #
    # Returns:
    # - a list of `Miner` objects
    #
    def fetch_miners(self, 
        filters: List[Filter] = None):

        params = self.__compile_query(filters=filters)
        
        result = self.__get_request(self.miners_endpoint, params=params)

        return [Miner(**j) for j in result]

    #
    # The function used to retrieve a single miner by it's `threadid` from the REST API.
    #
    # Arguments:
    # - `threadid`: the thread id of the miner you wish to get
    #
    # Returns:
    # - a `Miner` object
    #
    def fetch_miner(self,
        threadid: str):

        if not threadid:
            raise Exception('\'threadid\' is required')

        result = self.__get_request(self.miners_endpoint + '/' + threadid)

        return Miner(**result)

    #
    # The function used to retrieve all transactions from the REST API.
    #
    # Arguments:
    # - `filters`: a list of `Filter` objects used to narrow down results. (Optional)
    # - `sort`: a single `Sort` object detailing how the response should be sorted. (Optional)
    # - `limit`: a single `Limit` object detailing how many objects should be in the response. (Optional)
    #
    # Returns:
    # - a list of `Transaction` objects
    #
    def fetch_transactions(self,
        filters: List[Filter] = None,
        sort: Sort = None,
        limit: Limit = None):

        params = self.__compile_query(filters=filters, sort=sort, limit=limit)

        result = self.__get_request(self.transactions_endpoint, params=params)

        return [Transaction(**t) for t in result]

    #
    # The function used to retrieve a single transaction by it's `hash` from the REST API.
    #
    # Arguments:
    # - `hash_id`: the hash of the transaction you wish to get
    #
    # Returns:
    # - a `Transaction` object
    #
    def fetch_transaction(self, 
        hash_id: str):

        if not hash_id:
            raise Exception('\'hash_id\' is required')

        result = self.__get_request(self.transactions_endpoint + '/' + hash_id)

        return Transaction(**result)

    #
    # The function used to retrieve all balances from the REST API.
    #
    # Arguments:
    # - `filters`: a list of `Filter` objects used to narrow down results. (Optional)
    # - `sort`: a single `Sort` object detailing how the response should be sorted. (Optional)
    # - `limit`: a single `Limit` object detailing how many objects should be in the response. (Optional)
    #
    # Returns:
    # - a list of `Balance` objects
    #
    def fetch_balances(self, 
        filters: List[Filter] = None, 
        sort: Sort = None, 
        limit: Limit = None):
        
        params = self.__compile_query(filters=filters, sort=sort, limit=limit)

        result = self.__get_request(self.balances_endpoint, params=params)

        return [Balance(**b) for b in result]

    #
    # The function used to retrieve a single balance for a user from the REST API.
    #
    # Arguments:
    # - `username`: the username of the balance you wish to get
    #
    # Returns:
    # - a `Balance` object
    #
    def fetch_balance(self,
        username: str):

        if not username:
            raise Exception('\'username\' is required')

        result = self.__get_request(self.balances_endpoint + '/' + username)

        return Balance(**result)

    #
    # The function used to retrieve the statistics from the REST API.
    #
    # Returns:
    # - a `Statistics` object
    #
    def fetch_statistics(self):
        response = requests.get(self.statistics_endpoint)

        result = json.loads(response.text)

        return Statistics(**result)

    #
    # The function used to retrieve all objects related to a user from the REST API.
    #
    # Arguments:
    # - `username`: the username of the user you want to get
    #
    # Returns: 
    # - a `User` object
