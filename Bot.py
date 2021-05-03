from mirai import (
    Mirai, Plain, MessageChain, Friend, Group, Member,
    FriendMessage,GroupMessage, Image, At,
    MemberJoinEvent, BotJoinGroupEvent
)
import asyncio
from typing import List
import utility,recg_face,Account


app = Mirai(f"mirai://{Account.mirai_api_http_locate}?authKey={Account.authKey}&qq={Account.qq}")

@app.receiver("FriendMessage")
async def event_gm(app: Mirai, friend: Friend, message: MessageChain):
    if friend.id == Account.admin:
        aplain: Plain = message.getFirstComponent(Plain)
        atext = aplain.text
        if atext == "save image":
            aimage: Image = message.getFirstComponent(Image)
            if aimage is not None:
                utility.download_imgae2(aimage.url,"Downloads/Images")
                await app.sendFriendMessage(
                    friend,
                    [Plain(text = "已存储")]
                )
        else:
            await app.sendFriendMessage(
                    friend,
                    [Plain(text = "Greetings!")]
                )

@app.receiver("MemberJoinEvent")
async def member_join(app: Mirai, event: MemberJoinEvent):
    await app.sendGroupMessage(
        event.member.group.id,
        [
            At(target=event.member.id),
            Plain(text="欢迎欢迎!")
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
        if aat.target == Account.qq:
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