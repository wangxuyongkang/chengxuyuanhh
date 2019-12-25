// pages/image/demo1/index.js
Page({
    data: {
        // page:1,
        // imgList: [
        //     {
        //         url: 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=1262379643,2889266243&fm=26&gp=0.jpg',
        //         text: '皎月女神 - 戴安娜',
        //         id: 1
        //     }, {
        //         url: 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=2024970122,1259443147&fm=26&gp=0.jpg',
        //         text: '武器大师 - 贾克斯',
        //         id: 2
        //     },
        //     {
        //         url: 'https://ss0.bdstatic.com/70cFuHSh_Q1YnxGkpoWK1HF6hhy/it/u=8017613,3291049031&fm=26&gp=0.jpg',
        //         text: '卡牌大师 - 崔斯特',
        //         id: 3
        //     }, {
        //         url: 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=3817800566,1997481956&fm=26&gp=0.jpg',
        //         text: '冰霜女巫 - 丽桑卓',
        //         id: 4
        //     },
        //     {
        //         url: 'https://ss3.bdstatic.com/70cFv8Sh_Q1YnxGkpoWK1HF6hhy/it/u=148559742,3105355281&fm=26&gp=0.jpg',
        //         text: '法外狂徒 - 格雷福斯',
        //         id: 5
        //     },
        //     {
        //         url: 'https://ss0.bdstatic.com/70cFvHSh_Q1YnxGkpoWK1HF6hhy/it/u=2205289034,170799742&fm=26&gp=0.jpg',
        //         text: '不祥之刃 - 卡特琳娜',
        //         id: 6
        //     },
        // ],
        loadingMoreHidden: true,
        page:1,
        imgList:[]

    },
    onLoad: function (options) {
        // 页面初始化 options为页面跳转所带来的参数
        this.getcatrall()
    },
    onReady: function () {
        // 页面渲染完成
    },
    onShow: function () {
        // 页面显示
    },
    onHide: function () {
        // 页面隐藏
    },
    onReachBottom:function () {
        var that = this
        console.log('该加载数据了')
       that.setData({
           page: that.data.page + 1,
                })
       this.getcatrall()
        //加载更多
    },
    onUnload: function () {
        // 页面关闭
    },
    getcatrall:function () {
    var that=this;
        console.log(that.data)// 发起网络请求
        wx.request({
            url: 'http://127.0.0.1:5000/hero',
            data: {
                'page':that.data.page
            },
            method: 'GET',
            success(res) {

                if (res.data.code == 0) {
                    app.alter({'content': data.msg});
                    return;
                }
                that.setData({
                    loadingMoreHidden: false,
                    imgList:that.data.imgList.concat(res.data.data.lists),
                })

                }
            })
        },


})