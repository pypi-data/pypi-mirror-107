[![pypi](https://img.shields.io/pypi/v/globconf.svg)](https://pypi.python.org/pypi/python-flex-cache)
[![versions](https://img.shields.io/pypi/pyversions/globconf.svg)](https://github.com/steffenschumacher/python-flex-cache)
[![license](https://img.shields.io/github/license/steffenschumacher/globconf.svg)](https://github.com/steffenschumacher/python-flex-cache/blob/master/LICENSE)

# globconf

* Creates a global configparser object, regardless of the project and module in need of it
* A docker container can be used to host protected config files, consumable by the parser object
* verify_required_options merges default options with the configparser ones, and optionally ENV 
  options while validating required options have been set either way.


## Getting Started
In a project using globconf:
```python
from globconf import config, verify_required_options, read_config, fetch_config
# when starting the app, the config can be loaded from a specific path:
read_config(path='flaf.ini', force=True)  # reloads config, even if it already is loaded

# or from the globconfd container - caching supported as convenience for offline devs:
fetch_config('http://127.0.0.1:5000/cfg.ini', 'user', 'pass', cache_timeout=86400, force=True)

# if config is not explicitly loaded, config.ini is read from current folder (if there).

# verify_required_options checks presence of options, yielding a dict with the merged options 
# for the section
DEFAULTS = {'required': None, 'optional_a': 1234}
cfg = verify_required_options('Some section', ['required', 'options', 'for', 'the', 'section'])
 
# beyond this, its still basic ConfigParser as you know it..
```

In modules:
```python
from globconf import verify_required_options
class module(object):
    def __init__(self):
        sec = 'service now'
        self.cfg = verify_required_options(sec, ['host', 'user', 'pwd'])
        if not self.cfg.getboolean('verify_ssl', fallback=True):
            import urllib3
            urllib3.disable_warnings(InsecureRequestWarning)
```

And your module is happy as long as someone has initialised the needed section in the global config.

##globconfd via docker
```
docker run -it -v ./users.conf:env_users.conf -v ./cfgs:/configs -p 5000:5000 ssch/globconfd:latest -d
```

### Prerequisites

configparser, diskcache, requests


### Building
Build:
```
sudo python setup.py sdist bdist_wheel
twine upload dist/*
```



## Authors

* **Steffen Schumacher** - *Initial work* - [steffenschumacher](https://github.com/steffenschumacher)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
Nahh..
