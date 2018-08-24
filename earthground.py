import urllib.request
from PIL import Image
from datetime import datetime,timedelta


img_loc = 'C:/Users/Qin/Documents/python/earthground/images/'

utc = datetime.utcnow()
utc_str = str(utc)

date = utc_str[:10].replace('-','') #yyymmdd
time = utc_str[11:15].replace(':','')+'000' # hour-1 + 10 minutes + 000
time = str(utc-timedelta(minutes=10))[11:15].replace(':','')+'000' #update every 10 minutes
# print(datetime.utcnow())
himawari8 = 'http://rammb-slider.cira.colostate.edu/data/imagery/{}/himawari---full_disk/geocolor/{}{}/'.format(date,date,time)

him8am = 'http://rammb.cira.colostate.edu/ramsdis/online/images/latest_hi_res/himawari-8/full_disk_ahi_rgb_airmass.jpg'
goes16 = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/1808x1808.jpg'
goes16v = 'https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/02/1808x1808.jpg'

tl = '/01/000_000.png'
tr = '/01/000_001.png'
ll = '/01/001_000.png'
lr = '01/001_001.png'


#http://rammb-slider.cira.colostate.edu/data/imagery/20180824/himawari---full_disk/geocolor/20180824060000/01/001_001.png - retrieved on 08/24/2018
#http://rammb.cira.colostate.edu/ramsdis/online/images/latest_hi_res/himawari-8/full_disk_ahi_rgb_airmass.jpg - himawari8 airmass
#https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/1808x1808.jpg - goes16
#https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/09/1808x1808.jpg - goes16 water vapor
#https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/02/1808x1808.jpg - goes16 visibility


while True:
        try:
                response = urllib.request.urlretrieve(himawari8+tl, img_loc+'him8_tl.png')
                break
        except:
                utc = utc-timedelta(minutes=10)
                utc_str = str(utc)
                date = utc_str[:10].replace('-','')
                time = utc_str[11:15].replace(':','')+'000'
                time = str(utc-timedelta(minutes=10))[11:15].replace(':','')+'000'
                himawari8 = 'http://rammb-slider.cira.colostate.edu/data/imagery/{}/himawari---full_disk/geocolor/{}{}/'.format(date,date,time)
                #print(time)

#download images to designated img_loc
urllib.request.urlretrieve(himawari8+tl, img_loc+'him8_tl.png')
urllib.request.urlretrieve(himawari8+tr, img_loc+'him8_tr.png')
urllib.request.urlretrieve(himawari8+ll, img_loc+'him8_ll.png')
urllib.request.urlretrieve(himawari8+lr, img_loc+'him8_lr.png')

urllib.request.urlretrieve(him8am, img_loc+'him8am.jpg')

urllib.request.urlretrieve(goes16, img_loc+'goes16.jpg')
urllib.request.urlretrieve(goes16v, img_loc+'goes16v.jpg')

#merge himawari 8 images
img_tl = Image.open(img_loc+'him8_tl.png')
img_tr = Image.open(img_loc+'him8_tr.png')
img_ll = Image.open(img_loc+'him8_ll.png')
img_lr = Image.open(img_loc+'him8_lr.png')

(width, height) = img_tl.size
result_width = width*2
result_height = height*2

him8 = Image.new('RGB', (result_width, result_height))
him8.paste(im=img_tl, box=(0, 0))
him8.paste(im=img_tr, box=(width, 0))
him8.paste(im=img_ll, box=(0, height))
him8.paste(im=img_lr, box=(width, height))
him8.save(img_loc+'him8.jpg')

#resize and merge him8 and goes16 images to specified resolution
img1 = Image.open(img_loc+'goes16.jpg')
img2 = Image.open(img_loc+'him8.jpg')

img3 = Image.open(img_loc+'goes16v.jpg')
img4 = Image.open(img_loc+'him8am.jpg')

height = 1080
width = 1920

imggh1 = img1.resize((int(width/2),height),Image.NEAREST)
imggh2 = img2.resize((int(width/2),height),Image.NEAREST)

resgh = Image.new('RGB', (width, height))

resgh.paste(im=imggh1, box=(0, 0))
resgh.paste(im=imggh2, box=(int(width/2), 0))

resgh.save(img_loc+'geog_himawari.bmp')



# him8 & him8 water vapor & goes16 & goes16 visibility

imgvwv1 = img1.resize((int(width/2),int(height/2)),Image.NEAREST)
imgvwv2 = img2.resize((int(width/2),int(height/2)),Image.NEAREST)
imgvwv3 = img3.resize((int(width/2),int(height/2)),Image.NEAREST)
imgvwv4 = img4.resize((int(width/2),int(height/2)),Image.NEAREST)

resvwv = Image.new('RGB', (width, height))

resvwv.paste(im=imgvwv1, box=(0, 0))
resvwv.paste(im=imgvwv2, box=(int(width/2), 0))
resvwv.paste(im=imgvwv3, box=(0,int(height/2)))
resvwv.paste(im=imgvwv4, box=(int(width/2),int(height/2)))

resvwv.save(img_loc+'geog_vis_him_wv.bmp')


#change desktop
import ctypes
SPI_SETDESKWALLPAPER = 20
ctypes.windll.user32.SystemParametersInfoW(20, 0, img_loc+'geog_himawari.bmp', 3)
