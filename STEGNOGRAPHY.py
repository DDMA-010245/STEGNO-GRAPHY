import os
import base64
import hashlib
from cryptography.fernet import Fernet
from PIL import Image
import numpy as np
import cv2
from pydub import AudioSegment

# ===================== ENCRYPTION =====================

def generate_key(num_key: int) -> bytes:
    key = hashlib.sha256(str(num_key).encode()).digest()
    return base64.urlsafe_b64encode(key)

def encrypt_message(message: str, num_key: int) -> bytes:
    return Fernet(generate_key(num_key)).encrypt(message.encode())

def decrypt_message(cipher: bytes, num_key: int) -> str:
    return Fernet(generate_key(num_key)).decrypt(cipher).decode()

# ===================== IMAGE =====================

def hide_image(in_path, out_path, data):
    img = Image.open(in_path)
    arr = np.array(img)

    binary = ''.join(format(b, '08b') for b in data) + '1111111111111110'
    idx = 0

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            for k in range(3):
                if idx < len(binary):
                    arr[i][j][k] = (arr[i][j][k] & 254) | int(binary[idx])
                    idx += 1

    Image.fromarray(arr).save(out_path)

def extract_image(path):
    img = Image.open(path)
    arr = np.array(img)
    bits = ""

    for i in range(arr.shape[0]):
        for j in range(arr.shape[1]):
            for k in range(3):
                bits += str(arr[i][j][k] & 1)

    data = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if byte == '11111111':
            break
        data.append(int(byte, 2))

    return bytes(data)

# ===================== AUDIO =====================

def hide_audio(in_path, out_path, data):
    audio = AudioSegment.from_file(in_path)
    raw = bytearray(audio.raw_data)

    binary = ''.join(format(b, '08b') for b in data) + '1111111111111110'
    if len(binary) > len(raw):
        raise ValueError("Message too large for this audio file")

    for i in range(len(binary)):
        raw[i] = (raw[i] & 254) | int(binary[i])

    audio._spawn(bytes(raw)).export(out_path, format="wav")

def extract_audio(path):
    audio = AudioSegment.from_file(path)
    raw = audio.raw_data
    bits = ''.join(str(b & 1) for b in raw)

    data = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if byte == '11111111':
            break
        data.append(int(byte, 2))

    return bytes(data)

# ===================== VIDEO =====================

def hide_video(in_path, out_path, data):
    cap = cv2.VideoCapture(in_path)
    # Changed to FFV1 for lossless compression to prevent data corruption
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(
        out_path, fourcc, cap.get(5),
        (int(cap.get(3)), int(cap.get(4)))
    )

    binary = ''.join(format(b, '08b') for b in data) + '1111111111111110'
    idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                for k in range(3):
                    if idx < len(binary):
                        frame[i][j][k] = (frame[i][j][k] & 254) | int(binary[idx])
                        idx += 1

        out.write(frame)

    cap.release()
    out.release()

def extract_video(path):
    cap = cv2.VideoCapture(path)
    bits = ""
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        for i in range(frame.shape[0]):
            for j in range(frame.shape[1]):
                for k in range(3):
                    bits += str(frame[i][j][k] & 1)

    cap.release()
    
    data = []
    for i in range(0, len(bits), 8):
        byte = bits[i:i+8]
        if byte == '11111111':
            break
        data.append(int(byte, 2))
        
    return bytes(data)

# ===================== MENU =====================

def main():
    print("\nWELCOME TO DARK-DEVIL'S STEGANOGRAPHY MODEL ( BASIC )\n")
    print("1 :) ENCRYPTION")
    print("2 :) DECRYPTION")
    choice = input("       CHOOSE :) -> ")

    if choice == "1":
        message = input("\nENTER THE SECRET MESSAGE : ")
        key = int(input("ENTER THE KEY FOR ENCRYPTION ( NUMBER ) : "))

        print("\nFILE TYPE :")
        print("1 :) IMAGE -> .PNG")
        print("2 :) VIDEO -> .AVI")
        print("3 :) MUSIC -> .WAV")
        ftype = input("       CHOOSE :) -> ")

        in_file = input("\nENTER INPUT FILE PATH : ")
        out_file = input("ENTER OUTPUT FILE PATH : ")

        encrypted = encrypt_message(message, key)

        if ftype == "1":
            hide_image(in_file, out_file, encrypted)
        elif ftype == "2":
            hide_video(in_file, out_file, encrypted)
        elif ftype == "3":
            hide_audio(in_file, out_file, encrypted)
        else:
            print("INVALID FILE TYPE")
            return

        print("\nENCRYPTED")
        print("GENERATED THE FILE OF THE ENCRYPTED FILE")

    elif choice == "2":
        key = int(input("\nENTER THE KEY : "))
        enc_file = input("ENTER THE ENCRYPTED FILE PATH : ")

        ext = enc_file.split(".")[-1].lower()

        try:
            if ext == "png":
                data = extract_image(enc_file)
            elif ext == "wav":
                data = extract_audio(enc_file)
            elif ext == "avi":
                data = extract_video(enc_file)
            else:
                print("FILE TYPE NOT SUPPORTED")
                return

            msg = decrypt_message(data, key)
            print("\nDECRYPTION SUCCESSFUL")
            print("SECRET MESSAGE : ", msg)

        except Exception:
            print("\nDECRYPTION FAILED")
            print("WRONG KEY OR NO HIDDEN DATA")

    else:
        print("INVALID OPTION")

if __name__ == "__main__":
    main()
