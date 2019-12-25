<template>
  <div class="my_nala_centre ilizi_centre">
    <div class="ilizi cle">
      <div class="box">
        <div class="box_1">
          <div class="userCenterBox boxCenterList clearfix" style="_height:1%;">
            <h5><span>收货人信息</span></h5>
            <div class="blank"></div>
            <!-- 收货信息 -->
            <table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd" v-for="(item,index) in receiveInfoArr" :key="index">
              <tbody>
                <tr>
                  <td align="right" bgcolor="#ffffff">配送区域：</td>
                  <td colspan="3" align="left" bgcolor="#ffffff">
                    <div class="addr" @click="bubble(index)">
                      <!-- 三级级联菜单 -->
                      <v-distpicker :province="item.province" :city="item.city" :area="item.district" @selected="onSelected"></v-distpicker>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td align="right" bgcolor="#ffffff">收货人姓名：</td>
                  <td align="left" bgcolor="#ffffff"><input name="consignee" type="text" class="inputBg" v-model="item.signer_name">
                    <span :class="{error: item.signer_name==''}">(必填)</span>
                  </td>
                </tr>
                <tr>
                  <td align="right" bgcolor="#ffffff">详细地址：</td>
                  <td align="left" bgcolor="#ffffff"><input name="address" type="text" class="inputBg" v-model="item.address">
                    <span :class="{error: item.address==''}">(必填)</span></td>
                </tr>
                <tr>
                  <td align="right" bgcolor="#ffffff">手机：</td>
                  <td align="left" bgcolor="#ffffff"><input name="mobile" type="text" class="inputBg" v-model="item.signer_mobile">
                    <span :class="{error: item.signer_mobile==''}">(必填)</span></td>
                </tr>
                <tr>
                  <td align="right" bgcolor="#ffffff">&nbsp;</td>
                  <td colspan="3" align="center" bgcolor="#ffffff">
                    <button class="bnt_blue_2" @click="confirmUpdate(item.id, index)">确定修改</button>
                    <button class="bnt_blue_2" @click="deleteInfo(item.id)">删除</button>
                    <!-- <input type="hidden" name="act" value="act_edit_address">
                    <input name="address_id" type="hidden" value="320"> -->
                  </td>
                </tr>
              </tbody>
            </table>

            <!-- 新增收货地址 -->
            <table width="100%" border="0" cellpadding="5" cellspacing="1" bgcolor="#dddddd">
              <tbody>
                <tr>
                  <td align="right" bgcolor="#ffffff">配送区域：</td>
                  <td colspan="3" align="left" bgcolor="#ffffff">
                    <div class="addr">
                      <!-- 三级级联菜单 -->
                      <v-distpicker :province="newInfo.province" :city="newInfo.city" :area="newInfo.district" @selected="getSelected"></v-distpicker>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td align="right" bgcolor="#ffffff">收货人姓名：</td>
                  <td align="left" bgcolor="#ffffff"><input name="consignee" type="text" class="inputBg" v-model="newInfo.signer_name">
                    <span :class="{error: newInfo.signer_name==''}">(必填)</span>
                  </td>
                </tr>
                <tr>
                  <td align="right" bgcolor="#ffffff">详细地址：</td>
                  <td align="left" bgcolor="#ffffff"><input name="address" type="text" class="inputBg" v-model="newInfo.address">
                    <span :class="{error: newInfo.address==''}">(必填)</span>
                  </td>
                </tr>
                <tr>
                  <td align="right" bgcolor="#ffffff">手机：</td>
                  <td align="left" bgcolor="#ffffff"><input name="mobile" type="text" class="inputBg" v-model="newInfo.signer_mobile">
                    <span :class="{error: newInfo.signer_mobile==''}">(必填)</span></td>
                </tr>
                <tr>
                  <td align="right" bgcolor="#ffffff">&nbsp;</td>
                  <td colspan="3" align="center" bgcolor="#ffffff">
                    <button class="bnt_blue_2" @click="addReceive">新增收货地址</button>

                    <!-- <input type="hidden" name="act" value="act_edit_address">
                    <input name="address_id" type="hidden" value="320"> -->
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

  </div>

</template>

<script>
import VDistpicker from 'v-distpicker'
import {getAddress, updateAddress, delAddress, addAddress} from '../../api/api'

export default {
  data () {
    return {
      receiveInfoArr: [],
      currentIndex: -1,
      newInfo: {
        province: '', // 省
        city: '', // 市
        district: '', // 区
        signer_name: '', // 收件人姓名
        signer_mobile: '', // 电话
        address: '' // 详细地址
      },
      newInfoEmpty: {
        province: '', // 省
        city: '', // 市
        district: '', // 区
        signer_name: '', // 收件人姓名
        signer_mobile: '', // 电话
        address: '' // 详细地址
      }
    }
  },
  components: {
    VDistpicker
  },
  created () {
    this.getReceiveInfo()
  },
  methods: {
    getReceiveInfo () { // 获取收件人信息
      getAddress().then(response => {
        // console.log(response.data)
        this.receiveInfoArr = response.data
      }).catch(error => {
        console.log(error)
      })
    },
    onSelected (data) {
      // alert(data.province + ' | ' + data.city + ' | ' + data.area)
      // console.log(data)
      let ri = this.receiveInfoArr[this.currentIndex]
      ri.province = data.province.value
      ri.city = data.city.value
      ri.district = data.area.value
    },
    bubble (index) {
      this.currentIndex = index
    },
    confirmUpdate (id, index) { // 更新收货信息
      updateAddress(id, this.receiveInfoArr[index]).then(response => {
        // console.log(response.data)
        alert('修改成功')
        this.getReceiveInfo()
      }).catch(error => {
        console.log(error)
      })
    },
    deleteInfo (id) { // 删除收货人信息
      delAddress(id).then(response => {
        // console.log(response.data)
        alert('删除成功')
        this.getReceiveInfo()
      }).catch(error => {
        console.log(error)
      })
    },
    getSelected (data) {
      // alert(data.province + ' | ' + data.city + ' | ' + data.area)
      // console.log(data)
      this.newInfo.province = data.province.value
      this.newInfo.city = data.city.value
      this.newInfo.district = data.area.value
    },
    addReceive () { // 提交收货信息
      // 表单验证略
      addAddress(this.newInfo).then(response => {
        // console.log(response.data)
        alert('添加成功')
        // 重置新的
        this.getReceiveInfo()
        Object.assign(this.newInfo, this.newInfoEmpty)
      }).catch(error => {
        console.log(error)
      })
    }
  }
}
</script>

<style scoped>
.error{
  color:#fa8341;
}
table {
    margin-bottom: 20px;
}
select {
    min-width: 80px;
}

.my_nala_main h3.my_nala {
    height:60px;
    border:1px solid #e7e7e7;
    border-bottom:0
}
.my_nala_main h3.my_nala a {
    display:block;
    height:60px;
    font-size:22px;
    text-align:center;
    line-height:60px;
    overflow:hidden
}
.my_nala_main h3.my_nala a:hover {
    text-decoration:none
}

.my_nala_centre {
    float:right;
    width:970px;
    background-color:#fff
}
.my_nala_centre .trade_mod .h301 a.more {
    font-size:14px;
    color:#666;
    font-weight:normal
}
.my_nala_centre .trade_mod .h301 a.more:hover {
    color:#09c762
}
.my_nala_centre .something_interesting {
    margin-top:10px
}
.my_nala_centre .something_interesting ul {
    margin-left:20px
}
.my_nala_centre .something_interesting li {
    width:130px;
    text-align:center;
    float:left
}
.my_nala_centre .something_interesting b {
    font-weight:normal
}
.my_nala_centre .something_interesting em {
    font-size:12px;
    font-weight:bold;
    color:#09c762
}
.my_nala_centre .relate_goods {
    border:1px solid #e4e4e4;
    border-top:0
}
.my_nala_centre .pagenav {
    padding:15px 10px;
    border-top:1px solid #e4e4e4
}

.ilizi_centre {
    background:0
}

.ilizi {
    border:1px solid #e4e4e4;
    padding:16px 18px;
    margin-bottom:10px;
    background:#fff
}
.ilizi .face,.iface .face {
    display:block;
    float:left;
    width:100px;
    height:100px;
    position:relative
}
.ilizi .edit_face,.iface .edit_face {
    position:absolute;
    height:20px;
    line-height:20px;
    width:100px;
    display:block;
    background:rgba(0,0,0,0.5);
    text-align:center;
    color:#fff;
    left:1px;
    bottom:-1px;
    _bottom:0;
    filter:progid:DXImageTransform.Microsoft.gradient(enabled=true,startColorstr='#77000000',endColorstr='#77000000');
    visibility:hidden;
    margin:0
}
.ilizi .face img,.iface .face img {
    width:100px;
    height:100px;
    border:1px solid #e4e4e4
}
.ilizi .ilizi_info {
    width:800px;
    float:right;
    height:100px
}
.bnt_blue_1,.bnt_blue,.bnt_bonus,.bnt_blue_2 {
    display:inline-block;
    padding:4px 12px;
    height:24px;
    line-height:16px;
    _line-height:18px;
    border:1px solid #1e9246;
    border-radius:3px;
    font-size:100%;
    color:#fff;
    background-color:#09c762;
    overflow:hidden;
    vertical-align:middle;
    cursor:pointer
}

    .addr .address {
        height: 35px;
    }
    .addr .address select{
        height: inherit;
        font-size: inherit;
        border-radius: initial;
        width: 130px;
        padding:0
    }
.userCenterBox table td{
    padding: 5px;
}
</style>
