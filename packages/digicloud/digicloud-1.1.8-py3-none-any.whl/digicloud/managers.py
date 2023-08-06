"""
    Managers definition.
"""
import os
import pickle
import sys
from pathlib import Path
from collections import ChainMap

from requests import Session as Sess


class ConfigManager():
    """Configuration manager for all configs."""
    FILE_NAME = 'config'
    DEFAULTS = {
        'BASE_URL': os.environ.get('API_BASE_URL', "https://api.digicloud.ir"),
    }

    def __init__(self, app_logger):
        self._log = app_logger
        self._path = self._get_config_path()
        self._states = dict()
        self._load()

    def __getitem__(self, item):
        try:
            return ChainMap(self.DEFAULTS, self._states).get(item)
        except KeyError:
            raise f'No "{item}" in configuration.'

    def __setitem__(self, item, value):
        self._states[item] = value

    def __delitem__(self, item):
        if item in self._states:
            del self._states[item]

    def __contains__(self, item):
        return item in self._states

    def __call__(self):
        return self._states

    def _get_config_path(self):
        """Create config file directory.

        Handles platform dependent path creation for ``FILE_NAME ``,
        and return full path to config file.
        """
        path = {
            'darwin': '$HOME/Library/Application Support/digicloud',
            'win': '%LOCALAPPDATA%/digicloud',
            'linux': '$HOME/.config/digicloud',
        }[sys.platform]

        path = os.path.expandvars(path)

        if not os.path.isdir(path):
            self._log.debug('No config director found.')
            try:
                os.mkdir(path, mode=0o755)
                self._log.debug(f'Config dir made in "{path}".')
            except IOError:
                raise "Create config path failes."

        full_path = os.path.join(path, self.FILE_NAME)
        Path(full_path).touch()

        return full_path

    def _load(self):
        with open(self._path, 'rb') as file_:
            if os.path.getsize(self._path) > 0:
                self._states = pickle.load(file_)

    def _dump(self):
        with open(self._path, 'wb') as file_:
            pickle.dump(self._states, file_, pickle.HIGHEST_PROTOCOL)

    def get(self, item, default=None):
        """return item from config or default."""
        return self.__getitem__(item) or default

    def save(self):
        """write configurations to file."""
        self._dump()


class Session(Sess):
    """Custom ``requests.Session`` object model."""

    def __init__(self, base_url, *args, **kwargs):
        self.base_url = base_url
        super(Session, self).__init__(*args, **kwargs)

    def resource(self, uri, method='GET', payload=None, params=None,
                 endpoint_version='/v1'):
        """Resource access helper."""
        url = f'{self.base_url}{endpoint_version}{uri}'
        response = self.request(method, url, params=params, json=payload)
        response.raise_for_status()
        return response.json()

    def get(self, uri, params=None):
        return self.resource(uri, params=params)

    def post(self, uri, payload):
        return self.resource(uri, 'POST', payload)

    def put(self, uri, payload):
        return self.resource(uri, 'PUT', payload)

    def patch(self, uri, payload):
        return self.resource(uri, 'PATCH', payload)

    def delete(self, uri, payload=None):
        return self.resource(uri, 'DELETE', payload)


class VersionChecker:
    def __init__(self, package_name):
        self.package_name = package_name

    def get_latest_version_number(self):
        uri = 'https://pypi.org/pypi/{}/json'.format(self.package_name)
        return Sess().get(uri).json()['info']['version']
