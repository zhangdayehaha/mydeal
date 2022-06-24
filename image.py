from PIL import Image
bg1 = Image.open('login2.png')
        
        
crop = bg1.crop((300,200, 520,400))

crop.save(('loginsmall2.png'))
