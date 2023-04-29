# Introduction
- This repository was created by 4th Himars Battery
- Telegram bot can be used for fire mission checks, griddling, converting grids between rso and utm formats.
    - Refer to `/telegrambot` for more information
- Streamlit can be used for deployment range and overhead violations check
    - Refer to `/streamlit` for more information
- A server was provisioned on AWS t2.micro to host the telegrambot and streamlit in the background.

# Terraform
- Terraform was used to manage the server
- Ensure the firewall enables inbound port 22, 443, 8100

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