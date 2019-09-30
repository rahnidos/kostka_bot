from PIL import Image

im = Image.new("RGB",(142,100),0)
imglist=["cards/6_of_clubs.jpg","cards/5_of_clubs.jpg"]
x=0

for img in imglist:
    tmpf=Image.open(img)
    tmpf.thumbnail((70,100))
    im.paste(tmpf,(x,0))
    x=x+71

im.save('nowe.png')
