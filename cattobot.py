import pymongo
from os import environ
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from datetime import datetime, timedelta, timezone
import urllib.request
from pymongo import MongoClient
import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
import json

# pprint library is used to make the output look more pretty
from pprint import pprint
USER = environ['USER']
PASSWORD = environ['PASSWORD']

connection_string = "mongodb+srv://" + USER + ":" + PASSWORD + "@cluster0.6wv5r.mongodb.net/myFirstDatabase?ssl=true&ssl_cert_reqs=CERT_NONE"
client = pymongo.MongoClient(connection_string)
db = client.cattology
people = db.people


# sekarang lagi make pikuhhh
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_TOKEN = environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']

# Authenticate to Twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# Create API object
api = tweepy.API(auth, wait_on_rate_limit=True)

print("connected to twitter")

class IDPrinter(tweepy.Stream):

    
    def on_connect( self ):
        print("Connection established!!")

    def on_data( self, status ):
        #code to run each time you receive some data (direct message, delete, profile update, status,...)
        
                
        a = json.loads(status)
         
        screen_name = "@"+ a["user"]["screen_name"].lower()
        in_rep = a['in_reply_to_status_id_str']
        status_id = a['id']
        
        
        if in_rep == '1511563188894019585':
            x = people.find_one({ "username" : screen_name })
            
            if x == None:
                print("pass")
            else:
                
                
                title_font = ImageFont.truetype("./asset/Montserrat-Bold.ttf", 35)
                poin_font = ImageFont.truetype("./asset/Montserrat-Bold.ttf", 30)
                sub_font = ImageFont.truetype("./asset/Montserrat-Regular.ttf", 25)
                
                
                
                # Import Image
                my_image = Image.open("./asset/kosongan.jpg")
                image_editable = ImageDraw.Draw(my_image)
                
                #Create variable
                nama = x["name"]
                tanggal = x["date-create"].strftime("%d") + " " +  x["date-create"].strftime("%B") +" "+ x["date-create"].strftime("%Y") 
                username = a["user"]["screen_name"]
                date = 'Join Date: ' + tanggal
                jml = x["poin"]
                poin = str(jml) + " Points"
                
                #draw username
                W, H = (800,850)
                w, h = image_editable.textsize(username, font=title_font)
                h += int(h*0.21)      

                image_editable.text(((W-w)/2, (H-h)/2), username , font=title_font,  fill="#030304")
                
                #draw date join

                W, H = (800,950)
                w, h = image_editable.textsize(date, font=sub_font)

                image_editable.text(((W-w)/2, (H-h)/2), date, font=sub_font, fill="#797a7b")

                #draw poin
                
                W, H = (800,1130)
                w, h = image_editable.textsize(poin, font=title_font)

                image_editable.text(((W-w)/2, (H-h)/2), poin, font=title_font, fill="#030304")


                ############progress bar##############

                

                def drawProgressBar(d, x, y, w, h, progress, bg="#a8a6cd", fg="#524e9c"):
                    # draw background
                    d.ellipse((x+w, y, x+h+w, y+h), fill=bg)
                    d.ellipse((x, y, x+h, y+h), fill=bg)
                    d.rectangle((x+(h/2), y, x+w+(h/2), y+h), fill=bg)

                    # draw progress bar
                    w *= progress
                    d.ellipse((x+w, y, x+h+w, y+h),fill=fg)
                    d.ellipse((x, y, x+h, y+h),fill=fg)
                    d.rectangle((x+(h/2), y, x+w+(h/2), y+h),fill=fg)

                    return d

                progress = jml/100

                # draw the progress bar to given location, width, progress and color
                d = drawProgressBar(image_editable, 80, 600, 630, 10, progress)

                
                #place the avatar
                imgURL = a['user']['profile_image_url_https'].replace("normal", "400x400")
                urllib.request.urlretrieve(imgURL, "./asset/avatar_user.png")

    

                im2 = Image.open("./asset/avatar_user.png")
                im2 = im2.resize((180, 180))


                mask_im = Image.new("L", im2.size, 0)
                draw = ImageDraw.Draw(mask_im)
                draw.ellipse((0, 0, 180, 180), fill=255)
                mask_im.save("./asset/mask_circle.jpg", quality=95)

                back_im = my_image.copy()
                back_im.paste(im2, (313, 190), mask_im)



                #saving the final image
                plt.imshow(back_im)
                back_im.save("./asset/jadi.jpg")
                
                
                
                table_image = Image.open("./asset/table-kosongan.jpg")
                image_table = ImageDraw.Draw(table_image)

                tb_font = ImageFont.truetype("./asset/Montserrat-Regular.ttf", 22)

                List = x["Pembelian"]

                t = 0

                for i in range(len(List)):
                    Nomor = i + 1
                    Katalog = List[i][0]
                    Jumlah = List [i][1]
                    Tanggal = List[i][2]
                    image_table.text((100,161+t), str(Nomor), font=tb_font,  fill="#797a7b")
                    image_table.text((183,161+t), Katalog.upper() , font=tb_font,  fill="#797a7b")    
                    image_table.text((422,161+t), Jumlah , font=tb_font,  fill="#797a7b")        
                    image_table.text((705,184+t), Tanggal , font=tb_font, align="right", anchor ="rs",  fill="#797a7b")
                    t = t + 63
                
                table_image.save("./asset/jadi-2.jpg")
                
                
                #load hasil
                hasil_1 = "./asset/jadi.jpg"
                hasil_2 = "./asset/jadi-2.jpg"
                
                filenames = [hasil_1, hasil_2]
                media_ids = []
                for filename in filenames:
                     res = api.media_upload(filename)
                     media_ids.append(res.media_id)

                kata2 = "Hello kak " + a["user"]["screen_name"] + "! here's your Catto Club membership status."
                    
                # Tweet with multiple images
                api.update_status(status="@" + a["user"]["screen_name"]  + " " + kata2, media_ids=media_ids, in_reply_to_status_id = status_id)

            
                
                # posting the tweet
                #api.update_status_with_media("@" + a["user"]["screen_name"], hasil, in_reply_to_status_id = status_id)
                
                print("a catto club image to " + a["user"]["screen_name"] + "posted")
        
        else:
            pass
    
    def on_direct_message(self, status): 
        #code to run each time the stream receives a direct message
        print(status.text)


printer = IDPrinter(
    CONSUMER_KEY, CONSUMER_SECRET,
    ACCESS_TOKEN, ACCESS_TOKEN_SECRET
)

printer.filter(track=["@cattoclub"])
