
# DC Shop Automation Script

## Overview

This script automates interactions with the DragonForce DBTech Shop using Python. It performs various actions such as logging in, withdrawing and depositing funds, stealing currency, and marking messages as read.

## Features

- Automated login
- Withdraw funds
- Deposit funds
- Steal currency from other users
- Mark all messages as read
- Retrieve top 5 users

## Prerequisites

- Python 3.12 or later
- Google Chrome or Chromium
- [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads)

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**

   Ensure you have a `requirements.txt` file in the root directory of your project with the following content:

   ```plaintext
   requests
   selenium
   webdriver-manager
   colorama
   ```

   Then, run:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install Google Chrome or Chromium:**

   Follow the instructions based on your operating system:

   ### Debian/Ubuntu:

   ```bash
   sudo apt update
   sudo apt install -y google-chrome-stable
   ```

   Or for Chromium:

   ```bash
   sudo apt update
   sudo apt install -y chromium-browser
   ```

5. **Create a configuration file:**

   Create a file named `setting.ini` in the root directory with the following content:

   ```ini
   [LOGIN]
   username = your_username
   password = your_password
   ```

   Replace `your_username` and `your_password` with your actual credentials.

## Usage

To run the script:

```bash
python main.py
```

The script will log in, perform various actions, and print the results. It will continuously run, performing actions every 0.5 seconds.

## Troubleshooting

- **ChromeDriver not found**: Ensure ChromeDriver is installed and properly configured. You can manually download it from [ChromeDriver's website](https://sites.google.com/a/chromium.org/chromedriver/downloads) if automatic installation fails.
- **Headless Chrome errors**: Ensure Google Chrome or Chromium is installed and accessible. Verify your environment supports headless browsing.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact <dodgerxc47@gmail.com>.
