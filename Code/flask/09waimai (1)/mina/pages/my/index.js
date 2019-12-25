//获取应用实例
var app = getApp();
Page({
    data: {},
    onLoad() {

    },
    onShow() {
        var that = this;
        // that.setData({
        //     user_info: {
        //         nickname: "test",
        //         avatar_url: "/images/more/logo.png"
        //     },
        // })
        that.getUserInfo()
    },
        getUserInfo: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/user/info'),
            method: 'GET',
            header: app.getRequestHeader(),
            success: function (res) {
                if (res.data.code != 1) {
                    app.alert({'content': data.msg})
                    return;
                }

                that.setData({
                    user_info:res.data.data.user_info,
                })
            }

        })

    }
});