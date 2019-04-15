var HelpUI = UIBase.extend({
    ctor: function () {
        this._super();
        this.resourceFilename = "res/ui/HelpUI.json";
        this.setLocalZOrder(const_val.MAX_LAYER_NUM);
    },

    show_by_info:function (info_dict) {
        this.info_dict = info_dict;
        this.show();
    },

    initUI: function () {
        var self = this;
        var player = h1global.player();
        var help_panel = this.rootUINode.getChildByName("help_panel");

        var close_btn = help_panel.getChildByName("close_btn");

        var room_mode_btn = help_panel.getChildByName("room_mode_btn");
        var title_mj_btn = help_panel.getChildByName("title_mj_btn");
        room_mode_btn.setTouchEnabled(false);
        room_mode_btn.setBright(false);
        title_mj_btn.setTouchEnabled(true);
        title_mj_btn.setBright(true);

        var room_mode_panel = help_panel.getChildByName("room_mode_panel");
        var title_mj_panel = help_panel.getChildByName("title_mj_panel");
        room_mode_panel.setVisible(true);
        title_mj_panel.setVisible(false);

        if(this.info_dict) {
            // this.change_select("rule_chx_" + this.info_dict.game_mode.toString());
            // this.change_select("round_chx_" + (this.info_dict.maxRound / 8 - 1).toString());
            // this.change_select("limit_chx_" + ((this.info_dict.round_max_lose / 10) > 3 ? 0 : (this.info_dict.round_max_lose / 10)).toString());
            // this.change_select("mobao_chx_" + this.info_dict.luckyTileNum.toString());

            this.change_select("game_mode_panel", "game_mode_chx" + String(this.info_dict.game_mode+1));
            if(this.info_dict.game_mode === 0){
                this.change_select("round_panel", "round_chx" + String(this.info_dict.maxRound/8));
            }else{
                this.change_select("game_max_lose_panel", "game_max_lose_chx" + String(this.info_dict.game_max_lose/10 - 3));
            }

            this.change_select("base_score_panel", "base_score_chx" + this.info_dict.base_score.toString());
            if(this.info_dict.round_max_lose >= 100){
                this.change_select("round_max_lose_panel", "round_max_lose_chx1");
            } else {
                var list = [0, 20, 40, 80]
                this.change_select("round_max_lose_panel", "round_max_lose_chx" + String(list.indexOf(this.info_dict.round_max_lose) + 1));
            }

            this.change_select("play_panel", "king_mode_chx" + String(this.info_dict.king_mode+1));
            this.change_select("play_panel", "begin_dealer_mul_chx" + this.info_dict.begin_dealer_mul.toString());
            this.change_select("play_panel", "win_mode_chx" + String(this.info_dict.win_mode+1));

            if(this.info_dict.three_job){
                this.change_select("play_panel", "three_job_chx1");
            }
            if(this.info_dict.pong_useful){
                this.change_select("play_panel", "pong_useful_chx1");
            }
            if(this.info_dict.bao_tou){
                this.change_select("play_panel", "bao_tou_chx1");
            }
            if (this.info_dict.pay_mode === const_val.AA_PAY_MODE) {
                this.change_select("pay_panel", "pay_mode_chx2")
            } else {
                this.change_select("pay_panel", "pay_mode_chx1")
            }
            this.updatePayText(this.info_dict.room_type);
        }else {
            this.gamehall_show();
        }

		close_btn.hitTest = function (pt) {
			var size = this.getContentSize();
			var bb = cc.rect(-size.width, -size.height * 0.3, size.width * 3, size.height * 2);
			return cc.rectContainsPoint(bb, this.convertToNodeSpace(pt));
		};
        close_btn.addTouchEventListener(function (sender, eventType) {
            if (eventType === ccui.Widget.TOUCH_ENDED) {
                self.hide();
            }
        });

        room_mode_btn.addTouchEventListener(function (sender, eventType) {
            if (eventType === ccui.Widget.TOUCH_ENDED) {
                room_mode_btn.setTouchEnabled(false);
                room_mode_btn.setBright(false);
                title_mj_btn.setTouchEnabled(true);
                title_mj_btn.setBright(true);
                title_mj_panel.setVisible(false);
                room_mode_panel.setVisible(true);
            }
        });

        title_mj_btn.addTouchEventListener(function (sender, eventType) {
            if (eventType === ccui.Widget.TOUCH_ENDED) {
                title_mj_btn.setTouchEnabled(false);
                title_mj_btn.setBright(false);
                room_mode_btn.setTouchEnabled(true);
                room_mode_btn.setBright(true);
                room_mode_panel.setVisible(false);
                title_mj_panel.setVisible(true);
            }
        });
    },

    change_select:function (parentName, chxName) {
        cc.log(parentName, chxName)
        var room_mode_panel = this.rootUINode.getChildByName("help_panel").getChildByName("room_mode_panel");
        var chx = room_mode_panel.getChildByName(parentName).getChildByName(chxName);
        chx.setBright(true);
    },

    gamehall_show:function () {
        var help_panel = this.rootUINode.getChildByName("help_panel");
        var room_mode_btn = help_panel.getChildByName("room_mode_btn");
        var title_mj_btn = help_panel.getChildByName("title_mj_btn");
        var line_img = help_panel.getChildByName("line_img");
        room_mode_btn.setVisible(false);
        line_img.setVisible(false);
        title_mj_btn.setTouchEnabled(false);
        title_mj_btn.setBright(false);
        title_mj_btn.setPositionY(title_mj_btn.getPositionY() + 100);

        var room_mode_panel = help_panel.getChildByName("room_mode_panel");
        var title_mj_panel = help_panel.getChildByName("title_mj_panel");
        room_mode_panel.setVisible(false);
        title_mj_panel.setVisible(true);
    },

	updatePayText: function (r_type) {
		var help_panel = this.rootUINode.getChildByName("help_panel");
		var room_mode_panel = help_panel.getChildByName("room_mode_panel");
		var pay_panel = room_mode_panel.getChildByName("pay_panel");
		var label_1 = pay_panel.getChildByName("pay_mode_label_1");
		if (r_type === const_val.CLUB_ROOM) {
			label_1.setString("老板支付");
		} else {
			label_1.setString("房主支付");
		}
	}
});