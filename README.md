# Google Form Auto-Filler 🤖📝

This is an automated Python Selenium script designed to fill out a specific, multi-page Google Form. It seamlessly handles demographic questions, Likert scale grids, and multi-page navigation, and includes a smart-loop to submit multiple responses consecutively.

## Features
* **Multi-Page Handling:** Automatically detects and clicks "Next" or "Submit" buttons using a robust text-reading fallback, bypassing Google's strict HTML structures.
* **Weighted Probabilities:** When answering 1-to-5 Likert scale questions, the script is heavily weighted to favor options `3` and `5` (40% chance each), while randomly distributing the remaining choices.
* **Smart Option Filtering:** Automatically ignores specific answers like "Other" on demographic questions, ensuring clean data.
* **Language Agnostic Resiliency:** Forces the Chrome WebDriver and the Form URL to load in English, preventing regional translation bugs from breaking the button-hunting logic.
* **Human Emulation:** Includes slight randomized sleep delays between actions and submissions to mimic human behavior and prevent getting blocked.

## Prerequisites

Before running the script, ensure you have the following installed:
1. **Python 3.x:** Download from [python.org](https://www.python.org/downloads/) (Make sure to check "Add Python to PATH" during installation).
2. **Google Chrome:** The script uses the Chrome browser. Ensure it is updated to the latest version.
3. **Selenium:** The web automation library for Python.

## Installation

1. Clone or download this repository to your local machine.
2. Open your Command Prompt or Terminal.
3. Navigate to the folder containing the script.
4. Install the required Selenium library by running:
   ```bash
   pip install selenium