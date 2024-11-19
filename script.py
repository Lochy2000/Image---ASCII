import PIL.Image 

# ascii character used to build the output text. 
# Each pixel with get assoicated with a similar character depending on its insenity 
ASCII_CHARS = ["@","#","S","%","?","*",";",",","."]

#resize imaage according to a new width
def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize(( new_width, new_height))
    return(resize_image)

#convert each pixel to greyscale 
def grayify(image):
    grayscale_image = image.convert("L")
    return(grayscale_image)

# convert pixels to a string of ASCII characters
def pixels_to_asccii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25]] for pixel in pixels)
    return(characters)


def main(new_width=100):
    #attempt to ope image form user-input
    path = input("Enter a valid pathname to an image plez :/n")
    try:
        image = PIL.Image.open(path)
    except:
        print(path, "is not a valid path to an image.")

    new_image_data = pixels_to_asccii(grayify(resize_image(image)))

    #format 
    pixel_count = len (new_image_data)
    ascii_image ="\n".join(new_image_data[i:(i+new_width)] for i in range(0, pixel_count, new_width))

    #print result 
    print (ascii_image)

    #save result yo "ascii_image.txt"
    with open("ascii_image.txt", "w") as f:
        f.write(ascii_image)
        
main()