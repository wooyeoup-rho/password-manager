# Password Manager App
A simple Password Manager app built with Python and Tkinter.

Created as a part of [
100 Days of Code: The Complete Python Pro Bootcamp
](https://www.udemy.com/course/100-days-of-code/) by Angela Yu.

## Disclaimer
The application *may be flagged as malicious* by certain security vendors and antivirus programs (6/70 on VirusTotal).
- It's likely due to the app's behaviour in writing to and modifying a .txt file (data.txt that stores the passwords).

**The application does not transmit any data. You are encouraged to inspect the code and build it yourself. Steps below.**

---
### Demonstration


https://github.com/user-attachments/assets/93ac0842-a9f8-46ff-beff-9b9d3207d596


---
### Requirements
1. Python
2. PyInstaller (For creating the executable)

### Installation
Clone the repository:

```commandline
git clone https://github.com/wooyeoup-rho/password-manager.git
```

### Running the application:
```commandline
cd password-manager
python main.py
```

### Creating an executable
1. Install PyInstaller
```commandline
pip install pyinstaller
```
2. Create the executable:
```commandline
pyinstaller --onefile --add-data "assets;assets" --name password-manager --windowed --icon=assets/images/lock.ico main.py
```
- `--onefile` bundles everything into a single executable.
- `--add-data "assets;assets"` includes everything in the `assets` file into the executable.
- `--name password-manager` names the executable file.
- `--windowed` prevents a command-line window from appearing.
- `--icon=assets/images/lock.ico` specifies the application icon.
- `main.py` specifies the Python script to bundle.

3. Locate and run the executable:

The executable will be located in the `dist` folder. You can now open the `password-manager.exe` inside to open the application.
