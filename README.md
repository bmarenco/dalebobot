# dalebobot
This is a Twitter bot that automatically replies "Dale bobo" to the people it follows. 
It is written in python 2 using [Tweepy](https://www.tweepy.org/).

## Requirements
You need to Python 2.7 or later to run the bot. If you have an Ubutuntu distro you can install Python 2 by saying:

```bash
sudo apt install python2.7
```

If you have Windows: why?

Optionally, you can install pip to handle the dependencies:

```bash
sudo apt install python-pip
```

Then, requirements can be installed using pip (it is recommended to use a [virtual environment](https://realpython.com/python-virtual-environments-a-primer/)):

```bash
pip install -r requirements.txt
```

## Usage

Simply run:

```bash
python check_for_bobada.py
```

Optionally, you can a pass the program a list of Twitter handles you want the bot to follow and reply to, using the `-b` or `--bobo_list` flag:

```bash
python check_for_bobada.py -b userhandle1 userhandle2 ... userhandleN
```

Login to your Twitter account is handled by the `config`module. This module is exactly the same as the one in [this Tweepy tutorial](https://realpython.com/twitter-bot-python-tweepy/).
It reads authentication credentials from the environment variables `CONSUMER_KEY`, `CONSUMER_SECRET`, `ACCESS_TOKEN` and `ACCESS_TOKEN_SECRET`.
To set them, export them before running the program:

```bash
export CONSUMER_KEY="your consumer key"
export CONSUMER_SECRET="your consumer secret"
export ACCESS_TOKEN="your access token"
export ACCESS_TOKEN_SECRET="your access token secret"
```

See [this section of the above tutorial](https://realpython.com/twitter-bot-python-tweepy/#creating-twitter-api-authentication-credentials) for more info on authentication credentials.

## License

This software is published under the GNU AFFERO GENERAL PUBLIC LICENSE  - See [LICENSE.md](./LICENSE.md).