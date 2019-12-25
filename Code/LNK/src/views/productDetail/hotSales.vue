<template>
  <div class="z-detail-right">
          <div class="tabs_bar_right">
            <div class="tabs_bar2">热卖商品</div>
          </div>
          <div class="hot_box">
            <ul>
              <!-- 商品 -->
              <li>
                <a href="productDetail.html">
                  <img width="194px" height="194px" src="../../../static/images/goods/images/24_P_1448948023823.jpg">
                  <p>有机黑米</p>
                  <p class="hot_price">￥9元</p>
                </a>
              </li>
              <li>
                <a href="productDetail.html">
                  <img width="194px" height="194px" src="../../../static/images/goods/images/25_P_1448947875346.jpg">
                  <p>非转基因橄榄大豆油</p>
                  <p class="hot_price">￥92元</p>
                </a>
              </li>
              <li>
                <a href="productDetail.html">
                  <img width="194px" height="194px" src="../../../static/images/goods/images/37_P_1448949284365.jpg">
                  <p>旺儿佳全脂乳粉</p>
                  <p class="hot_price">￥162元</p>
                </a>
              </li>
            </ul>
          </div>
        </div>
</template>

<script>

</script>

<style scoped>
html {
    background:#fafafa;
    color:#333;
    _background-attachment:fixed
}

body,p,ul,ol,li {
    margin:0;
    padding:0
}
body{
    font:12px/1.5 "Microsoft YaHei",Tahoma,Helvetica,Arial,simsun
}

ul,ol {
    list-style:none
}
img {
    border:0
}

input{
    font-size:12px;
    outline:0;
    resize:none;
    color:#333
}
button {
    cursor:pointer
}

.clear {
    clear:both;
    height:0;
    font-size:0;
    line-height:0;
    overflow:hidden
}
.cle:after {
    visibility:hidden;
    display:block;
    font-size:0;
    content:'\20';
    clear:both;
    height:0
}
.cle{
    *zoom:1
}
.fl {
    float:left
}
.fr {
    float:right
}
a {
    text-decoration:none;
    color:#333;
    -webkit-transition:color .2s;
    -moz-transition:color .2s;
    -o-transition:color .2s;
    -ms-transition:color .2s;
    transition:color .2s
}
a:hover {
    color:#09c762
}
a:focus,area:focus {
    outline:0
}
::selection {
    background:#09c762;
    color:#fff
}
canvas {
    -ms-touch-action:double-tap-zoom
}


.z-detail-right {
    width:216px;
    float:right
}
.tabs_bar_right {
    height:50px;
    width:216px;
}
.tabs_bar2 {
    height:48px;
    background:#f3f3f3;
    border:1px solid #ccc;
    padding:0 35px;
    display:block;
    line-height:48px;
    text-align:center;
}

.hot_box {
    padding:10px;
    border:1px solid #ccc;
    border-top:0;
}
.hot_box ul li {
    margin-bottom:10px;
}
p.hot_price {
    color:#09c762;
    font-weight:bold;
    font-size:14px;
    line-height:24px;
}
</style>
