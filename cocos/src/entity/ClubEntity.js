"use strict";

var ClubEntity = KBEngine.Entity.extend({
    ctor : function(club_base_info)
    {
        this._super();
        this.club_base_info = club_base_info;

        this.club_id = club_base_info["club_id"];
        this.club_name = club_base_info["club_name"];

        this.owner = club_base_info["owner"];

        this.club_notice = "";
        this.room_type = club_base_info["room_type"];
        this.table_info_list = [0, 0, 0, 0, 0, 0, 0, 0];
        KBEngine.DEBUG_MSG("Create ClubEntity")
    },

    update_club_info:function (club_detail_info) {
        this.member_num = club_detail_info["member_num"];
        this.room_type = club_detail_info["room_type"];
        this.club_notice = club_detail_info["club_notice"];
        this.table_info_list = club_detail_info["table_info_list"]
    },

    update_table_list:function (table_info_list) {
        this.table_info_list = table_info_list;
    },

    get_base_info:function () {
        return {
            "club_id" : this.club_id,
            "club_name" : this.club_name,
            "owner" : this.owner,
            // 'room_type': this.room_type,
        }
    },

    is_owner:function (user_id) {
        return user_id === this.owner.userId
    },

    getRoomCreateDict:function () {
        return {
			"room_type"			: this.room_type.room_type,
            "game_mode" 		: this.room_type.game_mode,
            "maxRound" 			: this.room_type.game_round,
            "game_max_lose" 	: this.room_type.game_max_lose,
            "base_score" 		: this.room_type.base_score,
            "round_max_lose" 	: this.room_type.round_max_lose,
            "king_mode" 		: this.room_type.play_list[0],
            "begin_dealer_mul" 	: this.room_type.play_list[1],
            "win_mode" 			: this.room_type.play_list[2],
            "three_job" 		: this.room_type.play_list[3],
            "pong_useful" 		: this.room_type.play_list[4],
            "bao_tou" 			: this.room_type.play_list[5],
			"pay_mode"			: this.room_type.pay_mode
		};
    },
});