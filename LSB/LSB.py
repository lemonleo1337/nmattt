import sys
import numpy as np
from PIL import Image
np.set_printoptions(threshold=sys.maxsize)


def encode(src, message, dest, password):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))
    # print(array[0], array[1], array[2])
    n = 3
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size // n

    message += password
    # print("Message to Hide:", message)
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)
    # print("Bit", b_message)

    if req_pixels > (total_pixels * 3):
        print("ERROR: Need larger file size")

    else:
        index = 0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(format(array[p][q], '08b')[:-1] + b_message[index], 2)
                    index += 1
        # print(array[0], array[1], array[2])
        # Save the Encoded Image
        array = array.reshape(height, width, n)
        enc_img = Image.fromarray(array.astype('uint8'), img.mode)

        if dest.split('.')[1] == 'jpg' or dest.split('.')[1] == 'jpeg':
            dest = dest.split('.')[0] + '.png'
        enc_img.save(dest)
        print("Image Encoded Successfully")


def decode(src, secret):

    img = Image.open(src, 'r')
    array = np.array(list(img.getdata()))
    n = 3
    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4

    total_pixels = array.size//n

    hidden_bits = ""
    for p in range(total_pixels):
        for q in range(0, 3):
            hidden_bits += format(array[p][q], '08b')[-1]

    hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

    message = ""
    hidden_message = ""
    x = len(secret)
    for i in range(len(hidden_bits)):
        if message[-x:] == secret:
            break
        else:
            message += chr(int(hidden_bits[i], 2))
            message = f'{message}'
            hidden_message = message
    # print(message)
    if secret in message:
        print("Hidden Message:", hidden_message[:-x])
    else:
        print("Something went wrong! Please Try Again")


# Using arg parse
def main():
    import argparse
    parser = argparse.ArgumentParser(description='LSB Steganography')
    parser.add_argument('-t', '--type', type=str, help='Encode or Decode')
    parser.add_argument('-s', '--src', type=str, help='Source Image Path')
    parser.add_argument('-m', '--message', type=str, help='Message to Hide')
    parser.add_argument('-o', '--dest', type=str, help='Destination Image Path')
    parser.add_argument('-p', '--secret', default="xes", type=str, help='Secret Password')
    args = parser.parse_args()
    if args.dest is None:
        args.dest = args.src.split('.')[0] + '_lsb' + '.' + args.src.split('.')[1]
    if args.type.lower() == 'encode':
        encode(args.src, args.message, args.dest, args.secret)
    elif args.type.lower() == 'decode':
        decode(args.src, args.secret)
    else:
        print("Invalid Operation")


if __name__ == '__main__':
    main()
