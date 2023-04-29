# Python Environment
```
conda create -n telegram python=3.8
conda activate telegram
pip install pyTelegramBotAPI psutil watchdog python-dotenv
```
# Start Bot
Get BOT_TOKEN from Telegram @BotFather and add in `.env.template` while renaming the file to `.env`
```
conda activate telegram
python main.py
```
# Commands
| commands  | description 
| :---      | :---
| /fmsn_fdo | Fire mission check with utm target grid
| /fmsn_fo  | Fire mission check with rso target grid
| /rso_to_utm   | Convert grid from rso to utm format
| /utm_to_rso   | Convert grid from utm to rso format
| /griddle  | Convert Digits to Alphabets
| /degriddle    | Convert Alphabets to Digits
| /set_utm_fp   | Setup Telegram Bot Firing Point in UTM format
| /set_dof  | Setup Telegram Bot Direction of Fire
| /set_griddle  |   Setup Telegram Bot Griddle Table
| /get_fp   |   Check Telegram Bot Firing Point
| /get_dof  |   Check Telegram Bot Direction of Fire
| /get_griddle  |   Check Telegram Bot Griddle Table

# Possible Future Improvements
1. `/get_target_grid`
    - Pre-requisite: `/set_utm_fp` has been done
    - Input: range in metres, dof in mils
    - Output: target grid with the respective range and dof from the firing point set.


