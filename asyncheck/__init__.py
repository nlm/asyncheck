"""
Module for storing and retrieving Nagios Results in redis
"""
from redis.sentinel import Sentinel
import pickle

OK = 0
WARNING = 1
CRITICAL = 2
UNKNOWN = 3

class Result(object):
    """ class represting a nagios result """

    def __init__(self, code, message=None, perfdata=None, extdata=None):
        self.code = code
        self.message = message
        self.perfdata = perfdata
        self.extdata = extdata

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, self.__dict__)


class RedisStorageEngine(object):
    """ class for interacting with redis """

    def __init__(self, sentinels, namespace, svcname=None, expire=None):
        """
        initializes the object

        parameters:
            sentinels: a list of (server, port) tuples
            namespace: a namespace to store keys under
            svcname: redis service name (default: mymaster)
            expire: keys expiration time (default: 600)
        """
        self._sentinel = Sentinel(sentinels=sentinels, socket_timeout=0.1)
        self._servicename = svcname if svcname is not None else 'mymaster'
        self._namespace = namespace
        self._expire = expire if expire is not None else 600

    def get(self, key):
        """
        get a result from redis

        parameters:
            key: the key to retrieve data from

        returns:
            a result object
        """
        data = self._sentinel.master_for(self._servicename).get(self._namespace + '.' + key)
        if data is not None:
            return pickle.loads(data)
        return None

    def set(self, key, obj):
        """
        get a result from redis

        parameters:
            key: the key to store data to
            obj: the result object to store

        returns:
            nothing
        """
        return self._sentinel.master_for(self._servicename).set(self._namespace + '.' + key, pickle.dumps(obj), ex=self._expire)

    def delete(self, key):
        """
        delete a result from redis

        parameters:
            key: the key to store data to

        returns:
            nothing
        """
        return self._sentinel.master_for(self._servicename).delete(self._namespace + '.' + key)

    def persist(self, key):
        """
        persist a key

        parameters:
            key: the key to store data to

        returns:
            nothing
        """
        return self._sentinel.master_for(self._servicename).persist(self._namespace + '.' + key)
