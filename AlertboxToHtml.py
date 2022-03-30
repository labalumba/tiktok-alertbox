from TikTokLive import TikTokLiveClient as ttcl
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent, ShareEvent, LikeEvent, FollowEvent, ViewerCountUpdateEvent
import sched, time



tiktokid="ytlosman"

gifter_que=[]


client: ttcl =ttcl(
    unique_id=tiktokid,**({
        "enable_extended_gift_info":True
    })

)

@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID", client.room_id)
    print(gifter_que)

@client.on("gift")
async def on_gift(event: GiftEvent):
    
    # If it's type 1 and the streak is over
    if event.gift.gift_type == 1 and event.gift.repeat_end == 1:
        gifter_tuple=()
        gifter_tuple=(event.user.uniqueId, event.gift.extended_gift.name, event.gift.repeat_count)
        gifter_que.append(gifter_tuple)


    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.gift_type != 1:
        gifter_tuple=()
        gifter_tuple=(event.user.uniqueId, event.gift.extended_gift.name)
        gifter_que.append(gifter_tuple)

    

if __name__ == '__main__':
    client.run()


