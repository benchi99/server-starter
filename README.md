# Server Starter

Bridge application for starting up game servers from Discord because I'm honestly sick of having to SSH into my VPS y'know

> Why spend one minute doing this task when I could spend a month automating it?
> 
> _- Literally every developer ever_

Requires Python 3.8 or higher to run

## Usage

It is highly encouraged to utilise any flavour of Linux as your OS for the best experience.

- Install the following packages with your package manager of choice
```shell
$ sudo apt install -y python3 python3-dev python3-pip build-essential uwsgi uwsgi-plugin-python3
```
- Run `pip install -r requirements.txt`
- Define the following environment variables:
  - CLIENT_ID: your discord application's client id
  - CLIENT_SECRET: your discord application's client secret
  - CLIENT_PUBLIC_KEY: your discord application's public key
  - PASS: the linux user's account password that will run the commands to start and stop servers
- Run the application
  - To create slash commands in a given guild, run the following:
```shell
$ python entrypoint.py --create_commands <guild_id>
```
  - To start the Flask application and listen for interactions, run the following:
```shell
$ python entrypoint.py
```

## Local development setup

- Run `pip install -r requirements.txt` 
- Define the following environment variables:
  - CLIENT_ID: your discord application's client id
  - CLIENT_SECRET: your discord application's client secret
  - CLIENT_PUBLIC_KEY: your discord application's public key
  - PASS: the linux user's account password that will run the commands to start and stop servers
- Start developing!

## Contributing

Pull requests are welcome! Specially to change the way to call commands as another user without requiring the invoking user's password.