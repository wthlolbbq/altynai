## AltynAI

A simple Discord Bot written using Python.

### Requirements

- `python 3.10` or above

Install the latest version of the following packages (if you're using `pip`, run `pip install -r requirements.txt`):

- `discord.py`
- `python-dotenv`

Include a `.env` file in the directory root with your Discord token in the following format:

  ```properties
  DISCORD_TOKEN=YOUR_TOKEN_STRING
  ```

### Startup Script

`startup.sh` may be used to automatically start the bot in a containerized or virtual environment 
with `bash` installed. Make sure to give it execute permissions before running it.
