# 🧰 Toolbox
Toolbox is a utility discord bot for things you didn't know you would need one day. You can quicly set slowmode, or age-restrict channels, get info about a member or role, and a lot more!

<div id="badges", align="center">
  <a href="https://repl.it/github/tibor309/toolbox">
    <img src="https://img.shields.io/badge/Replit-8f97cb.svg?style=for-the-badge&logo=Replit&logoColor=gray&labelColor=b4befe&label=Run on" alt="Replit Badge"/>
  </a>
  <a href="https://glitch.com/edit/#!/import/github/tibor309/toolbox">
    <img src="https://img.shields.io/badge/Glitch-8f97cb.svg?style=for-the-badge&logo=Glitch&logoColor=gray&labelColor=b4befe&label=Remix on" alt="Glitch Badge"/>
  </a>
  <a href="https://hub.docker.com/r/tibor309/toolbox">
    <img src="https://img.shields.io/badge/Docker-8f97cb.svg?style=for-the-badge&logo=Docker&logoColor=gray&labelColor=b4befe&label=Pull from" alt="Docker Badge"/>
  </a>
  <a href="https://discord.com/api/oauth2/authorize?client_id=1158403680962367608&permissions=8&scope=bot%20applications.commands">
    <img src="https://img.shields.io/badge/Discord-8f97cb?style=for-the-badge&logo=discord&logoColor=gray&labelColor=b4befe&label=Invite to" alt="Discord Invite Badge"/>
  </a>
</div>

## Setup
### Replit and Glitch
First clone the repo with the buttons on top, or manually on the site. Then head over to the secrets tab, and create a new secret called `TOKEN`, and place your bot token in the value field. Install all the packages using the command below, and you're done!

### Source
Clone the repo, and install all the required packages with the command below. At least python 3.10 is required!
```bash
pip3 install -r requirements.txt
```

Then create a secrets file, and set your bot token. After that, run the but with this command:

```bash
python3 main.py
```

## Docker
You can also run the bot with docker, but you won't be able to customize the configuration. Simply run the command below:

```bash
docker run -d -it -e TOKEN=your-bot-token tibor309/toolbox:latest
```

## Configuration
You can customize the bot in the config file. You can change the date format for logging, icons, embed colors, ect.

> All icons were provided by [fontawesome](https://fontawesome.com/)! <3