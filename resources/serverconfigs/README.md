# serverconfigs go here

Here will live your configuration files for your game servers. The application will expect JSON files with the following structure:

### Expected structure

`````json
{
  "name": "name of your game server",
  "user": "linux user any commands will run under",
  "start": {
    "script": "here goes your starting script"
  },
  "status": {
    "script": "here goes your status script"
  },
  "stop": {
    "script": "here goes your stopping script"
  }
}
`````