# CryptorPWS

A utility for generating PowerShell scripts that download and execute EXE files, demonstrating virus encryption techniques.

## Description

CryptorPWS is a GUI application that generates PowerShell scripts for automatically downloading and running EXE files. The scripts can be encoded in base64 for additional obfuscation. This tool is designed to demonstrate how malicious software can use encryption and obfuscation techniques to evade detection.

![image](https://github.com/user-attachments/assets/cf7dd356-cb1d-422d-b848-489aab0619b8)

## Features

- Creation of PowerShell scripts for downloading EXE files from URLs
- Base64 encoding option for script obfuscation
- Demonstration of antivirus check bypassing techniques for C:\ drive
- Hidden execution mode for scripts
- Execution of downloaded programs with administrator privileges

## Installation

1. Clone the repository
```
git clone https://github.com/yourusername/CryptorPWS.git
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Run the program
```
python main.py
```

## Usage

1. Enter the URL for downloading the EXE file
2. Enter a name for the generated PS1 file
3. Choose whether to encode the script in base64
4. Specify the directory to save the script
5. Click the "Build" button

## Disclaimer

This program is intended for educational purposes only, to demonstrate how malicious software can use encryption and obfuscation techniques. It should be used in a controlled environment for learning about cybersecurity. Use at your own risk and never for malicious purposes.
