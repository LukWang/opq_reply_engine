from botoy import jconfig, logger
import os
import json
from .exceptions import ConfigErrorException

cur_file_dir = os.path.dirname(os.path.realpath(__file__))


class replyConfig:
    def __init__(self):
        # 需要的botoy配置
        self.host = ""
        self.port = ""
        # replyServer配置
        self.bot = 0
        self.super_user = 0  # bot主人的qq
        self.pic_dir = "pics"  # 用于存放下载图片的路径
        self.voice_dir = "voice"  # 用于存放语音回复的路径
        self.private_limit = 10  # 私聊回复与关键词的数量限制
        self.user_record_level = 1  # 用户行为记录的等级
        # user_record_level:
        # 0: do not record
        # 1: cmd level record
        # 2: reply_level_record
        self.cmd_search_regexp = True  # 查询关键字时是否使用正则匹配
        self.bot_primary_cmd = "bot_theme"  # bot的主题图库, 用于在生成【对话列表】时挑选显示的图片

        self.read_botoy_config()
        self.read_local_config()
        try:
            self.validation()
        except ConfigErrorException as e:
            logger.error(e.default_output())
            raise e

    def read_botoy_config(self):
        # 先检查botoy的jconfig
        self.host = jconfig.host
        self.port = jconfig.port
        if hasattr(jconfig, "bot"):
            self.bot = jconfig.bot
        if hasattr(jconfig, "super_user"):
            self.super_user = jconfig.super_user
        if hasattr(jconfig, "pic_dir"):
            self.pic_dir = jconfig.pic_dir
        if hasattr(jconfig, "voice_dir"):
            self.voice_dir = jconfig.voice_dir
        if hasattr(jconfig, "private_limit"):
            self.voice_dir = jconfig.voice_dir
        if hasattr(jconfig, "user_record_level"):
            self.voice_dir = jconfig.user_record_level
        if hasattr(jconfig, "cmd_search_regexp"):
            if jconfig.cmd_search_regexp > 0:
                self.cmd_search_regexp = True
            else:
                self.cmd_search_regexp = False
        if hasattr(jconfig, "bot_primary_cmd"):
            self.bot_primary_cmd = jconfig.bot_primary_cmd

    def read_local_config(self):
        # 如果有本地config则使用本地config
        local_config = os.path.join(cur_file_dir, "config.json")
        if os.path.exists(local_config):
            with open(local_config, 'r', encoding='utf-8') as f:
                config_json = json.load(f)
                if "bot" in config_json:
                    self.bot = config_json["bot"]
                if "super_user" in config_json:
                    self.super_user = config_json["super_user"]
                if "pic_dir" in config_json:
                    self.pic_dir = config_json['pic_dir']
                if "voice_dir" in config_json:
                    voice_dir = config_json['voice_dir']
                if "user_record_level" in config_json:
                    user_record_level = config_json["user_record_level"]
                if "private_limit" in config_json:
                    private_limit = config_json["user_record_level"]
                if "cmd_search_regexp" in config_json:
                    if config_json.cmd_search_regexp > 0:
                        self.cmd_search_regexp = True
                    else:
                        self.cmd_search_regexp = False
                if "bot_primary_cmd" in config_json:
                    self.bot_primary_cmd = config_json.bot_primary_cmd

    def validation(self):
        if self.super_user == 0:
            raise ConfigErrorException("super_user", "配置项不存在")
