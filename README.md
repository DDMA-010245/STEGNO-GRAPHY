# DARK-DEVIL'S STEGANOGRAPHY MODEL

A powerful and user-friendly steganography tool capable of hiding secret messages within Image, Audio, and Video files using AES-256 encryption.

## Features

-   **Image Steganography**: Hide messages in `.png` files.
-   **Audio Steganography**: Hide messages in `.wav` files.
-   **Video Steganography**: Hide messages in `.avi` files (using FFV1 codec for lossless compression).
-   **Encryption**: Secures your messages using Fernet (symmetric encryption) before hiding them.
-   **Key Generation**: Generates a unique key based on a numeric input for encryption/decryption.

## Requirements

-   Python 3.x
-   cryptography
-   pillow
-   numpy
-   opencv-python
-   pydub

## Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/DDMA-010245/STEGNO-GRAPHY.git
    cd STEGNO-GRAPHY
    ```

2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

    *Note: For audio steganography, you may need to install ffmpeg manually if not already present on your system.*

## Usage

Run the main script:

```bash
python STEGNOGRAPHY.py
```

### Steps to Hide Data (Encryption)

1.  Select **Option 1 (ENCRYPTION)**.
2.  Enter your **Secret Message**.
3.  Enter a **Numeric Key** (remember this, you will need it for decryption).
4.  Choose the **File Type** (Image, Video, or Music).
5.  Enter the **Input File Path** (e.g., `image.png`).
6.  Enter the **Output File Path** (e.g., `encrypted_image.png`).

### Steps to Extract Data (Decryption)

1.  Select **Option 2 (DECRYPTION)**.
2.  Enter the **Numeric Key** used during encryption.
3.  Enter the **Encrypted File Path**.
4.  The tool will extract and display your secret message.

## Disclaimer

This tool is for educational purposes only. The author is not responsible for any misuse of this software.
