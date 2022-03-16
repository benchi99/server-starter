# serverconfigs go here

Here will live your configuration files for your game servers. The application will expect JSON files with the following structure:

### Expected structure

`````json
{
  "name": "name of your game server",
  "user": "linux user any commands will run under",
  "start": {
    "allowed_users_to_run_command": [
      "user_id_in_discord_1",
      "user_id_in_discord_2"
    ],
    "script": "echo 'cool this will totally start my game server'"
  },
  "status": {
    "allowed_users_to_run_command": null,
    "script": "echo 'aw yes the server's running all fine mate'"
  },
  "stop": {
    "allowed_users_to_run_command": [
      "140100355902930944"
    ],
    "script": "echo 'time to sleep now server'"
  }
}
`````