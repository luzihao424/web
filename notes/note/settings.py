import os
import socket
from urllib.parse import urlparse, urlunparse

def resolve_db_host_to_ipv4(uri):
    """
    为了解决 Render 等不支持 IPv6 的环境连接 Supabase 报错的问题：
    在将数据库链接传给 SQLAlchemy/psycopg2 之前，在 Python 层面先将其解析为公网 IPv4 地址，
    避免底层 C 语言库 (libpq) 进行 IPv6 的 DNS 解析。
    """
    if not uri or uri.startswith("sqlite"):
        return uri
    try:
        parsed = urlparse(uri)
        if not parsed.hostname:
            return uri
        # 强制只获取 IPv4 地址 (AF_INET)
        addr_info = socket.getaddrinfo(parsed.hostname, parsed.port or 5432, socket.AF_INET)
        ipv4_address = addr_info[0][4][0]
        
        # 将连接串中的域名替换为 IPv4 IP 地址
        netloc = parsed.netloc.replace(parsed.hostname, ipv4_address)
        return urlunparse((
            parsed.scheme,
            netloc,
            parsed.path,
            parsed.params,
            parsed.query,
            parsed.fragment
        ))
    except Exception as e:
        # 如果解析失败，打印错误原因以便调试，并回退到原 URI
        import sys
        print(f"DEBUG: resolve_db_host_to_ipv4 failed with error: {e}", file=sys.stderr)
        return uri

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-2026")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    DEBUG = True
    # 本地开发：使用 resolve_db_host_to_ipv4 处理
    SQLALCHEMY_DATABASE_URI = resolve_db_host_to_ipv4(os.getenv("DATABASE_URL", "sqlite:///data.db"))
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

class TestConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

class ProdConfig(BaseConfig):
    DEBUG = False
    # 生产环境：使用 resolve_db_host_to_ipv4 处理
    SQLALCHEMY_DATABASE_URI = resolve_db_host_to_ipv4(os.getenv("DATABASE_URL"))
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith("postgres://"):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace("postgres://", "postgresql://", 1)

config_map = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}