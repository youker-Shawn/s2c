调试demo步骤：
(使用默认的sqlite)

「启动环境」
- cd s2c/s2cDemo/
- python -m venv venv
- source ./venv/bin/activate
- pip install -r requirements.txt
- python manage.py migrate

「创建超级用户，用于进入后台管理系统」
- python manage.py createsuperuser

「单元测试」
- python manage.py test

「本地启动后端服务」
- python manage.py runserver


「小程序端」

暂时用开发者工具模拟器调试。可以将POST时的invite参数替换为前面的超级管理员的invite即可。


「在线调试」
- 小程序发布体验版，生成带指定邀请码的二维码，提供扫描进入小程序。
- 后端部署需要服务到服务器，暴露接口给公网。供小程序发起请求。
