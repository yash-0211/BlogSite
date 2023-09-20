from PIL import Image
e= "sedv"
img = Image.open(f"static/img/propics/{e.id}.jpg")
width, height = img.size
if width==height:
    pass
elif width>= height:
    diff= width-height
    left= diff//2
    right= width-diff//2
else:
    diff= height-width
    top= diff//2
    bottom= height-diff//2
left = 5
top = height / 4
right = 164
bottom = 3 * height / 4
 
im1 = img.crop((left, top, right, bottom))

im1.save(f"static/img/propics/{e.id}.jpg")