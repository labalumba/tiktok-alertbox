
from TikTokLive import TikTokLiveClient as ttcl
from TikTokLive.types.events import  ConnectEvent, GiftEvent, ShareEvent, LikeEvent, FollowEvent, ViewerCountUpdateEvent
import asyncio

tiktokid="memo.live"

gifter_que=[]
playing_animation=False
flag=False


def gift_alert(user_id,gift_type,gift_amount):

    print (len(gifter_que))
    print("playing animation for " + user_id)
    
    text1 = '''   
    <html>
        <body>
        <div id="main">
        <div id="toRemove">
            <h1>{} {} adet {} yolladı </h1>
            <img src="mygif.gif" width="250" />
        </div>
        </div>


        </body>
    </html>'''.format(user_id,gift_amount,gift_type)
    text2='''
    <script>
    function reload(){
    location.href=location.href
    }
    setInterval('reload()',3000)
    </script>
    <script>
    const para = document.createElement("p");
    const node = document.createTextNode("This is new.");
    para.appendChild(node);
    const element = document.getElementById("div1");
    element.appendChild(para);
    </script>

    '''
       
    file = open("sample.html","w")
    file.write(text1+text2)
    file.close()

    

async def all_gifters():
    if len(gifter_que)==0:
            text1='''<script>
        function reload(){
        location.href=location.href
        }
        setInterval('reload()',3000)
        </script>
            
            '''
            text2=''
            file = open("sample.html","w")
            file.write(text1+text2)
            file.close()
    
    while len(gifter_que)!=0:
        gift_alert(gifter_que[0][0],gifter_que[0][1],gifter_que[0][2])
        gifter_que.pop(0)
        print("popping")
        await asyncio.sleep(3)
        if len(gifter_que)==0:
            text1='''<script>
        function reload(){
        location.href=location.href
        }
        setInterval('reload()',3000)
        </script>
            
            '''
            text2=''
            file = open("sample.html","w")
            file.write(text1+text2)
            file.close()
        return False
    


async def queuer():
    global flag
    if flag:
        return
    else:
        flag=True
        flag=await all_gifters()

        


        






client: ttcl =ttcl(
    unique_id=tiktokid,**({
        "enable_extended_gift_info":True
    })

)







@client.on("connect")
async def on_connect(_: ConnectEvent):
    print("Connected to Room ID", client.room_id)
    print(gifter_que)
    await all_gifters()


@client.on("gift")
async def on_gift(event: GiftEvent):
    
    # If it's type 1 and the streak is over
    if event.gift.gift_type == 1 and event.gift.repeat_end == 1:
        gifter_tuple=()
        gifter_tuple=(event.user.uniqueId, event.gift.extended_gift.name, event.gift.repeat_count)
        gifter_que.append(gifter_tuple)
        print(gifter_que)
        await queuer()

    # It's not type 1, which means it can't have a streak & is automatically over
    elif event.gift.gift_type != 1:
        gifter_tuple=()
        gifter_tuple=(event.user.uniqueId, event.gift.extended_gift.name,'1')
        gifter_que.append(gifter_tuple)
        print(gifter_que)
        await queuer()
    
    


if __name__ == '__main__':
    client.run()



