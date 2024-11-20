from PIL import Image

def convert_to_ascii(image_path, width=100):
    """
    Convert an image to ASCII art
    """
    # Open image and convert to grayscale
    try:
        img = Image.open(image_path)
        img = img.convert('L')  # Convert to grayscale
    except:
        return "Error: Could not open image file"

    # Calculate new dimensions while maintaining aspect ratio
    aspect_ratio = img.height / img.width
    height = int(aspect_ratio * width * 0.55)  # 0.55 compensates for terminal character spacing
    
    # Resize image
    img = img.resize((width, height))
    
    # ASCII characters from darkest to lightest
    ascii_chars = '@%#*+=-:. '
    
    # Convert pixels to ASCII
    pixels = img.getdata()
    ascii_str = ''
    for i, pixel in enumerate(pixels):
        # Map pixel to ASCII character
        ascii_str += ascii_chars[pixel//32]  # 256/8 = 32 levels
        
        # Add newline after each row
        if (i + 1) % width == 0:
            ascii_str += '\n'
            
    return ascii_str

def main():
    # Get image path from user
    image_path = input("Enter the path to your image: ")
    
    # Convert image to ASCII
    ascii_art = convert_to_ascii(image_path)
    
    # Print ASCII art
    print(ascii_art)
    
    # Save ASCII art to file
    with open('ascii_art.txt', 'w') as f:
        f.write(ascii_art)
    print("ASCII art has been saved to 'ascii_art.txt'")

if __name__ == "__main__":
    main()