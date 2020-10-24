"""
    Author:  Nathan Dow / Bitheral
    Created: 24/10/2020
"""
import json
import consts
import datetime

logo = [
    "\n"
    "  _______ _    _ ______   ____  ______ ______ _____   ____________ _____  _  ________ _____\n",
    " |__   __| |  | |  ____| |  _ \|  ____|  ____|  __ \ |___  /  ____|  __ \| |/ /  ____|  __ \\\n",
    "    | |  | |__| | |__    | |_) | |__  | |__  | |__) |   / /| |__  | |__) | ' /| |__  | |__) |\n",
    "    | |  |  __  |  __|   |  _ <|  __| |  __| |  _  /   / / |  __| |  _  /|  < |  __| |  _  /\n",
    "    | |  | |  | | |____  | |_) | |____| |____| | \ \  / /__| |____| | \ \| . \| |____| | \ \\\n",
    "    |_|  |_|  |_|______| |____/|______|______|_|  \_\/_____|______|_|  \_\_|\_\______|_|  \_\\\n",
    "\n\n",
    "=========================================================================================================\n"
]


class Logger:

    def __init__(self):
        launch_time = datetime.datetime.now()
        # Add file logging capability
        self.file = open("log.txt", "w")
        self.file.writelines(logo)

    def log(self, log, component, message):
        currentTime = datetime.datetime.now()
        date = {
            "year": currentTime.year,
            "month": currentTime.month,
            "day": currentTime.day,
            "hour": currentTime.hour,
            "minute": currentTime.minute,
            "second": currentTime.second
        }
        month = f"0{date['month']}" if date['month'] < 10 else str(date['month'])
        day = f"0{date['day']}" if date['day'] < 10 else str(date['day'])
        hour = f"0{date['hour']}" if date['hour'] < 10 else str(date['hour'])
        minute = f"0{date['minute']}" if date['minute'] < 10 else str(date['minute'])
        second = f"0{date['second']}" if date['second'] < 10 else str(date['second'])

        line = f"[{day}/{month}/{date['year']} {hour}:{minute}:{second}][{log.upper()}][{component.upper()}]: {message}"
        self.file.write(line + "\n")
        print(line)

    def info(self, component, message):
        self.log("info", component, message)

    def warning(self, component, message):
        self.log("warning", component, message)

    def error(self, component, message):
        self.log("error", component, message)

    def stop(self):
        self.info("VALHALLA", "Stopping...")
        self.file.close()


def create_settings_file():
    with open("settings.json", "w") as file:
        json.dump(consts.SETTINGS, file)
    file.close()

    consts.LOGGER.info("Valhalla", "Saving settings to file")


def load_settings_file():
    with open("settings.json") as file:
        consts.LOGGER.info("Valhalla", "Loading settings from file")
        consts.SETTINGS = json.load(file)
    file.close()
    consts.LOGGER.info("Valhalla", "Finished loading setting from file")
