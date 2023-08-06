import os
from .schema_common_api_conf import CommonApiConf
from .schema_db_conf import DBConf
from .schema_ext_platform_conf import ExtPlatformConf
from .schema_message_sender_conf import MessageSenderConf

BASE_CONFIG_DIR = os.path.join('.','configs')

DB_CONFIG_DIR = os.path.join(BASE_CONFIG_DIR, 'db_conf.ini')
EXT_PLATFORM_CONFIG_DIR = os.path.join(BASE_CONFIG_DIR, 'ext_platform_conf.ini')

COMMON_API_CONFIG_DIR = os.path.join(BASE_CONFIG_DIR, 'common_api_conf.ini')

MESSAGE_SENDER_CONFIG_DIR = os.path.join(BASE_CONFIG_DIR, 'message_sender_conf.ini')


mapping_type = {
    DB_CONFIG_DIR: DBConf,
    EXT_PLATFORM_CONFIG_DIR: ExtPlatformConf,
    COMMON_API_CONFIG_DIR: CommonApiConf,
    MESSAGE_SENDER_CONFIG_DIR: MessageSenderConf,
}
