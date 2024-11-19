from PIL import Image
import sys

def resize_image(image, new_width=100):
    """Resize image maintaining aspect ratio"""
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width)
    return image.resize((new_width, new_height))

def grayify(image):
    """Convert image to grayscale"""
    return image.convert("L")

def pixels_to_ascii(image):
    """Convert pixels to ASCII chars"""
    ASCII_CHARS = "@%#*+=-:. "
    pixels = image.getdata()
    ascii_str = ''
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 28]  # 255 // 28 = 9 levels
    return ascii_str

def main():
    try:
        # Open the image file
        image_path = input("Enter a valid pathname to an image: ")
        try:
            image = Image.open(image_path)
        except Exception as e:
            print(f"Unable to open image file: {e}")
            return

        # Convert image to ASCII
        new_image_data = pixels_to_ascii(grayify(resize_image(image)))

        # Format ASCII image
        pixel_count = len(new_image_data)
        ascii_image = "\n".join(new_image_data[i:(i + image.size[0])] 
                              for i in range(0, pixel_count, image.size[0]))

        # Print result
        print(ascii_image)

        # Save result to file
        with open("ascii_image.txt", "w") as f:
            f.write(ascii_image)

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()