<template>
  <div>
    <footer class="footer" style="margin-top:30px;">
      <div class="footerK">
        <div class="pageNav" >
          <!-- 页码 -->
          <span @click="pageCallback(page.page)" v-for="(page,index) in apages" :key="index" class="page" :class="[page.active?'cPageNum':'pageNum']">{{page.text}}</span>
        </div>
      </div>
    </footer>
  </div>

</template>

<script>
export default {
  props: {
    preText: {
      type: String,
      default: '上一页'
    },
    nextText: {
      type: String,
      default: '下一页'
    },
    endShow: {
      type: String,
      default: 'false'
    },
    page: [String, Number],
    totalPage: [String, Number]
  },
  computed: {
    apages: function () {
      return this.nav(parseInt(this.page), parseInt(this.totalPage))
    }
  },
  methods: {
    nav: function (a, b) { // 当前页, 总页数
      var c = [] // 最终要遍历的数组
      if (b <= 1) {
        return []
      }
      b < a && (a = b)
      if (a <= 1) {
        a = 1
      } else {
        c.push({page: a - 1, text: this.preText})
        c.push({page: 1, text: '1'})
      }
      var d = 2
      var e = b < 9 ? b : 9
      if (a >= 7) {
        c.push({page: '', text: '...'})
        d = a - 4
        e = a + 4
        e = b < e ? b : e
      }
      for (; d < a; d++) c.push({page: d, text: d})
      c.push({page: a, text: a, active: true})
      for (d = a + 1; d <= e; d++)c.push({page: d, text: d})
      if (this.endShow === 'true') {
        if (e < b) {
          c.push({page: b, text: '...'})
          c.push({page: b, text: b})
        }
      }
      a < b && (c.push({page: a + 1, text: this.nextText}))
      return c
    },
    pageCallback: function (page) {
      this.$emit('pagefn', {page: page, totalPage: this.totalPage})
    }
  }
}
</script>

<style scoped>
footer {
  width: 100%;
  height: 60px;
  float: left;
}
.footerK {
  height: 100%;
  margin: 0px auto;
  line-height: 60px;
  text-align: right;
  position: relative;
}
.page{
  border: 1px solid #ddd;
  padding: 8px 12px;
  margin-left: 10px;
  text-align: center;
  cursor:pointer;
}
.page:hover{
  color:#09c762;
  border-color:#09c762;
}
.footerK a,
.cPageNum {
  line-height: 35px;
  font-size: 12px;

  color: #939393;
  border: none;
  tencursor: pointer;
}
.cPageNum {
  color: #333333;
  font-weight: bold;

}
.footerK a:hover {
  color: #fff;
  background: #68a0fc;
}
</style>
