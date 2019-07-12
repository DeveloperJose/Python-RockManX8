from configparser import ConfigParser
from pathlib import Path


class Config:
    cfg_path: Path
    install_path: Path
    is_valid_collection: bool
    language: str

    @staticmethod
    def from_path(cfg_path):
        cfg = ConfigParser()
        cfg.read(cfg_path)
        return Config.from_parser(cfg_path, cfg)

    @staticmethod
    def from_parser(cfg_path: Path, cfg: ConfigParser):
        instnc = Config()
        instnc.cfg_path = cfg_path
        instnc.install_path = Path(cfg['editor']['installation_path'])
        instnc.is_valid_collection = cfg.getboolean('editor', 'is_legacy_collection')
        instnc.language = cfg['editor']['language']
        return instnc

    @staticmethod
    def create_default(cfg_path, lang_folder, install_path, is_valid_collection):
        cfg = ConfigParser()
        cfg.add_section('editor')
        cfg.set('editor', 'language', lang_folder)
        cfg.set('editor', 'installation_path', str(install_path))
        cfg.set('editor', 'is_legacy_collection', str(is_valid_collection))

        with open(cfg_path, 'w') as cfgfile:
            cfg.write(cfgfile)

        return Config.from_parser(cfg_path, cfg)
