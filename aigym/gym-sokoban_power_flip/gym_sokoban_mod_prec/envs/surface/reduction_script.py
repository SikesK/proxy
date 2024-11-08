import imageio
import PIL.Image
folder = './'

def reduce_image_dimensions():
    #image_list = ["x0","x1","x2","x3","x4","x5","x6","x7","x8","x9"] #,"y0","y1","y2","y3","y4","y5","y6","y7","y8","y9"]
    #image_list = ["y0","y1","y2","y3","y4","y5","y6","y7","y8","y9"]
    image_list = ["button_on", "button_off"]
    for im_name in image_list:
        file_name = folder + im_name + ".png"
        target_file_name = folder + im_name + ".jpg"
        img = PIL.Image.open(file_name)
        img = img.resize((16,16))
        fixed_img = img.convert('RGB')
        pixels = img.load()
        #for i in range(16):
        #    pixels[15,i] = (0,0,0)
        #background = PIL.Image.new("RGB", img.size, (255, 255, 255))
        #background.paste(img, mask=img.split()[3]) # 3 is the alpha channel
        #background.save(target_file_name, 'JPEG', quality=80)
        #imageio.imwrite(file_name, fixed_img)
        fixed_img.save(target_file_name, 'JPEG', quality=80)
if __name__ == "__main__":
    reduce_image_dimensions()
    # print(imageio.imread(folder+'temp'))

