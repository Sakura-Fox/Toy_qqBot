# Personal qqBot Toy

#### 这是什么？

基于高性能机器人开发框架 [Mirai](https://github.com/mamoe/mirai) 的 Python 接口 [Python-mirai](https://github.com/GreyElaina/python-mirai) 开发的应用程序，使用 [face_recognition](https://github.com/ageitgey/face_recognition) 库实现对群消息图片中的人脸识别功能。

#### 开始使用

##### 获取依赖：[mirai-console](https://github.com/mamoe/mirai-console), [python-mirai](https://github.com/GreyElaina/python-mirai), [face_recognition](https://github.com/ageitgey/face_recognition)

由于 `python-mirai` 依赖于 `mirai` 提供的 `mirai-http-api` 插件, 所以你需要先运行一个 `mirai-core` 或是 `mirai-console` 实例以支撑你的应用运行.

在 `mirai-console` 处 login 你的qq机器人，根据 mirai-console 的 setting.yml 配置 `bot.py` 中的字段，在安装所有依赖后，运行`bot.py`.

你需要在当前目录下创建三个文件夹 `known_faces`(存储已知的人脸图片), `mirai_imgs`(存储从群消息中下载的图片), `res_imgs`(存储标记好的人脸图片). 

`known_faces` 中的人脸图片由你自己添加，当机器人在一条消息内被@并收到正确的命令与图片时，会下载图片至 `mirai_imgs`，与 `known_faces` 中的人脸比对，将结果放入 `res_imgs` 并发出.

添加人脸图片至`known_faces`后，建议运行 `judge_face.py` 以保证所有图片都可识别出人脸。

#### 欢迎贡献

欢迎一切形式上的贡献(包括但不限于 `Issues`, `Pull Requests`, `Good Idea` 等)

#### 鸣谢

- [`mirai`](https://github.com/mamoe/mirai): 即 `mirai-core`, 一个高性能, 高可扩展性的 QQ 协议库, 同时也是个很棒的机器人开发框架!
- [`mirai-console`](https://github.com/mamoe/mirai-console): 一个基于 `mirai` 开发的插件式可扩展开发平台, 极大地降低了我的学习成本。
- [`python-mirai`](https://github.com/GreyElaina/python-mirai):  `mirai`的python接口，很适合用来入门。
- [`face_recognition`](https://github.com/ageitgey/face_recognition):  很好用的人脸识别库。

#### 许可证

​	使用[`GNU AGPLv3`](https://choosealicense.com/licenses/agpl-3.0/) 作为本项目的开源许可证,  因为原项目 [`python-mirai`](https://github.com/GreyElaina/python-mirai) 同样使用了 `GNU AGPLv3` 作为开源许可证, 因此你在使用时需要遵守相应的规则.

