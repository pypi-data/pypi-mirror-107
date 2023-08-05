# (c) Roxy Corp. 2020-
# Roxy AI Inspect-Server API
import sys
from pathlib import Path
import json5 as json
import re
from termcolor import cprint

import logging.config
log = logging.getLogger(__name__)


class BaseConfig():
    def __init__(self, dic: dict):
        self._dic = dic
        for item, val in dic.items():
            setattr(self, item, val)

    @classmethod
    def load(cls, path):
        path = Path(path)
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            log.exception(f'Failed to load config file: {path}')
            raise

        try:
            dic = json.loads(text)
        except Exception:
            log.exception(f'Failed to parse config file: {path}')
            raise

        return cls(dic)


class CommonConfig(BaseConfig):
    """ 共通設定ファイル
    """
    # 定数定義
    DEFAULT_PATH = (Path(__file__).parent / '../../../config/common.json').resolve()

    @classmethod
    def load(cls, path=None):
        path = path or cls.DEFAULT_PATH
        if not path.exists():
            log.error(f'Config file does not exist: {path.absolute()}')
            cprint(
                f'Please copy config files "{cls.DEFAULT_PATH.name}" from default folder. '
                f'({cls.DEFAULT_PATH.parent / "default"})', color='yellow'
            )
            sys.exit(1)
        return super().load(path)


class ServerConfig(BaseConfig):
    """ 共通サーバ設定ファイル
    """
    # 定数定義
    DEFAULT_PATH = (Path(__file__).parent / '../../../config/server.json').resolve()

    @classmethod
    def load(cls, path=None):
        path = path or cls.DEFAULT_PATH
        if not path.exists():
            log.error(f'Config file does not exist: {path.absolute()}')
            cprint(
                f'Please copy config files "{cls.DEFAULT_PATH.name}" from default folder. '
                f'({cls.DEFAULT_PATH.parent / "default"})', color='yellow'
            )
            sys.exit(1)
        return super().load(path)

    def __init__(self, dic: dict):
        super().__init__(dic)
        for item, val in dic.items():
            if type(val) is list:
                hosts = []
                ports = []
                for v in val:
                    mr = re.match(r'(?P<host>(\d+\.\d+\.\d+\.\d+))\:(?P<port>(\d+))', v)
                    if mr:
                        hosts.append(mr['host'])
                        ports.append(int(mr['port']))
                setattr(self, item + '_host', hosts)
                setattr(self, item + '_port', ports)
