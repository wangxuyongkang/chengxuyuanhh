//index.js
//获取应用实例
var app = getApp();
Page({
    data: {
        indicatorDots: true,
        autoplay: true,
        interval: 3000,
        duration: 1000,
        loadingHidden: false, // loading
        swiperCurrent: 0,
        categories: [],
        activeCategoryId: 0,
        goods: [],
        scrollTop: "0",
        loadingMoreHidden: true,
        searchInput: '',
        banners: [],
        p: 1,
        isloading: false,
    },
    onLoad: function () {
        var that = this;

        wx.setNavigationBarTitle({
            title: app.globalData.shopName
        });

        this.getBannersAndCategories()
        this.getGoods()
    },
    scroll: function (e) {
        var that = this, scrollTop = that.data.scrollTop;
        that.setData({
            scrollTop: e.detail.scrollTop
        });
    },
    //事件处理函数
    swiperchange: function (e) {
        this.setData({
            swiperCurrent: e.detail.current
        })
    },
    listenerSearchInput: function (e) {
        this.setData({
            searchInput: e.detail.value
        });
    },
    toSearch: function (e) {
        this.setData({
            p: 1,
            goods: [],
            loadingMoreHidden: true
        });
        this.getFoodList();
    },
    tapBanner: function (e) {
        if (e.currentTarget.dataset.id != 0) {
            wx.navigateTo({
                url: "/pages/food/info?id=" + e.currentTarget.dataset.id
            });
        }
    },
    toDetailsTap: function (e) {
        console.log(e)
        wx.navigateTo({
            url: "/pages/food/info?id=" + e.currentTarget.dataset.id
        });
    },

    onReachBottom: function () {
            if (this.data.isloading == false) {
                this.setData({
                    p: this.data.p + 1
                });
                this.getGoods()

            }

    },

    catclick: function (e) {
        this.setData({
            activeCategoryId: e.target.id,
            p: 1,
            goods: [],
            loadingMoreHidden: true,
        })
        //点击分类的时候发起请求
        this.getGoods()
    },

    getBannersAndCategories: function () {
        var that = this
        wx.request({
            url: app.buildUrl('/v1/food/search'),
            method: 'GET',
            header: app.getRequestHeader(),
            success(res) {
                if (res.data.code == 1) {
                    that.setData({
                        banners: res.data.data.banners,
                        categories: res.data.data.categories
                    })
                }
            }
        })

    },
    getGoods: function () {
        var that = this

        if (that.data.isloading == true) {
            return;
        }

        that.setData({
            isloading: true
        })

        wx.request({
            url: app.buildUrl('/v1/food/all'),

            method: 'GET',
            data: {
                'category_id': that.data.activeCategoryId,
                'p': that.data.p
            },
            header: app.getRequestHeader(),
            success(res) {
                var data = res.data
                if (data.code != 1) {
                    app.alert({'content': data.msg})
                    return;
                }
                that.setData({
                    goods: that.data.goods.concat(data.data.goods),
                    isloading: false
                })

                if (data.data.has_more == 0) {
                    that.setData({
                        loadingMoreHidden: false,
                    })
                }
            }
        })

    }
});
