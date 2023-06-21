# ClashVerse

## To-do

- [ ] Update to latest `coc.py`
- [ ] Update to latest `discord.py` and remove dependance from `discord_py_slash_command`
- [ ] Rework database to use `motor` instead of `pymongo`
- [ ] Separate database operations, processing, and image generation.
- [ ] Add support for TH15 in clan and war commands.
- [ ] Add comments to the code 🙈

## secret.py

This file with the below contents need to be created and placed in the same place as the bot.py file.

```py
extensions = [ "cogs.general", "cogs.zapquake", "cogs.clan", "cogs.server" ]
mongodb_url = "mongogo_db_url_here"
discord_token = "bot_discord_token_here"
testguild = [your_test_server_id]
statguild = [your_test_server_id]
swordguild = [your_sword_server_id]
swordchannel = your_sword_channel_id
coc_email = "coc_api_site_login_email"
coc_password = "coc_api_site_login_password"
coc_keycount = 1
useCocPy = True
```