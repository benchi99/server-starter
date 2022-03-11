# Server Starter

Bridge application for starting up game servers from Discord because I'm honestly sick of having to SSH into my VPS y'know

> Why spend one minute doing this task when I could spend a month automating it?
> 
> _- Literally every developer ever_

Requires Python 3.9 or higher to run

## Usage

- Run `pip install -r requirements.txt`
- Define the following environment variables:
  - CLIENT_ID: your discord application's client id
  - CLIENT_SECRET: your discord application's client secret
  - CLIENT_PUBLIC_KEY: your discord application's public key
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
- go nuts mate


## Contributing

The project is still in its early stages, so I won't be accepting pull requests at this time. Sorry!