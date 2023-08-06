from os import environ
from configparser import ConfigParser, NoOptionError, NoSectionError, SectionProxy

"""
global/singleton config object to be uses across modules
"""
config = None


def _parse_option(v):
    if v.lower() in 'true yes on':
        return True
    elif v.lower() in 'false, no off':
        return False
    elif v.isnumeric():
        return int(v)
    elif v.replace('.', '').isnumeric():
        return float(v)
    else:
        return v


def verify_required_options(section, option_keys, defaults={}, parse_env=False):
    """
    Verifies that section exists, and that it has option_keys defined
    :param str section: Section in the config
    :param list[str] option_keys: list of required options
    :param dict[str, str] defaults: dict of default option values
    :param bool parse_env: parse environment variables (trumps file options)
    :rtype: dict[str, str|int|float|bool]
    :raises: NoSectionError, NoOptionError
    """
    merged_config = defaults.copy()
    file_config = read_config()
    if section in file_config:
        for k, v in file_config[section].items():
            merged_config[k] = _parse_option(v)
    if parse_env:
        up_sec = section.upper().replace(' ', '_')
        for k, v in merged_config.items():
            candidate = environ.get('{}_{}'.format(up_sec, k.upper()))
            if candidate is not None:
                merged_config[k] = _parse_option(candidate)
    missing_requireds = [k for k in option_keys if k not in merged_config or merged_config[k] is None]
    if missing_requireds:
        if section not in file_config:
            raise NoSectionError(section)
        else:
            raise NoOptionError(', '.join(missing_requireds), section)
    return merged_config


def read_config(path='config.ini', force=False):
    """
    :param str path:
    :param bool force:
    :rtype: ConfigParser
    """
    global config
    if not config or force:
        config = ConfigParser()
        config.read(path)
    return config


def fetch_config(url, user, password, cache_timeout=86400, force=False):
    """
    :param str url:
    :param str user:
    :param str password:
    :param int cache_timeout: timeout seconds
    :param bool force: force config reload
    :rtype: ConfigParser
    """
    global config
    if not config or force:
        import os
        import hashlib
        from diskcache import Cache
        from requests import get
        from requests.auth import HTTPBasicAuth
        url_hash = hashlib.md5('{}{}{}'.format(url, user, password).encode()).hexdigest()
        cfg_path = os.environ.get('GLOBCONF_CACHE_PATH', 'tmp')
        config = ConfigParser()

        with Cache(cfg_path, timeout=cache_timeout) as c:
            cfg_string, expire = c.get(url_hash, expire_time=True)
            if cfg_string is None:
                r = get(url, auth=HTTPBasicAuth(user, password), timeout=5)
                r.raise_for_status()
                cfg_string = r.text
                c.add(url_hash, cfg_string)
        config.read_string(cfg_string)
    return config
