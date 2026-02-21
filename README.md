# Whisper Bot

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![discord.py](https://img.shields.io/badge/library-discord.py-5865f2?logo=discord&logoColor=white)](https://github.com/Rapptz/discord.py)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This is a Discord bot cog that lets users send **secret whisper messages** to other users in a server. The whisper appears as a public embed notifying the recipient, but the actual message content is hidden behind a button that only the intended recipient can reveal.

---

## How It Works

### Sending a Whisper
There are two ways to send a whisper:

- **Prefix command:** `!whisper @user your message here` — The bot deletes your original command message and posts the whisper embed in the channel. Take into consideration it WILL be visible to the chat for a little moment, so it is possible to see the message, which is why I prefer...
- **Slash command:** `/whisper @user` — A modal (popup form) appears for you to type your message privately before sending.

### The Whisper Embed
Once sent, the bot posts an embed in the channel notifying the target user that they have a whisper waiting. The embed does **not** reveal who sent it or what the message says.

### Revealing the Whisper
The embed includes a **"Reveal Whisper"** button. Only the intended recipient can click it — anyone else will receive an ephemeral error message. When the recipient clicks it, they see an ephemeral embed showing the sender and the full message content.

---

## Setup

1. Install dependencies:
   ```
   pip install discord.py
   ```
2. Create a bot in the [Discord Developer Portal](https://discord.com/developers/applications) and enable the **Message Content Intent**
3. Load the cog in your bot's main file:
   ```python
   await bot.load_extension("main")  # or wherever the file is located
   ```
4. Run your bot.

---

## Things to consider / change

### Hide the Sender's Identity Until Revealed
Currently the sender is shown when the whisper is revealed. To make whispers fully anonymous, replace the `From` field in the embed with a generic label:
```python
embed.add_field(name="From", value="Anonymous", inline=False)
```

### Add a Whisper Log for Moderation
To keep a private log of all whispers (e.g. for moderation purposes), write to a file or database inside `send_whisper_embed()`:
```python
with open("whisper_log.txt", "a") as f:
    f.write(f"{sender} -> {target}: {message_content}\n")
```

### Set an Expiry on the Reveal Button
By default the view has no timeout, meaning the button lasts forever. Add a timeout (in seconds) to expire it:
```python
super().__init__(timeout=300)  # Button expires after 5 minutes
```

### Limit Whispers to Specific Channels
Add a channel check inside the prefix command or slash command handler:
```python
ALLOWED_CHANNELS = [123456789, 987654321]

if ctx.channel.id not in ALLOWED_CHANNELS:
    await ctx.send("Whispers are not allowed in this channel.", ephemeral=True)
    return
```

### Prevent Users from Whispering Themselves
Add a self-whisper check before sending:
```python
if member == ctx.author:
    await ctx.send("You can't whisper to yourself!", ephemeral=True)
    return
```

---

## Further info
- The bot requires the `Manage Messages` permission to delete the original `!whisper` command message.
- Ephemeral messages (the reveal and error responses) are only visible to the relevant user and disappear when dismissed.
- The slash command modal approach is recommended as it keeps the message content fully hidden from anyone watching the channel.
