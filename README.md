# gclassRoom-autoBot

A python BOT written out of sheer necessity of not being able to get up on time on those lazy mornings to attend classes.

# Features!

  - Import your time-table and watch it attend all your classes everyday till eternity passes away.
  - Leave classes when number of people drops below a threshold.
  - Ability to sleep & wake-up according to schedule.
  - Auto log-in into your G-account


## You can also:

  - Deploy it on any cloud/VPS, the BOT can attend classes according to loaded timetable without any intervention.
  - One-click deploy to Heroku & Slack updates via PaperTrail add-on (coming soon!)

# Initial Set-Up

### This version only supports Chrome Browser, but it's pretty easy to modify the code to work with other browsers.

requires [Python v3](https://www.python.org/downloads/) to run.


## To set-up on your system, follow these steps:


1. Clone this repo.

```sh
$ git clone
```
or

Simply download this repo as `.zip` file and extract the contents somewhere.


2. Check your chrome version `chrome://settings/help` and download appropriate version of ChromeDriver [here](https://chromedriver.chromium.org/downloads).

2. Navigate inside the folder and Install the requirements.

```sh
$ cd
$ pip install -r requirements.txt
```
3. Edit `config.py` and add your time-table into `timetable.txt`, see CONFIG.md for a detailed guide.

4. Run `python main.py` and rest will be taken care of :)

### Todo

 - Write Tests
 - Heroku One-click deploy app

## Contributing [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dwyl/esta/issues)

- Contributions are welcomed, please see CONTRIBUTING.md for detailed guide on how to contribute.

- New features are welcomed, as long as they don't break old ones.

License
----

MIT
