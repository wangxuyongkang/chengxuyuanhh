//获取应用实例
var commonCityData = require('../../utils/city.js');
var app = getApp();
Page({
    data: {
        provinces: [],
        citys: [],
        districts: [],
        selProvince: '请选择',
        selCity: '请选择',
        selDistrict: '请选择',
        selProvinceIndex: 0,
        selCityIndex: 0,
        selDistrictIndex: 0
    },
    onLoad: function (e) {
        var that = this;
        this.initCityData(1);
    },
    //初始化城市数据
    initCityData: function (level, obj) {
        if (level == 1) {
            var pinkArray = [];
            for (var i = 0; i < commonCityData.cityData.length; i++) {
                pinkArray.push(commonCityData.cityData[i].name);
            }
            this.setData({
                provinces: pinkArray
            });
        } else if (level == 2) {
            var pinkArray = [];
            var dataArray = obj.cityList
            for (var i = 0; i < dataArray.length; i++) {
                pinkArray.push(dataArray[i].name);
            }
            this.setData({
                citys: pinkArray
            });
        } else if (level == 3) {
            var pinkArray = [];
            var dataArray = obj.districtList
            for (var i = 0; i < dataArray.length; i++) {
                pinkArray.push(dataArray[i].name);
            }
            this.setData({
                districts: pinkArray
            });
        }
    },
    bindPickerProvinceChange: function (event) {
        var selIterm = commonCityData.cityData[event.detail.value];
        this.setData({
            selProvince: selIterm.name,
            selProvinceIndex: event.detail.value,
            selCity: '请选择',
            selCityIndex: 0,
            selDistrict: '请选择',
            selDistrictIndex: 0
        });
        this.initCityData(2, selIterm);
    },
    bindPickerCityChange: function (event) {
        var selIterm = commonCityData.cityData[this.data.selProvinceIndex].cityList[event.detail.value];
        this.setData({
            selCity: selIterm.name,
            selCityIndex: event.detail.value,
            selDistrict: '请选择',
            selDistrictIndex: 0
        });
        this.initCityData(3, selIterm);
    },
    bindPickerChange: function (event) {
        var selIterm = commonCityData.cityData[this.data.selProvinceIndex].cityList[this.data.selCityIndex].districtList[event.detail.value];
        if (selIterm && selIterm.name && event.detail.value) {
            this.setData({
                selDistrict: selIterm.name,
                selDistrictIndex: event.detail.value
            })
        }
    },
    bindCancel: function () {
        wx.navigateBack({});
    },
    bindSave: function (e) {
        var that = this
        var nickname = e.detail.value.nickname
        var mobile = e.detail.value.mobile
        var address = e.detail.value.address
        var province_id = commonCityData.cityData[that.data.selProvinceIndex].id
        var city_id = commonCityData.cityData[that.data.selProvinceIndex].cityList[that.data.selCityIndex].id

        var area_id = 0
        if (commonCityData.cityData[that.data.selProvinceIndex].cityList[that.data.selCityIndex].districtList.length != 0) {
            area_id = commonCityData.cityData[that.data.selProvinceIndex].cityList[that.data.selCityIndex].districtList[that.data.selDistrictIndex].id
        }


        var data = {
            'nickname': nickname,
            'mobile': mobile,
            'province_id': province_id,
            'province_str': that.data.selProvince,
            'city_id': city_id,
            'city_str': that.data.selCity,
            'area_id': area_id,
            'area_str': that.data.selDistrict,
            'address': address,
        }

        wx.request({
            url: app.buildUrl('/v1/address/set'),
            method: 'POST',
            data: data,
            header: app.getRequestHeader(),
            success: function (res) {
                var data = res.data
                if (data.code != 1) {
                    app.alert({'content': data.msg})
                    return;
                }

                app.alert({'content': data.msg})
            }

        })
    },
    deleteAddress: function (e) {

    },
});
