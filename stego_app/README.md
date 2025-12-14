# Cyber Steganography Suite

![Cyber Steganography](https://img.shields.io/badge/Cyber-Steganography-blue?style=for-the-badge&logo=python&logoColor=white)
![Version](https://img.shields.io/badge/Version-1.0.0-green?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-red?style=flat-square)

## 🔒 Overview

**Cyber Steganography Suite** is a comprehensive, user-friendly desktop application for hiding and extracting secret messages within various file types using advanced steganography techniques. Built with Python and Tkinter, it provides a modern GUI interface for secure data concealment.

## ✨ Features

### 🎨 Modern UI/UX
- Dark theme with cyber aesthetic
- Intuitive navigation between modules
- Real-time progress indicators
- Responsive design

### 📁 Supported File Types
- **Images**: PNG
- **Audio**: WAV files
- **Video**: MP4, AVI, MOV, MKV, WMV
- **Text Files**: TXT

### 🔧 Steganography Methods

#### Images
- **LSB (Least Significant Bit)**: Pixel-based hiding (1 bit per RGB channel)
- **Metadata Chunk**: PNG chunk-based metadata injection

#### Audio
- **LSB in Audio Samples**: Sample-based audio steganography
- **Chunk Injection**: WAV metadata chunk injection

#### Video
- **LSB in Frames**: Advanced LSB frame-based video steganography
- **Metadata**: Video metadata injection
- **EOF Injection**: Video file end injection

#### Text Files
- **Whitespace Encoding**: Hiding in spaces and tabs at line ends
- **Zero-Width Characters**: Invisible Unicode character injection

### 🔐 Security Features
- **AES Encryption**: All hidden messages are encrypted
- **Password Protection**: Strong encryption keys required
- **Multiple Methods**: Choose from various concealment techniques
- **Auto-Detection**: Automatic method detection during extraction

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (for video/audio processing)
- pip package manager

### Step-by-Step Installation

1. **Clone or Download the Repository**
   ```bash
   git clone https://github.com/yourusername/cyber-steganography.git
   cd cyber-steganography
   ```

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install FFmpeg**
   - **Windows**: Download from [FFmpeg website](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`

4. **Run the Application**
   ```bash
   python main.py
   ```

## 📖 Usage Guide

### Getting Started
1. Launch the application with `python main.py`
2. Navigate through the modules using the main menu
3. Select your desired file type (Image, Audio, Video, Text)

### Hiding a Message (Encoding)

1. **Select Source File**: Choose the file you want to hide data in
2. **Choose Output Location**: Specify where to save the encoded file
3. **Select Method**: Pick your preferred steganography method
4. **Enter Secret Message**: Type or paste your message
5. **Set Encryption Key**: Create a strong password for encryption
6. **Encode**: Click the encode button and wait for completion

### Extracting a Message (Decoding)

1. **Select Encoded File**: Choose the file containing hidden data
2. **Set Decryption Key**: Enter the password used during encoding
3. **Choose Method**: Select Auto-detect or specific method
4. **Decode**: Extract the hidden message

### Tips for Best Results

- **Use strong passwords** (12+ characters, mixed case, numbers, symbols)
- **For videos**: LSB method offers highest capacity but slower processing
- **For quick operations**: Use Metadata method for videos
- **File size impact**: LSB methods may increase file size; others have minimal impact

## 🔧 Technical Details

### Architecture
- **Frontend**: Tkinter-based GUI
- **Backend**: Python modules for each file type
- **Encryption**: Fernet (AES-based symmetric encryption)
- **Image Processing**: OpenCV and PIL
- **Audio/Video Processing**: OpenCV and FFmpeg

### Security Considerations
- Messages are encrypted before hiding
- No plaintext data stored in memory
- Secure key derivation using PBKDF2
- Multiple steganography methods for deniability

## 📋 Requirements

### Python Packages
```
cryptography>=3.4.7
opencv-python>=4.5.3
Pillow>=8.3.1
numpy>=1.21.2
```

### System Requirements
- **OS**: Windows 10+, macOS 10.15+, Linux
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 100MB free space
- **Display**: 1280x720 minimum resolution

## 🐛 Troubleshooting

### Common Issues

**Application won't start**
- Ensure Python 3.8+ is installed
- Check all dependencies are installed: `pip install -r requirements.txt`

**FFmpeg not found**
- Install FFmpeg and ensure it's in PATH
- For Windows, add FFmpeg bin folder to system PATH

**Encoding/Decoding fails**
- Verify file formats are supported
- Check file permissions and disk space
- Ensure encryption keys match

**Video processing is slow**
- Use Metadata method for fastest video processing
- Reduce video resolution if possible
- Close other resource-intensive applications

### Error Messages
- **"No LSB marker found"**: File doesn't contain LSB-encoded data
- **"Decryption failed"**: Wrong password or corrupted data
- **"Video too short"**: Source video lacks capacity for message

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit with clear messages: `git commit -m "Add feature X"`
5. Push to your fork: `git push origin feature-name`
6. Create a Pull Request

### Development Setup
```bash
# Clone repository
git clone https://github.com/yourusername/cyber-steganography.git
cd cyber-steganography

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with Python and Tkinter
- Uses OpenCV for multimedia processing
- Cryptography library for secure encryption
- FFmpeg for advanced video/audio handling

## 📞 Support

For support, bug reports, or feature requests:
- Create an issue on GitHub
- Check the troubleshooting section above
- Ensure you're using the latest version

---

**⚠️ Disclaimer**: This tool is for educational and legitimate security research purposes only. Users are responsible for complying with applicable laws and regulations regarding data concealment and privacy.