![Image of dlive.py](./dlivepy.png)

DLive.py is an asynchronous wrapper for making bots in Python, for DLive

### THIS IS IN DEVELOPMENT

### Support
For support with the wrapper, please join the support server [here](https://discord.gg/WSEFTkY)

### Installation
To install dlive.py, the use on of the following commands

```
# Linux/macOS
python3 -m pip install -U dlive.py

# Windows
py -3 -m pip install -U dlive.py
```

To install via GitHub, use:

```
# Linux/macOS
python3 -m pip install git+https://github.com/A-Trash-Coder/dlive.py

# Windows
py -3 -m pip install -U git+https://github.com/A-Trash-Coder/dlive.py
```

### Example Usage

```python
import dlive

bot = dlive.models.Bot(command_prefix="!", channels=["A-Trash-Coder"])

@bot.listener
async def ready():
    print("ready")

bot.run("auth token")
```