from mirai import (
    Mirai, Plain, MessageChain, Friend, Group, Member,
    FriendMessage,GroupMessage, Image, At,
    MemberJoinEvent, BotJoinGroupEvent
)
import asyncio
from typing import List
import utility,recg_face
qq = 123456 # 字段 qq 的值
authKey = 'graia-mirai-api-http-authkey' # 字段 authKey 的值
mirai_api_http_locate = 'localhost:8080/ws' # httpapi所在主机的地址端口,如果 setting.yml 文件里字段 "enableWebsocket" 的值为 "true" 则需要将 "/" 换成 "/ws", 否则将接收不到消息.

app = Mirai(f"mirai://{mirai_api_http_locate}?authKey={authKey}&qq={qq}")

@app.receiver("FriendMessage")
async def event_gm(app: Mirai, friend: Friend):
    await app.sendFriendMessage(friend, [
        Plain(text="Hello, world!")
    ])
@app.receiver("MemberJoinEvent")
async def member_join(app: Mirai, event: MemberJoinEvent):
    await app.sendGroupMessage(
        event.member.group.id,
        [
            At(target=event.member.id),
            Plain(text="欢迎进群!")
        ]
    )
# @app.receiver("BotJoinGroupEvent") #不知为和这个annotation用不了
# async def bot_join(app:Mirai, group: Group):
#     await app.sendGroupMessage(
#         group.id,
#         [Plain(text = "大家好，我是兔兔伯爵，叫我兔兔就好，初来乍到，还请大家观照～")]
#     )
@app.receiver("GroupMessage")
async def GMHandler(app: Mirai, group: Group, message: MessageChain):
    aat: At = message.getFirstComponent(At)
    replyFlag = 0
    if aat is not None:
        if aat.target == qq:
            aplain: Plain = message.getFirstComponent(Plain)
            replyFlag = 1
            if aplain is None:
                plainToSend = Plain(text = "还没有输入指令哦")
            else:
                atext = aplain.text
                if "谁" in atext:
                    aimage: Image = message.getFirstComponent(Image)
                    if aimage is None:
                        plainToSend = Plain(text = "没有收到图片呢，请在@我的同时发送图片") 
                    else:
                        replyFlag = 2
                        utility.download_imgae(aimage.url)
                        recg_face.recognize_face()
                else:
                    plainToSend = Plain(text = "兔兔目前还不会这个指令哟") 
    if replyFlag == 1:
        await app.sendGroupMessage(
            group.id, 
            [
                plainToSend
            ]
        )
    elif replyFlag == 2:
        if recg_face.recg_res:
            plainToSend = [Plain(text = f"兔兔找到了{len(recg_face.reslist)}个人")]
            if len(recg_face.reslist)>1:
                plainToSend.append(Plain(text = "分别"))
            plainToSend.append(Plain(text="是:\n"))
            for name in recg_face.reslist:
                plainToSend.append(Plain(text = f"{name} "))
            imageToSend = Image.fromFileSystem(f"{recg_face.res_face_path}/{recg_face.image_cnt}.jpg")
            await app.sendGroupMessage(
                group.id,
                plainToSend
            )
            await app.sendGroupMessage(
                group.id,
                [imageToSend]
            )
        else:
            plainToSend = Plain(text = "兔兔没有找到人脸欸，换张照片试试吧")
            await app.sendGroupMessage(
            group.id, 
            [
                plainToSend
            ]
        )
if __name__ == "__main__":
    app.run()