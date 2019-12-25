var app = getApp();
Page({
    data: {
        statusType: ["待付款", "待发货", "待收货", "待评价", "已完成", "已关闭"],
        status: ["-8", "-7", "-6", "-5", "1", "0"],
        currentType: 0,
        tabClass: ["", "", "", "", "", ""],
    },
    statusTap: function (e) {
        var curType = e.currentTarget.dataset.index;
        this.data.currentType = curType;
        this.setData({
            currentType: curType
        });
        this.onShow();
    },
    orderDetail: function (e) {
        wx.navigateTo({
            url: "/pages/my/order_info"
        })
    },
    onLoad: function (options) {
        // 生命周期函数--监听页面加载
    },
    onReady: function () {
        // 生命周期函数--监听页面初次渲染完
    },
    onShow: function () {
        var that = this;
        that.getOrderList();
        that.pay();
        that.comment()
    },
    onHide: function () {
        // 生命周期函数--监听页面隐藏
    },
    onUnload: function () {
        // 生命周期函数--监听页面卸载
    },
    onPullDownRefresh: function () {
        // 页面相关事件处理函数--监听用户下拉动作
    },
    onReachBottom: function () {
        // 页面上拉触底事件的处理函数

    },
    toDetallsTap: function (e) {
        console.log(e);
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        })
    },
    getOrderList: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/allorder'),
            method: 'GET',
            header: app.getRequestHeader(),
            data: {
                status: that.data.status[that.data.currentType]
            },
            success: function (res) {
                var data = res.data
                if (data.code != 1) {
                    app.alert({'content': data.msg});
                    return;
                }
                that.setData({
                    order_list:res.data.data.order_list
                })
            }
        })

    },
    pay: function (e) {
        var oder_sn = e.currentTarget.dataset.id
        var that = this
        wx.request({
            url: app.buildUrl('/v1/order/pay'),
            method: 'GET',
            header: app.getRequestHeader(),
            data: {
                order_sn: oder_sn
            },
            success: function (res) {
                var data = res.data
                if (data.code != 1) {
                    app.alert({'content': data.msg})
                    return;
                }
            }

        })
    },
    comment: function (e) {
        console.log(e);
        wx.navigateTo({
            url: "/pages/my/comment?id=" + e.currentTarget.dataset.id
        })
    }
});
