//获取应用实例
var app = getApp();

Page({
    data: {
        // goods_list: [
        //     {
        //         id:22,
        //         name: "小鸡炖蘑菇",
        //         price: "85.00",
        //         pic_url: "/images/food.jpg",
        //         number: 1,
        //     },
        //     {
        //         id:22,
        //         name: "小鸡炖蘑菇",
        //         price: "85.00",
        //         pic_url: "/images/food.jpg",
        //         number: 1,
        //     }
        // ],
        // default_address: {
        //     name: "编程浪子",
        //     mobile: "12345678901",
        //     detail: "上海市浦东新区XX",
        // },
        // yun_price: "1.00",
        // pay_price: "85.00",
        // total_price: "86.00",
        // params: null,
        ids: [],
        address_id: 0,
        note: '',
        num:0,
        fid:0,
        type:0,
    },
    onShow: function () {
        var that = this;
    },
    onLoad: function (options) {
        var that = this;
        // var ids = JSON.parse(options.ids);
        var type = options.type;
        var ids = options.ids;
        that.setData({
            type:type
        });
        if (type == '0') {
            var ids = JSON.parse(options.ids);
            that.setData({
                ids: ids
            });
            this.getOrderInfo()
        }else{
            var fid = options.fid;
            var num = options.num;
            that.setData({
                fid:fid,
                num:num
            });
            this.getOrderInfo1()
        }
    },

    formName: function (e) {
        this.setData({
            note: e.detail.value
        })
    },
    createOrder: function (e) {
        var that = this;
        if (that.data.type == '0'){
            wx.request({
            url: app.buildUrl('/v1/order/create'),//仅为实例
            method: 'POST',
            data: {
                ids: JSON.stringify(that.data.ids),
                note: that.data.note,
                address_id: that.data.address_id //购物车二
            },
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code == 1) {
                    wx.navigateTo({
                    url: "/pages/my/order_list"
                });
                }
            }
        })
        }else{
            wx.request({
            url: app.buildUrl('/v1/order/create1'),//仅为实例
            method: 'POST',
            data: {
                 id:that.data.fid,
                num:that.data.num,
                note: that.data.note,
                address_id: that.data.address_id //购物车二
            },
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code == 1) {
                    wx.navigateTo({
                    url: "/pages/my/order_list"
                });
                }
            }
        })
        }

    },
    addressSet: function () {
        wx.navigateTo({
            url: "/pages/my/addressSet"
        });
    },
    selectAddress: function () {
        wx.navigateTo({
            url: "/pages/my/addressList"
        });
    },


    getOrderInfo: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/info'),//仅为实例
            data: {
                ids: JSON.stringify(that.data.ids),
            },
            method: "POST",
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code != 1) {
                    app.alert({'content': res.data.msg})
                    return;
                }
                console.log(res.data.msg);
                console.log(res.data.data);
                that.setData({
                    goods_list: res.data.data.goods_list,
                    default_address: res.data.data.default_address,
                    address_id: res.data.data.default_address.id,
                    yun_price: res.data.data.yun_price,
                    pay_price: res.data.data.pay_price,
                    total_price: res.data.data.total_price,
                });
            }
        })
    },
    getOrderInfo1: function () {
        var that = this;
        wx.request({
            url: app.buildUrl('/v1/order/info1'),//仅为实例
            data: {
                id:that.data.fid,
                num:that.data.num
            },
            method: "POST",
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code != 1) {
                    app.alert({'content': res.data.msg})
                    return;
                }
                console.log(res.data.msg);
                console.log(res.data.data);
                that.setData({
                    goods_list: res.data.data.goods_list,
                    default_address: res.data.data.default_address,
                    address_id: res.data.data.default_address.id,
                    yun_price: res.data.data.yun_price,
                    pay_price: res.data.data.pay_price,
                    total_price: res.data.data.total_price,
                });
            }
        })
    },

});





