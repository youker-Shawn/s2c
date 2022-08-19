// index.js
Page({
    data: {
        username: "",
        inviteCode: "",
    },
    onLoad: function(options) {
        // 进入首页加载页面时，记录邀请码
        this.data.inviteCode = options.inviteCode
    },
    submit: function() {
        console.log(this.data.username, this.data.inviteCode)
        wx.request({
            url: 'http://127.0.0.1:8000/accounts/register/',  // 上线后替换为后端服务地址
            method: "POST",
            data: {
              username: this.data.username,
              invite: this.data.inviteCode,
            //   invite: "cf00df93461140368ffc2cfe1107d32e", // 调试用
            },
            header: {
              'content-type': 'application/json' // 默认值
            },
            success (res) {
              console.log(res.data)
            },
            fail (err) {
              console.log(err)
            }    
          })
    }
})
