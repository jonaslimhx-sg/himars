# Introduction
- This repository is created by 4th Himars Battery
- Telegram bot can be used for fire mission checks, griddling, converting grids between rso and utm formats.
    - Refer to `/telegrambot` for more information
- Streamlit can be used for deployment range and overhead violations check
    - Refer to `/streamlit` for more information

# Terraform
- Provisioning of server was done on AWS but you can do use your own server too.
- Ensure the firewall can enable port 22, 443, 8100

# Quickstart
- Run both telegrambot and streamlit in the background of a server (I am use AWS t2.micro)
```
# Create new session window
tmux new -s deploy

cd ../telegrambot
# Install python environment and start telegrambot

# Create new pane
ctr + b + c

cd ../streamlit
# Install python environment and start streamlit

# Close window
ctr + b + d