# 🧰 Toolbox
Toolbox is a utility discord bot for things you didn't know you will need one day. You can quicly set slowmode, or age-restrict channels, get info about a member or role, and a lot more! Im still working on the features.

<div id="badges", align="center">
  <a href="https://repl.it/github/tibor309/toolbox">
    <img src="https://img.shields.io/badge/Replit-F26207.svg?style=for-the-badge&logo=Replit&logoColor=white&label=Run on" alt="Replit Badge"/>
  </a>
  <a href="https://glitch.com/edit/#!/import/github/tibor309/toolbox">
    <img src="https://img.shields.io/badge/Glitch-3333FF.svg?style=for-the-badge&logo=Glitch&logoColor=white&label=Remix on" alt="Glitch Badge"/>
  </a>
  <a href="https://hub.docker.com/r/tibor309/toolbox">
    <img src="https://img.shields.io/badge/Docker-2496ED.svg?style=for-the-badge&logo=Docker&logoColor=white&label=Run on" alt="Docker Badge"/>
  </a>
  <a href="https://discord.com/api/oauth2/authorize?client_id=1158403680962367608&permissions=8&scope=bot%20applications.commands">
    <img src="https://img.shields.io/badge/Discord-5662f6?style=for-the-badge&logo=discord&logoColor=white&label=Invite to" alt="Discord Invite Badge"/>
  </a>
</div>

## Setup
### Replit and Glitch
First clone the repo with the buttons on top, or manually on the site. Then head over to the secrets tab, and create a new secret called `TOKEN`, and place your bot token in the value field. After that just install the packages, and you're done!

### Source
Clone the repo, and install all the required packages with the command below. Then create a secrets file, and set your bot token. After that, just run it somewhere, or change the configuration in the config file. Soon there will be a docker image too!
```
pip3 install -r requirements.txt
```

## Docker
If you prefer, you can run the bot on docker. But you won't be able to customize the configuration. Simply run the command below, and you're done. 
```
docker run -d -it -e TOKEN=your-bot-token tibor309/toolbox:latest
```

## Configuration
You can change a few things in the config file. You can change the date format for logging, icons, embed colors, ect.

> All icons were provided by [fontawesome](https://fontawesome.com/)! <3