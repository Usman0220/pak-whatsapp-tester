# 📱 Pakistani WhatsApp Number Tester 🇵🇰

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Async](https://img.shields.io/badge/Async-aiohttp-green.svg)](https://aiohttp.readthedocs.io/)
[![License](https://img.shields.io/badge/License-Educational-yellow.svg)](#)

> 🚀 **Discover active WhatsApp numbers from Pakistan with lightning speed!** ⚡

## 🎯 What Does This Do?

This powerful Python script automatically generates and tests Pakistani phone numbers to find **active WhatsApp accounts**. When it finds registered numbers, it extracts their:

- 📞 **Phone Numbers** (Local & International format)
- 🖼️ **Profile Pictures** (Downloaded automatically)
- 👤 **Display Names** (From profile headers)
- 🔗 **Direct WhatsApp Links** (Ready to click!)

## ✨ Key Features

### 🔥 **Super Fast Testing**
- **Concurrent requests** - Tests multiple numbers simultaneously
- **Batch processing** - Handles 10 numbers at once
- **Smart rate limiting** - Avoids getting blocked

### 📸 **Profile Picture Magic**
- 🖼️ **Auto-download** profile pictures
- 📁 **Organized storage** in `profile_images/` folder
- 🏷️ **Smart naming** with phone number + display name
- 🛡️ **Error handling** for failed downloads

### 🎲 **Intelligent Number Generation**
- 📱 Generates **realistic Pakistani numbers** (92-3XX format)
- 🔀 **Random but valid** patterns
- 🎯 **High success rate** for finding active numbers

### 🎨 **Beautiful Output**
- 🌈 **Colorful terminal** display
- ✨ **Highlighted names** in bright yellow
- 📊 **Progress tracking** with numbered results
- 🔗 **Clickable links** ready to use

## 🚀 Quick Start

### 📋 Prerequisites
```bash
pip install aiohttp asyncio
```

### 🏃‍♂️ Run the Magic
```bash
python tester5.py
```

### 📁 What You'll Get
```
pak-whatsapp-tester/
├── tester5.py          # 🔧 Main script
├── profile_images/     # 📸 Downloaded pictures
│   ├── 923001234567_John_Doe.jpg
│   ├── 923009876543_Jane_Smith.jpg
│   └── ...
└── README.md          # 📖 This file
```

## 🎮 How It Works

1. **🎲 Generate Numbers**: Creates realistic Pakistani phone numbers
2. **🔍 Test WhatsApp**: Checks if numbers are registered on WhatsApp
3. **📸 Extract Data**: Gets profile pictures and display names
4. **💾 Save Everything**: Downloads images to organized folders
5. **📊 Display Results**: Shows beautiful, clickable output

## 📊 Sample Output

```
01. Local: 03001234567 | waLink: https://api.whatsapp.com/send/?phone=923001234567...
  Display name (h3): John Doe
  Attempting to download profile picture as profile_images/923001234567_John_Doe.jpg ...
  Profile picture saved as profile_images/923001234567_John_Doe.jpg

02. Local: 03009876543 | waLink: https://api.whatsapp.com/send/?phone=923009876543...
  Display name (h3): Jane Smith
  ✅ Profile picture saved as profile_images/923009876543_Jane_Smith.jpg
```

## ⚙️ Configuration

Want to customize? Edit these settings in `tester5.py`:

```python
TARGET_REGISTERED = 20    # 🎯 How many numbers to find
HTTP_TIMEOUT = 5         # ⏱️ Request timeout (seconds)
BATCH_SIZE = 10          # 📦 Numbers to test at once
IMAGES_DIR = "profile_images"  # 📁 Where to save pictures
```

## 🔧 Technical Features

- **🏗️ Async/Await Architecture** - Maximum performance
- **🛡️ Error Handling** - Graceful failure recovery  
- **🔄 Smart Retries** - Handles network issues
- **🧹 Clean Code** - Well-organized and documented
- **🌍 Cross-platform** - Works on Windows, macOS, Linux

## 🎨 Recent Updates

### 🆕 v2.0 - Image Organization
- 📁 **Separate folder** for profile images
- 🔄 **Auto-creation** of directories
- 🌐 **Cross-platform** path handling
- 🎯 **Cleaner** project structure

## 📸 Screenshots

### 🖥️ Terminal Output
```
Created directory: profile_images
01. Local: 03001234567 | waLink: https://api.whatsapp.com/send/?phone=923001234567...
  Display name (h3): محمد علی
  ✅ Profile picture saved as profile_images/923001234567_محمد_علی.jpg

02. Local: 03451234567 | waLink: https://api.whatsapp.com/send/?phone=923451234567...
  Display name (h3): Sara Khan  
  ✅ Profile picture saved as profile_images/923451234567_Sara_Khan.jpg
```

## 🔒 Ethical Usage

⚠️ **Important**: This tool is for **educational purposes only**. Please:
- 🤝 Respect people's privacy
- 📋 Follow local laws and regulations
- 🛡️ Use responsibly and ethically
- 💡 Learn about web scraping and async programming

## 🛠️ Troubleshooting

### 🚫 Getting 403 Errors?
- ✅ Check your internet connection
- 🔄 Try running with fewer concurrent requests
- ⏱️ Add delays between batches

### 📸 Images Not Downloading?
- 🌐 Ensure stable internet connection
- 📁 Check folder permissions
- 🔍 Verify profile pictures are public

## 🤝 Contributing

Found a bug? Have an idea? 

1. 🍴 Fork the repository
2. 🌟 Create your feature branch
3. 💾 Commit your changes
4. 📤 Push to the branch
5. 🎯 Open a Pull Request

## 📜 License

This project is for **educational purposes only**. Use responsibly! 🎓

## 🙏 Acknowledgments

- 💙 **aiohttp** - For amazing async HTTP capabilities
- 🐍 **Python** - For being awesome
- 🇵🇰 **Pakistan** - For the phone number patterns
- 🌟 **Open Source Community** - For inspiration

---

<div align="center">

### 🌟 **Star this repo if you found it useful!** ⭐

Made with ❤️ by developers, for developers

**Happy Coding! 🎉**

</div>
