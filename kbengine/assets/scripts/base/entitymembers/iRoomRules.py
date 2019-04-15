# -*- coding: utf-8 -*-

import KBEngine
from KBEDebug import *
import utility
import const
import random

class iRoomRules(object):

	def __init__(self):
		# 房间的牌堆
		self.tiles = []
		self.meld_dict = dict()

	def swapSeat(self, swap_list):
		random.shuffle(swap_list)
		for i in range(len(swap_list)):
			self.players_list[i] = self.origin_players_list[swap_list[i]]

		for i,p in enumerate(self.players_list):
			if p is not None:
				p.idx = i

	def setPrevailingWind(self):
		#圈风
		if self.player_num != 4:
			return
		minDearerNum = min(self.dealerNumList)
		self.prevailing_wind = const.WINDS[(self.prevailing_wind + 1 - const.WIND_EAST)%len(const.WINDS)] if minDearerNum >= 1 else self.prevailing_wind
		self.dealerNumList = [0] * self.player_num if minDearerNum >= 1 else self.dealerNumList
		self.dealerNumList[self.dealer_idx] += 1

	def setPlayerWind(self):
		if self.player_num != 4:
			return
		#位风
		for i,p in enumerate(self.players_list):
			if p is not None:
				p.wind = (self.player_num + i - self.dealer_idx)%self.player_num + const.WIND_EAST

	def initTiles(self):
		# 万 条 筒
		self.tiles = list(const.CHARACTER) * 4 + list(const.BAMBOO) * 4 + list(const.DOT) * 4
		# 东 西 南 北
		self.tiles += [const.WIND_EAST, const.WIND_SOUTH, const.WIND_WEST, const.WIND_NORTH] * 4
		# 中 发 白
		self.tiles += [const.DRAGON_RED, const.DRAGON_GREEN, const.DRAGON_WHITE] * 4
		# # 春 夏 秋 冬
		# self.tiles += [const.SEASON_SPRING, const.SEASON_SUMMER, const.SEASON_AUTUMN, const.SEASON_WINTER]
		# # 梅 兰 竹 菊
		# self.tiles += [const.FLOWER_PLUM, const.FLOWER_ORCHID, const.FLOWER_BAMBOO, const.FLOWER_CHRYSANTHEMUM]
		DEBUG_MSG("room:{},curround:{} init tiles:{}".format(self.roomID, self.current_round, self.tiles))
		self.shuffle_tiles()

	def shuffle_tiles(self):
		random.shuffle(self.tiles)
		DEBUG_MSG("room:{},curround:{} shuffle tiles:{}".format(self.roomID, self.current_round, self.tiles))

	def deal(self, prefabHandTiles, prefabTopList):
		""" 发牌 """
		if prefabHandTiles is not None:
			for i,p in enumerate(self.players_list):
				if p is not None and len(prefabHandTiles) >= 0:
					p.tiles = prefabHandTiles[i] if len(prefabHandTiles[i]) <= const.INIT_TILE_NUMBER else prefabHandTiles[i][0:const.INIT_TILE_NUMBER]
			topList = prefabTopList if prefabTopList is not None else []
			allTiles = []
			for i, p in enumerate(self.players_list):
				if p is not None:
					allTiles.extend(p.tiles)
			allTiles.extend(topList)

			tile2NumDict = utility.getTile2NumDict(allTiles)
			warning_tiles = [t for t, num in tile2NumDict.items() if num > 4]
			if len(warning_tiles) > 0:
				WARNING_MSG("room:{},curround:{} prefab {} is larger than 4.".format(self.roomID, self.current_round,
																					 warning_tiles))
			for t in allTiles:
				if t in self.tiles:
					self.tiles.remove(t)
			for i in range(const.INIT_TILE_NUMBER):
				num = 0
				for j in range(self.player_num):
					if len(self.players_list[j].tiles) >= const.INIT_TILE_NUMBER:
						continue
					self.players_list[j].tiles.append(self.tiles[num])
					num += 1
				self.tiles = self.tiles[num:]

			newTiles = topList
			newTiles.extend(self.tiles)
			self.tiles = newTiles
		else:
			for i in range(const.INIT_TILE_NUMBER):
				for j in range(self.player_num):
					self.players_list[j].tiles.append(self.tiles[j])
				self.tiles = self.tiles[self.player_num:]

		for i, p in enumerate(self.players_list):
			DEBUG_MSG("room:{},curround:{} idx:{} deal tiles:{}".format(self.roomID, self.current_round, i, p.tiles))

	def kongWreath(self):
		""" 杠花 """
		for i in range(self.player_num):
			for j in range(len(self.players_list[i].tiles)-1, -1, -1):
				tile = self.players_list[i].tiles[j]
				if tile in const.SEASON or tile in const.FLOWER:
					del self.players_list[i].tiles[j]
					self.players_list[i].wreaths.append(tile)
					DEBUG_MSG("room:{},curround:{} kong wreath, idx:{},tile:{}".format(self.roomID, self.current_round, i, tile))

	def addWreath(self):
		""" 补花 """
		for i in range(self.player_num):
			while len(self.players_list[i].tiles) < const.INIT_TILE_NUMBER:
				if len(self.tiles) <= 0:
					break
				tile = self.tiles[0]
				self.tiles = self.tiles[1:]
				if tile in const.SEASON or tile in const.FLOWER:
					self.players_list[i].wreaths.append(tile)
					DEBUG_MSG("room:{},curround:{} add wreath, tile is wreath,idx:{},tile:{}".format(self.roomID, self.current_round, i, tile))
				else:
					self.players_list[i].tiles.append(tile)
					DEBUG_MSG("room:{},curround:{} add wreath, tile is not wreath, idx:{},tile:{}".format(self.roomID, self.current_round, i, tile))

	# def rollKingTile(self):
	# 	""" 财神 """
	# 	self.kingTiles = []
	# 	if self.king_num > 0:
	# 		for i in range(len(self.tiles)):
	# 			t = self.tiles[i]
	# 			if t not in const.SEASON and t not in const.FLOWER: #第一张非花牌
	# 				# 1-9为一圈 东南西北为一圈 中发白为一圈
	# 				self.kingTiles.append(t)
	# 				if self.king_num > 1:
	# 					for tup in (const.CHARACTER, const.BAMBOO, const.DOT, const.WINDS, const.DRAGONS):
	# 						if t in tup:
	# 							index = tup.index(t)
	# 							self.kingTiles.append(tup[(index + 1)%len(tup)])
	# 							break
	# 				del self.tiles[i]
	# 				break

	# 杭州麻将特殊处理
	def rollKingTile(self, prefabKingTiles):
		""" 财神 """
		self.kingTiles = []
		if prefabKingTiles is not None and len(prefabKingTiles) > 0:
			if self.king_mode == 0:  # 财神模式 固定白板
				self.kingTiles.append(const.DRAGON_WHITE)
			else:
				self.kingTiles.append(prefabKingTiles[0])
				for t in self.kingTiles:
					if t in self.tiles:
						self.tiles.remove(t)
		else:
			if self.king_num > 0:
				if self.king_mode == 0: # 财神模式 固定白板
					self.kingTiles.append(const.DRAGON_WHITE)
				else:
					for i in range(len(self.tiles)):
						t = self.tiles[i]
						if t not in const.SEASON and t not in const.FLOWER: #第一张非花牌
							# 1-9为一圈 东南西北为一圈 中发白为一圈
							self.kingTiles.append(t)
							if self.king_num > 1:
								for tup in (const.CHARACTER, const.BAMBOO, const.DOT, const.WINDS, const.DRAGONS):
									if t in tup:
										index = tup.index(t)
										self.kingTiles.append(tup[(index + 1)%len(tup)])
										break
							del self.tiles[i]
							break

	def tidy(self):
		""" 整理 """
		for i in range(self.player_num):
			self.players_list[i].tidy(self.kingTiles)

	def count_king_tile(self):
		for i in range(self.player_num):
			p = self.players_list[i]
			p.count_draw_king(p.tiles)

	def throwDice(self, idxList):
		diceList = [[0,0] for i in range(self.player_num)]
		for i in range(len(diceList)):
			if i in idxList:
				diceList[i][0] = random.randint(1, 6)
				diceList[i][1] = random.randint(1, 6)
		return diceList

	def getMaxDiceIdx(self, diceList):
		numList = [v[0] + v[1] for v in diceList]
		maxVal, maxIdx = max(numList), self.dealer_idx
		for i in range(self.dealer_idx, self.dealer_idx + self.player_num):
			idx = i%self.player_num
			if numList[idx] == maxVal:
				maxIdx = idx
				break
		return maxIdx, maxVal

	def drawLuckyTile(self):
		return []
		# luckyTileList = []
		# for i in range(self.lucky_num):
		# 	if len(self.tiles) > 0:
		# 		luckyTileList.append(self.tiles[0])
		# 		self.tiles = self.tiles[1:]
		# return luckyTileList

	def cal_lucky_tile_score(self, lucky_tiles, winIdx):
		pass

	def swapTileToTop(self, tile):
		if tile in self.tiles:
			tileIdx = self.tiles.index(tile)
			self.tiles[0], self.tiles[tileIdx] = self.tiles[tileIdx], self.tiles[0]

	def winCount(self):
		pass

	def canTenPai(self, handTiles):
		length = len(handTiles)
		if length % 3 != 1:
			return False

		result = []
		tryTuple = (const.CHARACTER, const.BAMBOO, const.DOT, const.WINDS, const.DRAGONS)
		for tup in tryTuple:
			for t in tup:
				tmp = list(handTiles)
				tmp.append(t)
				sorted(tmp)
				if utility.isWinTile(tmp, self.kingTiles):
					result.append(t)
		return result != []

	def is_op_times_limit(self, idx):
		"""吃碰杠次数限制"""
		if self.three_job and (idx == self.dealer_idx or self.last_player_idx == self.dealer_idx): # 三摊 承包的模式 庄闲之间 无限制
			return False
		op_r = self.players_list[idx].op_r
		include_op_list = [const.OP_CHOW, const.OP_PONG, const.OP_EXPOSED_KONG] if self.pong_useful else [const.OP_CHOW]
		times = sum([1 for record in op_r if record[2] == self.last_player_idx and record[0] in include_op_list])
		return times >= 2

	def is_op_kingTile_limit(self, idx):
		"""打财神后操作限制"""
		if self.discard_king_idx >= 0 and self.discard_king_idx != idx:
			return True
		return False

	def is_op_limit(self, idx):
		"""操作限制"""
		if self.is_op_times_limit(idx) or self.is_op_kingTile_limit(idx):
			return True
		return False

	def circleSameTileNum(self, idx, t):
		"""获取一圈内打出同一张牌的张数"""
		discard_num = 0
		for record in reversed(self.op_record):
			if record[1] == idx:
				break
			if record[0] == const.OP_DISCARD and record[3][0] == t:
				discard_num += 1
		return discard_num

	def can_cut_after_kong(self):
		return False

	def can_discard(self, idx, t):
		if self.is_op_kingTile_limit(idx):
			if t == self.players_list[idx].last_draw:
				return True
			return False
		return True

	def can_chow(self, idx, t):
		if self.is_op_limit(idx):
			return False
		if t in self.kingTiles:
			return False
		# 白板代替财神
		virtual_tile = self.kingTiles[0] if t == const.DRAGON_WHITE and len(self.kingTiles) > 0 else t
		if virtual_tile >= const.BOUNDARY:
			return False
		tiles = list(filter(lambda x:x not in self.kingTiles, self.players_list[idx].tiles))
		tiles = list(map(lambda x:self.kingTiles[0] if x == const.DRAGON_WHITE else x, tiles))
		MATCH = ((-2, -1), (-1, 1), (1, 2))
		for tup in MATCH:
			if all(val+virtual_tile in tiles for val in tup):
				return True
		return False

	def can_chow_list(self, idx, tile_list):
		chow_list = list(tile_list)
		# """ 能吃 """
		if self.is_op_limit(idx):
			return False
		if len(chow_list) != 3:
			return False
		if any(t in self.kingTiles for t in tile_list):
			return False
		virtual_chow_list = list(tile_list)
		virtual_chow_list = list(map(lambda x:self.kingTiles[0] if x == const.DRAGON_WHITE else x, virtual_chow_list))
		if any(t >= const.BOUNDARY for t in virtual_chow_list):
			return False
		tiles 		= list(filter(lambda x: x not in self.kingTiles, self.players_list[idx].tiles))
		tiles 		= list(map(lambda x:self.kingTiles[0] if x == const.DRAGON_WHITE else x, tiles))
		if virtual_chow_list[1] in tiles and virtual_chow_list[2] in tiles:
			sortLis = sorted(virtual_chow_list)
			if (sortLis[2] + sortLis[0])/2 == sortLis[1] and sortLis[2] - sortLis[0] == 2:
				return True
		return False

	def can_pong(self, idx, t):
		""" 能碰 """
		if self.is_op_kingTile_limit(idx):
			return False
		if self.pong_useful and self.is_op_times_limit(idx):
			return False

		if self.circleSameTileNum(idx, t) >= 2:
			return False
		tiles = self.players_list[idx].tiles
		if t in self.kingTiles:
			return False
		return sum([1 for i in tiles if i == t]) >= 2

	def can_exposed_kong(self, idx, t):
		""" 能明杠 """
		if self.is_op_kingTile_limit(idx):
			return False
		if self.pong_useful and self.is_op_times_limit(idx):
			return False

		if t in self.kingTiles:
			return False
		tiles = self.players_list[idx].tiles
		return tiles.count(t) == 3

	def can_continue_kong(self, idx, t):
		""" 能够补杠 """
		if t in self.kingTiles:
			return False
		player = self.players_list[idx]
		for op in player.op_r:
			if op[0] == const.OP_PONG and op[1][0] == t:
				return True
		return False

	def can_concealed_kong(self, idx, t):
		""" 能暗杠 """
		if t in self.kingTiles:
			return False
		tiles = self.players_list[idx].tiles
		return tiles.count(t) == 4

	def can_kong_wreath(self, tiles, t):
		if t in tiles and (t in const.SEASON or t in const.FLOWER):
			return True
		return False

	def can_wreath_win(self, wreaths):
		if len(wreaths) == len(const.SEASON) + len(const.FLOWER):
			return True
		return False

	def getNotifyOpList(self, idx, aid, tile):
		# notifyOpList 和 self.wait_op_info_list 必须同时操作
		# 数据结构：问询玩家，操作玩家，牌，操作类型，得分，结果，状态
		notifyOpList = [[] for i in range(self.player_num)]
		self.wait_op_info_list = []
		#胡
		if aid == const.OP_KONG_WREATH and self.can_wreath_win(self.players_list[idx].wreaths): # 8花胡
			opDict = {"idx":idx, "from":idx, "tileList":[tile,], "aid":const.OP_WREATH_WIN, "score":0, "result":[], "state":const.OP_STATE_WAIT}
			notifyOpList[idx].append(opDict)
			self.wait_op_info_list.append(opDict)
		elif aid == const.OP_EXPOSED_KONG: #直杠 抢杠胡
			# wait_for_win_list = self.getKongWinList(idx, tile)
			# self.wait_op_info_list.extend(wait_for_win_list)
			# for i in range(len(wait_for_win_list)):
			# 	dic = wait_for_win_list[i]
			# 	notifyOpList[dic["idx"]].append(dic)
			pass
		elif aid == const.OP_CONTINUE_KONG: #碰后接杠 抢杠胡
			# wait_for_win_list = self.getKongWinList(idx, tile)
			# self.wait_op_info_list.extend(wait_for_win_list)
			# for i in range(len(wait_for_win_list)):
			# 	dic = wait_for_win_list[i]
			# 	notifyOpList[dic["idx"]].append(dic)
			pass
		elif aid == const.OP_CONCEALED_KONG:
			pass
		elif aid == const.OP_DISCARD:
			#胡(放炮胡)
			wait_for_win_list = self.getGiveWinList(idx, tile)
			self.wait_op_info_list.extend(wait_for_win_list)
			for i in range(len(wait_for_win_list)):
				dic = wait_for_win_list[i]
				notifyOpList[dic["idx"]].append(dic)
			#杠 碰
			for i, p in enumerate(self.players_list):
				if p and i != idx:
					if self.can_exposed_kong(i, tile):
						opDict = {"idx":i, "from":idx, "tileList":[tile,], "aid":const.OP_EXPOSED_KONG, "score":0, "result":[], "state":const.OP_STATE_WAIT}
						self.wait_op_info_list.append(opDict)
						notifyOpList[i].append(opDict)
					if self.can_pong(i, tile):
						opDict = {"idx":i, "from":idx, "tileList":[tile,], "aid":const.OP_PONG, "score":0, "result":[], "state":const.OP_STATE_WAIT}
						self.wait_op_info_list.append(opDict)
						notifyOpList[i].append(opDict)
			#吃
			nextIdx = self.nextIdx
			if self.can_chow(nextIdx, tile):
				opDict = {"idx":nextIdx, "from":idx, "tileList":[tile,], "aid":const.OP_CHOW, "score":0, "result":[], "state":const.OP_STATE_WAIT}
				self.wait_op_info_list.append(opDict)
				notifyOpList[nextIdx].append(opDict)
		return notifyOpList


	# 抢杠胡 玩家列表
	def getKongWinList(self, idx, tile):
		wait_for_win_list = []
		for i in range(self.player_num - 1):
			ask_idx = (idx+i+1)%self.player_num
			p = self.players_list[ask_idx]
			tryTiles = list(p.tiles)
			tryTiles.append(tile)
			tryTiles = sorted(tryTiles)
			DEBUG_MSG("room:{},curround:{} getKongWinList {}".format(self.roomID, self.current_round, ask_idx))
			is_win, score, result = self.can_win(tryTiles, tile, const.OP_KONG_WIN, ask_idx)
			if is_win:
				wait_for_win_list.append({"idx":ask_idx, "from":idx, "tileList":[tile,], "aid":const.OP_KONG_WIN, "score":score, "result":result, "state":const.OP_STATE_WAIT})
		return wait_for_win_list

	# 放炮胡 玩家列表
	def getGiveWinList(self, idx, tile):
		wait_for_win_list = []
		if self.win_mode == 0 or self.cur_dealer_mul < 3: # 放铳模式 庄三有效
			return  wait_for_win_list
		for i in range(self.player_num - 1):
			ask_idx = (idx+i+1)%self.player_num
			if ask_idx != self.dealer_idx and idx != self.dealer_idx: # 庄闲放铳
				continue
			p = self.players_list[ask_idx]
			tryTiles = list(p.tiles)
			tryTiles.append(tile)
			tryTiles = sorted(tryTiles)
			DEBUG_MSG("room:{},curround:{} getGiveWinList {} tile {}".format(self.roomID, self.current_round, ask_idx, tile))
			is_win, score, result = self.can_win(tryTiles, tile, const.OP_GIVE_WIN, ask_idx)
			if is_win:
				wait_for_win_list.append({"idx":ask_idx, "from":idx, "tileList":[tile,], "aid":const.OP_GIVE_WIN, "score":score, "result":result, "state":const.OP_STATE_WAIT})
		return wait_for_win_list

	def can_win(self, handTiles, finalTile, win_op, idx):
		#"""平胡 爆头 七对子 清七对"""
		#"""杠 + 飘"""
		result_list = [0] * 4
		multiply = 0
		if len(handTiles) % 3 != 2:
			DEBUG_MSG("room:{},curround:{} handTiles:{} finalTile:{} win_op:{} idx:{}".format(self.roomID, self.current_round, handTiles, finalTile, win_op, idx))
			return False, self.base_score * (2**multiply), result_list
		if win_op == const.OP_WREATH_WIN:
			DEBUG_MSG("room:{},curround:{} handTiles:{} finalTile:{} win_op:{} idx:{}".format(self.roomID, self.current_round, handTiles, finalTile, win_op, idx))
			return False, 2 ** multiply, result_list
		if win_op == const.OP_GIVE_WIN and finalTile in self.kingTiles:
			DEBUG_MSG("room:{},curround:{} handTiles:{} finalTile:{} win_op:{} idx:{}".format(self.roomID, self.current_round, handTiles, finalTile, win_op, idx))
			return False, 2 ** multiply, result_list

		p = self.players_list[idx]
		handCopyTiles = list(handTiles)
		handCopyTiles = sorted(handCopyTiles)
		kings, handTilesButKing = utility.classifyKingTiles(handCopyTiles, self.kingTiles)
		kingTilesNum = len(kings)
		# 白板代替财神
		if len(self.kingTiles) > 0:
			handTilesButKing = list(map(lambda x:self.kingTiles[0] if x == const.DRAGON_WHITE else x, handTilesButKing))
			insteadFinalTile = self.kingTiles[0] if finalTile == const.DRAGON_WHITE else finalTile
		else:
			insteadFinalTile = finalTile
		handTilesButKing = sorted(handTilesButKing)
		#2N
		is7Pair, isBaoTou, kongNum = utility.checkIs7Pair(handCopyTiles, handTilesButKing, kingTilesNum, self.kingTiles, insteadFinalTile)
		if is7Pair:
			DEBUG_MSG("room:{},curround:{} is7Pair".format(self.roomID, self.current_round))
			result_list[2] = 1 + kongNum
			multiply += result_list[2]
			if isBaoTou:
				result_list[1] = 1
				kingKongList = [1 if op == const.OP_DISCARD else -1 for op in utility.serialKingKong(p.op_r, self.kingTiles)]
				multiply += len(kingKongList) + 1
				result_list.extend(kingKongList)
				DEBUG_MSG("room:{},curround:{} is7Pair baotou".format(self.roomID, self.current_round))
				return True , self.base_score * (2 ** multiply), result_list
			elif kingTilesNum <= 0:
				result_list[3] = 1
				multiply += 1
				DEBUG_MSG("room:{},curround:{} is7Pair not baotou kingNum:0".format(self.roomID, self.current_round))
				return True, self.base_score * (2 ** multiply), result_list
			if self.bao_tou == 0:
				return True, self.base_score * (2**multiply), result_list

		#3N2
		result_list = [0] * 4
		multiply = 0
		if kingTilesNum <= 0: 	#无财神(只要满足能胡就可以胡)
			DEBUG_MSG("room:{},curround:{} kingTilesNum <= 0".format(self.roomID, self.current_round))
			if utility.meld_with_pair_need_num(handTilesButKing) <= kingTilesNum:
				result_list[0] = 1
				for op in utility.serialKingKong(p.op_r, self.kingTiles): #只有连续杠开
					if op != const.OP_DISCARD:
						result_list.append(-1)
						multiply += 1
					else:
						break
				DEBUG_MSG("room:{},curround:{} 3N2 kingNum:0".format(self.roomID, self.current_round))
				return True, self.base_score * (2**multiply), result_list
			DEBUG_MSG("room:{},curround:{} handTiles:{} finalTile:{} win_op:{} idx:{}".format(self.roomID, self.current_round, handTiles, finalTile, win_op, idx))
			return False, self.base_score * (2**multiply), result_list
		else:					#有财神(只要暴头都可以胡, 如果有财必暴，非暴头不能胡)
			# 除去暴头一对组成3N
			baotou_n3_list = []
			tryKingsNum = kingTilesNum
			if finalTile in self.kingTiles: # 最后一张 摸的是财神
				if tryKingsNum >= 2:
					tryKingsNum -= 2
					baotou_n3_list.append(list(handTilesButKing))
			else:
				tryKingsNum -= 1
				tryList = list(handTilesButKing)
				tryList.remove(insteadFinalTile) # 若最后一张不是财神 则用代替后的牌
				baotou_n3_list.append(tryList)
			DEBUG_MSG("room:{},curround:{} baotou_n3_list:{}".format(self.roomID, self.current_round, baotou_n3_list))
			#优先尝试暴头
			for tryList in baotou_n3_list:
				if utility.getMeldNeed(tryList) <= tryKingsNum:
					result_list[1] = 1
					# 连续飘杠胜利
					kingKongList = [1 if op == const.OP_DISCARD else -1 for op in utility.serialKingKong(p.op_r, self.kingTiles)]
					multiply += len(kingKongList) + 1
					result_list.extend(kingKongList)
					DEBUG_MSG("room:{},curround:{} 3N baotou".format(self.roomID, self.current_round))
					return True, self.base_score * (2 ** multiply), result_list
			else:
				DEBUG_MSG("room:{},curround:{} try not baotou".format(self.roomID, self.current_round))
				if self.bao_tou == 0 and utility.winWith3N2NeedKing(handTilesButKing) <= kingTilesNum:
					result_list[0] = 1
					# 连续杠胜利
					for op in utility.serialKingKong(p.op_r, self.kingTiles):  # 只有连续杠开
						if op != const.OP_DISCARD:
							result_list.append(-1)
							multiply += 1
						else:
							break
					DEBUG_MSG("room:{},curround:{} 3N not baotou".format(self.roomID, self.current_round))
					return True, self.base_score * (2 ** multiply), result_list
				DEBUG_MSG("room:{},curround:{} handTiles:{} finalTile:{} win_op:{} idx:{}".format(self.roomID, self.current_round, handTiles, finalTile, win_op, idx))
				return False, self.base_score * (2 ** multiply), result_list

	def job_relation(self): # 承包关系
		relations = []
		# 是否有三摊承包
		if not self.three_job:
			return relations
		# 碰是否算摊
		include_op_list = [const.OP_CHOW, const.OP_PONG, const.OP_EXPOSED_KONG] if self.pong_useful else [const.OP_CHOW]
		for k,v in enumerate(self.players_list):
			if v is not None:
				job_dict = {}
				for record in v.op_r:
					if (record[2] == self.dealer_idx or k == self.dealer_idx) and record[2] != k and record[0] in include_op_list:
						if record[2] not in job_dict:
							job_dict.setdefault(record[2],1)
						else:
							job_dict[record[2]] += 1
				for x,y in job_dict.items():
					if y >= 3:
						relations.append([k, x]) # k 吃 x 3次
		DEBUG_MSG("room:{},curround:{} job_relation {}".format(self.roomID, self.current_round, relations))
		return relations

	def cal_score(self, idx, fromIdx, aid, score):
		if aid == const.OP_EXPOSED_KONG:
			pass
		elif aid == const.OP_CONTINUE_KONG or aid == const.OP_CONCEALED_KONG:
			pass
		elif aid == const.OP_DRAW_WIN:
			relations = self.job_relation()
			if any(idx in rel for rel in relations): #有承包关系
				useful_rel_list = [rel for rel in relations if idx in rel]
				# 存在 互相承包的情况
				# 庄家赢 和 闲家赢 承包分数不同
				sub_all = score * (2 ** self.cur_dealer_mul) * 3 if idx == self.dealer_idx else score*(2**self.cur_dealer_mul) + score*2
				for rel in useful_rel_list:
					if idx == rel[0]:  # 吃三次
						real_Lose = self.players_list[rel[1]].add_score(-sub_all)
						self.players_list[rel[0]].add_score(-real_Lose)
						DEBUG_MSG("room:{0},curround:{1} OP_DRAW_WIN==>relation3: sub_all:{2},real_lose[idx:{3}-{4},idx:{5}-{6}]".format(self.roomID, self.current_round, sub_all,rel[1],real_Lose,rel[0],-real_Lose))
					else:  # 被吃三次(双倍)
						real_Lose = self.players_list[rel[0]].add_score(-sub_all * 2)
						self.players_list[rel[1]].add_score(-real_Lose)
						DEBUG_MSG("room:{0},curround:{1} OP_DRAW_WIN==>be relation3: sub_all:{2},real_lose[idx:{3}-{4},idx:{5}-{6}]".format(self.roomID, self.current_round, sub_all*2,rel[1],real_Lose,rel[0],-real_Lose))
			else:
				if idx == self.dealer_idx:	#庄家赢
					score *= 2 ** self.cur_dealer_mul
					real_Lose = 0
					for k,v in enumerate(self.players_list):
						if v is not None and k != idx:
							lose = v.add_score(-score)
							real_Lose += lose
							DEBUG_MSG("room:{0},curround:{1} OP_DRAW_WIN==>dealerwin: score:{2},idx:{3}-{4}".format(self.roomID, self.current_round, score, k, lose))
					self.players_list[idx].add_score(-real_Lose)
					DEBUG_MSG("room:{0},curround:{1} OP_DRAW_WIN==>dealerwin: score:{2},idx:{3}-{4}".format(self.roomID, self.current_round, score, idx, -real_Lose))
				else:						#非庄家赢
					# sub
					real_Lose = 0
					for k,v in enumerate(self.players_list):
						if v is not None and k != idx:
							if k == self.dealer_idx:
								dealer_lose = score * (2 ** self.cur_dealer_mul)
								lose = v.add_score(-dealer_lose)
								real_Lose += lose
								DEBUG_MSG("room:{0},curround:{1} OP_DRAW_WIN==>notdealerwin: dealer_lose:{2},idx:{3}-{4}".format(self.roomID, self.current_round, dealer_lose, k, lose))
							else:
								lose = v.add_score(-score)
								real_Lose += lose
								DEBUG_MSG("room:{0},curround:{1} OP_DRAW_WIN==>notdealerwin: score:{2},idx:{3}-{4}".format(self.roomID, self.current_round, score, k, lose))
					# add
					self.players_list[idx].add_score(-real_Lose)
					DEBUG_MSG("room:{0},curround:{1} OP_DRAW_WIN==>notdealerwin: idx:{2}-{3}".format(self.roomID, self.current_round, idx, -real_Lose))
		elif aid == const.OP_KONG_WIN:
			pass
		elif aid == const.OP_GIVE_WIN:
			# 放炮模式 除承包外 放炮还要算分
			if idx == self.dealer_idx:  # 庄家赢
				sub_all = score * (2 ** self.cur_dealer_mul) * 3
				real_Lose = self.players_list[fromIdx].add_score(-sub_all)
				self.players_list[idx].add_score(-real_Lose)
				DEBUG_MSG("room:{0},curround:{1} OP_GIVE_WIN==>dealerwin:sub_all:{2} real_lose[idx:{3}-{4},idx:{5}-{6}]".format(self.roomID, self.current_round, sub_all, fromIdx, real_Lose, idx, -real_Lose))
			else:  # 非庄家赢
				sub_all = score * (2 ** self.cur_dealer_mul) + score * 2
				real_Lose = self.players_list[fromIdx].add_score(-sub_all)
				self.players_list[idx].add_score(-real_Lose)
				DEBUG_MSG("room:{0},curround:{1} OP_GIVE_WIN==>notdealerwin:sub_all:{2} real_lose[idx:{3}-{4},idx:{5}-{6}]".format(self.roomID, self.current_round, sub_all, fromIdx, real_Lose,idx, -real_Lose))

			relations = self.job_relation()
			# 放炮两个人之间 有承包关系
			useful_rel_list = [rel for rel in relations if idx in rel and fromIdx in rel]
			if len(useful_rel_list) > 0:
				for rel in useful_rel_list:
					if idx == rel[0]:  # 吃三次
						real_Lose = self.players_list[rel[1]].add_score(-sub_all)
						self.players_list[rel[0]].add_score(-real_Lose)
						DEBUG_MSG("room:{0},curround:{1} OP_GIVE_WIN==>relation3:sub_all:{2} real_lose[idx:{3}-{4},idx:{5}-{6}]".format(self.roomID, self.current_round, sub_all, rel[1], real_Lose, rel[0], -real_Lose))
					else:  # 被吃三次(双倍)
						real_Lose = self.players_list[rel[0]].add_score(-sub_all * 2)
						self.players_list[rel[1]].add_score(-real_Lose)
						DEBUG_MSG("room:{0},curround:{1} OP_GIVE_WIN==>be relation3:sub_all:{2} real_lose[idx:{3}-{4},idx:{5}-{6}]".format(self.roomID, self.current_round, sub_all * 2, rel[1], real_Lose, rel[0], -real_Lose))
		elif aid == const.OP_WREATH_WIN:
			pass