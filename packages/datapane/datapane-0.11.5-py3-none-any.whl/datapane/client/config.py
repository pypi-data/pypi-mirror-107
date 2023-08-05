"""
Config subsystem
We use a module-level singleton pattern here, where top-level functions and globals
act like the state for a "Manager" class around the internal Config object
"""
import dataclasses as dc
import typing as t
import uuid
import webbrowser
from contextlib import suppress
from pathlib import Path
from typing import Optional

import click
import dacite
import yaml
from furl import furl

from datapane import _IN_PYTEST, log

from .utils import InvalidTokenError

APP_NAME = "datapane"
APP_DIR = Path(click.get_app_dir(APP_NAME))
APP_DIR.mkdir(parents=True, exist_ok=True)
DEFAULT_ENV = "default"
DEFAULT_SERVER = "https://datapane.com"
DEFAULT_TOKEN = "TOKEN_HERE"


# TODO - wrap into a singleton object that includes callable?
@dc.dataclass
class Config:
    """Global config read from config file"""

    server: str = DEFAULT_SERVER
    token: str = DEFAULT_TOKEN
    username: str = ""
    session_id: str = dc.field(default_factory=lambda: uuid.uuid4().hex)
    version: int = 1

    _env: t.ClassVar[Optional[str]]
    _path: t.ClassVar[Optional[Path]]

    def __post_init__(self):
        self.server = self.server.rstrip("/")  # server should be a valid origin

    @property
    def is_public(self) -> bool:
        return self.server == DEFAULT_SERVER

    # MANAGER functions
    @classmethod
    def load(cls, env: str = "default") -> "Config":
        """Load config for an environment and set globally"""
        config_f = cls.get_config_file(env)
        if not config_f.exists():
            cls.create_default(env, config_f)

        with config_f.open("r") as f:
            c_yaml = yaml.safe_load(f)

        # load config obj from file
        config = dacite.from_dict(Config, c_yaml)
        config._env = env
        config._path = config_f
        log.debug(f"Loaded client environment from {config._path}")

        # check if stored file is out of date
        config.upgrade_config_format()

        # set to the global state
        set_config(config)
        return config

    @classmethod
    def create_default(cls, env: str, config_f: Path) -> None:
        """Create an default config file"""
        from .analytics import capture_init

        # create default file
        _config = Config()
        _config.save(env)
        log.info(f"Created config file at {config_f}")
        capture_init(_config)

    def save(self, env: t.Optional[str] = None):
        if env:
            self._env = env
            self._path = self.get_config_file(env)

        with self._path.open("w") as f:
            yaml.safe_dump(dc.asdict(self), f)

    def remove(self):
        self._path.unlink()

    @staticmethod
    def get_config_file(env: str) -> Path:
        return APP_DIR / f"{env}.yaml"

    def upgrade_config_format(self):
        """Handles updating the older config format"""
        # migrate older config files
        if self.version == 1:
            from .analytics import capture_init

            self.version = 2

            # If token exists check still valid and can login
            if self.token and self.token != DEFAULT_TOKEN:
                from .api import ping

                with suppress(Exception):
                    self.username = ping(config=self, cli_login=True, verbose=False)

            capture_init(self)
            self.save()


# TODO - create a ConfigMgr singleton object?
config: Optional[Config] = None


################################################################################
# MODULE LEVEL INTERFACE
def init(config_env: str = "default", config: t.Optional[Config] = None) -> Config:
    """
    Init an API config
     - this MUST handle being called multiple times and only from the main-thread
    """
    if get_config() is not None:
        log.debug("Reinitialising client config")

    if config:
        set_config(config)
    else:
        config = Config.load(config_env)

    return config


def check_get_config() -> Config:
    """Attempt to get a config object, reloading if necessary"""
    global config
    if config.token == DEFAULT_TOKEN:
        # try reinit, as may have ran login in another terminal/subprocess
        _config = init(config._env)
        if _config.token == DEFAULT_TOKEN:
            # still don't have a token set for the env, open up the browser
            if not _IN_PYTEST:
                f = furl(path="/home/", origin=_config.server)
                webbrowser.open(url=str(f), new=2)
            raise InvalidTokenError(
                "Please sign-up and login - if you already have then please restart your Jupyter kernel/Python instance to initialize your new token"
            )
        return _config
    return config


def set_config(c: Optional[Config]):
    global config
    config = c


def get_config() -> Config:
    global config
    return config
