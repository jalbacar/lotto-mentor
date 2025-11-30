"""Lotto CSV Downloader con verificación VPN"""
__version__ = "1.0.0"

from .downloader import LottoDownloader
from .config import Config
from .vpn_checker import VPNChecker

__all__ = ['LottoDownloader', 'Config', 'VPNChecker']