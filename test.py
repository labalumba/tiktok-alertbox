from TikTokLive import TikTokLiveClient as ttcl
from TikTokLive.types.events import CommentEvent, ConnectEvent, GiftEvent, ShareEvent, LikeEvent, FollowEvent, ViewerCountUpdateEvent
import tkinter as tkr
import pyglet

tiktokid="kekeckenan.live"

def alerbox(id,gift_type,count):
    animation = pyglet.image.load_animation('giphy.gif')
    animSprite = pyglet.sprite.Sprite(animation)
    
    w = animSprite.width
    h = animSprite.height
    
    window = pyglet.window.Window(width=w, height=h,style=pyglet.window.Window.WINDOW_STYLE_BORDERLESS)
    
    r,g,b,alpha = 0.5,0.5,0.8,0.5, 
    pyglet.gl.glClearColor(r,g,b,alpha)

    label1= pyglet.text.Label(str(id)+ ' az önce ' + str(count) + ' adet ' + str(gift_type) +' yolladı!',
                            font_name='Open Sans',
                            font_size=36,
                            bold=True,
                            x=window.width//2, y=window.height//2+60,
                            anchor_x='center', anchor_y='bottom')
    

    label = pyglet.text.Label(id+ ' Seni çok seviyorum!',
                            font_name='Open Sans',
                            font_size=36,
                            bold=True,
                            x=window.width//2, y=window.height//2,
                            anchor_x='center', anchor_y='bottom')
    
    @window.event
    def on_draw():

        window.clear()
        animSprite.draw()
        label.draw()
        label1.draw()
        
    def close(event):
        window.close()

    pyglet.clock.schedule_once(close, 4.0)

    pyglet.app.run()


client: ttcl =ttcl(
    unique_id=tiktokid,**({
        "enable_extended_gift_info":True
    })

)

def gift_alert(gifter, gift_type, count=1):
    print(gifter+"çok iyi biri")
    alerbox(gifter,gift_type,count)

@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID", client.room_id)

#@client.on("comment")
#async def on_connect(event: CommentEvent):
#    print(f"{event.user.uniqueId} -> {event.comment} ")

@client.on("gift")
async def on_gift(event: GiftEvent):
    # If it's type 1 and the streak is over
    if event.gift.gift_type == 1 and event.gift.repeat_end == 1:
        print(f"{event.user.uniqueId} sent {event.gift.repeat_count}x \"{event.gift.extended_gift.name}\"")
        gift_alert(event.user.uniqueId,event.gift.extended_gift.name,event.gift.repeat_count)

    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.gift_type != 1:
        print(f"{event.user.uniqueId} sent \"{event.gift.extended_gift.name}\"")
        gift_alert(event.user.uniqueId,event.gift.extended_gift.name)
    
    

#@client.on("like")
#async def on_like(_: LikeEvent):
#    print(f"{event.user.uniqueId} has liked the stream {event.likeCount} times, there is now {event.totalLikeCount} total likes!  ")



if __name__ == '__main__':
    client.run()



 
