from PIL import Image

def main():
    Img = Image.open("Profile Pic.png")
    
    crop_box = (0,0,500,500)
    cropped_image = Img.crop(crop_box)
    cropped_image.show()
    Img.close()
    
    
main()