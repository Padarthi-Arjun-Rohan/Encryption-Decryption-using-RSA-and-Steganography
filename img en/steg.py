from PIL import Image

def text_to_binary(text):
    binary_message = ''.join(format(ord(char), '08b') for char in text)
    return binary_message

def binary_to_text(binary_message):
    text = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8))
    return text

def hide_message_in_image(input_image_path, output_image_path, message):
    binary_message = text_to_binary(message)

    # Open the image
    image = Image.open(input_image_path)
    width, height = image.size

    # Check if the message is too large to fit in the image
    max_message_length = width * height * 3 // 8
    if len(binary_message) > max_message_length:
        raise ValueError("Message is too large to hide in the image.")

    pixel_data = list(image.getdata())
    pixel_index = 0

    # Iterate through the binary message and hide it in the image
    for char in binary_message:
        pixel = list(pixel_data[pixel_index])
        pixel_index += 1
        pixel[-1] = int(char)
        pixel_data[pixel_index - 1] = tuple(pixel)

    # Create a new image with the hidden message
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(pixel_data)
    new_image.save(output_image_path)

def retrieve_message_from_image(input_image_path):
    # Open the image
    image = Image.open(input_image_path)
    pixel_data = list(image.getdata())

    # Retrieve the binary message from the image
    binary_message = ''
    for pixel in pixel_data:
        binary_message += str(pixel[-1])

    # Convert the binary message to text
    message = binary_to_text(binary_message)
    return message

if __name__ == "__main__":
    # Example usage:
    input_image_path = "input_image.png"
    output_image_path = "output_image.png"
    message_to_hide = "This is a secret message!"

    # Hide the message in the image
    hide_message_in_image(input_image_path, output_image_path, message_to_hide)
    print("Message hidden in the image.")

    # Retrieve the hidden message from the image
    retrieved_message = retrieve_message_from_image(output_image_path)
    print("Retrieved message:", retrieved_message)
