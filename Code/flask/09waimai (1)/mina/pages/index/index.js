//login.js
//获取应用实例
var app = getApp();
Page({
    data: {
        remind: '加载中',
        angle: 0,
        userInfo: {},
        islogin: false
    },
    goToIndex: function () {
        wx.switchTab({
            url: '/pages/food/index',
        });
    },
    onLoad: function () {
        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        })
        this.checklogin()
    },
    onShow: function () {

    },
    onReady: function () {
        var that = this;
        setTimeout(function () {
            that.setData({
                remind: ''
            });
        }, 1000);
        wx.onAccelerometerChange(function (res) {
            var angle = -(res.x * 30).toFixed(1);
            if (angle > 14) {
                angle = 14;
            } else if (angle < -14) {
                angle = -14;
            }
            if (that.data.angle !== angle) {
                that.setData({
                    angle: angle
                });
            }
        });
    },
    bindGetUserInfo(e) {
        var that = this
        wx.login({
            success(res) {
                if (res.code) {
                    //发起网络请求
                    console.log(res.code)
                    wx.request({
                        url: app.buildUrl('/v1/user/login'),
                        data: {
                            code: res.code,
                            nickName: e.detail.userInfo.nickName,
                            avatarUrl: e.detail.userInfo.avatarUrl,
                            gender: e.detail.userInfo.gender
                        },
                        method: 'POST',
                        header: app.getRequestHeader(),
                        success(res) {
                            if (res.data.code == -1) {
                                app.alert({'content': res.data.msg})
                                return;
                            }
                            if (res.data.code == 1) {
                                app.setCache('token', res.data.data.token)
                                that.goToIndex()
                            }
                        }
                    })
                } else {
                    console.log('登录失败！' + res.errMsg)
                }
            }
        });
        console.log(e.detail.userInfo)
    },
    checklogin: function () {
        var that = this
        wx.login({
            success(res) {
                if (res.code) {
                    //发起网络请求
                    console.log(res.code)
                    wx.request({
                        url: app.buildUrl('/v1/user/cklogin'),
                        data: {
                            'code': res.code,
                        },
                        method: 'POST',
                        header: app.getRequestHeader(),
                        success(res) {
                            if (res.data.code == -1) {

                                app.alert({'content': res.data.msg})
                                return;
                            }
                            if (res.data.code == 1) {
                                app.setCache('token', res.data.data.token)
                                that.setData({
                                    islogin: true
                                })
                            }
                        }
                    })
                } else {
                    console.log('登录失败！' + res.errMsg)
                }
            }
        });

    }
});