"use strict";
var ActivityUI = BasicDialogUI.extend({
    ctor:function() {
        this._super();
        this.resourceFilename = "res/ui/ActivityUI.json";
    },

    initUI:function(){
        var self = this;
        var activity_panel = this.rootUINode.getChildByName("activity_panel");
        activity_panel.getChildByName("close_btn").addTouchEventListener(function(sender, eventType){
            if(eventType == ccui.Widget.TOUCH_ENDED){
                self.hide();
            }
        });

        this.btn_list = [];

        for (var i = 0; i < 6; i++) {
            if (i == 0 || i == 1 || i == 2 || i==3 ) {
                continue;
            }
            var btn = activity_panel.getChildByName("notice_btn" + i.toString());
            if (i === 5) {
                btn.setTouchEnabled(false);
                btn.setBright(false);
            }
            let index = i;
            this.btn_list.push(btn);
            if (i === 5) {
                btn.addTouchEventListener(function (source, eventType) {
                    if (eventType === ccui.Widget.TOUCH_ENDED) {
                        activity_panel.getChildByName("notice_panel").getChildByName("notice_img").setVisible(false);
                        activity_panel.getChildByName("notice_panel").getChildByName("ruler_panel").setVisible(true);
                        for (var j = 0; j < self.btn_list.length; j++) {
                            var obj = self.btn_list[j];
                            obj.setTouchEnabled(obj !== source);
                            obj.setBright(obj !== source);
                        }
                    }
                });
                continue;
            }
            btn.addTouchEventListener(function (source, eventType) {
                if (eventType === ccui.Widget.TOUCH_ENDED) {
                    activity_panel.getChildByName("notice_panel").getChildByName("notice_img").setVisible(true);
                    activity_panel.getChildByName("notice_panel").getChildByName("ruler_panel").setVisible(false);
                    var imgView = activity_panel.getChildByName("notice_panel")
                        .getChildByName("notice_img");
                    imgView.loadTexture("res/ui/ActivityUI/notice_img" + index + ".png");
                    for (var j = 0; j < self.btn_list.length; j++) {
                        var obj = self.btn_list[j];
                        obj.setTouchEnabled(obj !== source);
                        obj.setBright(obj !== source);
                    }
                }
            });
        }
    },
});