# LF3 Decryptor
This script decrypts LeapFrog's LF3 files. Credit to Deak Phreak and is0Mick for writing this code in LeapPad Manager, credit to BLiNXthetimesweeperGOD/Dr. RNG for decompiling this code, and credit to ChatGPT for converting the originally C# code to Python and also doing everything except for bug fixes because I have no clue how to do it.

# Before use
I'm too dumb to properly troubleshoot, and as a result of that, you need to modify lines 10 and 11 with your cache folder and the folder you want files to decrypt to. Place the edited script in a folder with a copy of [7za.exe](https://www.7-zip.org/a/7z2301-extra.7z) (or install it to your PATH). Make sure the pip package cryptography is installed.

# Usage
```
lf3.py file/location/here/
```
You can decrypt single files or a folder of files. Note you cannot decrypt files in subdirectories (as I have no clue why or how to fix it).
