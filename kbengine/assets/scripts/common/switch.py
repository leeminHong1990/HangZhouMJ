# -*- coding: utf-8 -*-

DB_NAME = "kbe_HZMJ"

PUBLISH_VERSION = 0

DEBUG_BASE = 1 # 0 真实环境 1 调试环境 2 测试环境

PHP_SERVER_URL = 'http://10.0.0.4:9981/api/'
PHP_SERVER_SECRET = "zDYnetiVvFgWCRMIBGwsAKaqPOUjfNXS"
ACCOUNT_LOGIN_SECRET = "KFZ<]~ct(uYHM%#LABX<>>O6-N(~F#GM" # 登录校验的密钥

PHP_DEBUG_URL = 'http://localhost:9080/index.php'
CLUB_CARD_MIN	= 24
CLUB_CARD_WARN	= 100

#计算消耗
def calc_cost(game_round, default_avg):
	game_mode = default_avg['game_mode']
	pay_mode = default_avg['pay_mode']
	if game_mode == 0:
		base = int(game_round / 8)
		if pay_mode == 1:
			# AA
			return base, 9999
		else:
			return base * 4, 9999
	elif game_mode == 1:
		max_lose = default_avg['game_max_lose']
		base = int(max_lose / 10 - 3)
		if pay_mode == 1:
			# AA
			return base, 9999
		else:
			return base * 4, 9999
	return 9999, 9999