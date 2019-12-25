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
    }