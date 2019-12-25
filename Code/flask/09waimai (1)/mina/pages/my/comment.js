//获取应用实例
var app = getApp();
Page({
    data: {
        "content":"非常愉快的订餐体验~~",
        "score":10,
        "order_sn":""
    },
    onLoad: function (options) {
        console.log(options);
        this.setData({
            order_sn:options.id
        })

    },
    scoreChange:function( e ){
        this.setData({
            "score":e.detail.value
        });
    },
    inputchange:function(e){
        this.setData({
            content:e.detail.value
        })
    },

    doComment:function(){
        var that = this;
        wx.request({
            url: app.buildUrl("/v1/comment/add"),
            data:{
                order_sn:that.data.order_sn,
                score:that.data.score,
                content:that.data.content,
            },
            method:"POST",
            header: app.getRequestHeader(),
            success: function (res) {
                var resp = res.data;
                if (resp.code != 1) {
                    app.alert({"content": resp.msg});
                    return;
                }
            }
        });
    }
});
