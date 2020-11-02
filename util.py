"""
    Author:  Nathan Dow / Bitheral
    Created: 24/10/2020
"""
import json
import consts
import datetime
import os
import shutil
import ctypes

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


class Mouse:

    def __init__(self):
        self.pos = (0, 0)

    def update(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos


class Logger:

    def __init__(self):
        self.time = datetime.datetime.now()
        self.file = open("log.txt", "w")
        self.file.writelines(logo)
        for line in logo:
            print(line[:-1])
        self.date = {}

    def log(self, log, component, message):
        self.time = datetime.datetime.now()
        date = {
            "year": self.time.year,
            "month": self.time.month,
            "day": self.time.day,
            "hour": self.time.hour,
            "minute": self.time.minute,
            "second": self.time.second
        }
        self.date = date
        month = f"0{date['month']}" if date['month'] < 10 else str(date['month'])
        day = f"0{date['day']}" if date['day'] < 10 else str(date['day'])
        hour = f"0{date['hour']}" if date['hour'] < 10 else str(date['hour'])
        minute = f"0{date['minute']}" if date['minute'] < 10 else str(date['minute'])
        second = f"0{date['second']}" if date['second'] < 10 else str(date['second'])

        line = f"[{day}/{month}/{date['year']} {hour}:{minute}:{second}][{log.upper()}][{component.upper()}]: {message}"
        self.file.write(line + "\n")
        print(line)

    def debug(self, component, message):
        self.log("debug", component, message)

    def info(self, component, message):
        self.log("info", component, message)

    def warning(self, component, message):
        self.log("warning", component, message)

    def error(self, component, message):
        self.log("error", component, message)

    def stop(self):
        self.info("VALHALLA", "Stopping...")
        month = f"0{self.date['month']}" if self.date['month'] < 10 else str(self.date['month'])
        day = f"0{self.date['day']}" if self.date['day'] < 10 else str(self.date['day'])
        hour = f"0{self.date['hour']}" if self.date['hour'] < 10 else str(self.date['hour'])
        minute = f"0{self.date['minute']}" if self.date['minute'] < 10 else str(self.date['minute'])
        second = f"0{self.date['second']}" if self.date['second'] < 10 else str(self.date['second'])
        self.file.close()
        if not os.path.exists("logs"):
            os.mkdir("logs")
        shutil.move("log.txt", f"logs/")
        os.rename("logs/log.txt",
                  f"logs/{self.date['year']}-{month}-{day} {hour}-{minute}-{second}.txt")

        # print()
        # print(f"Saved to {os.getcwd()}\logs\{self.date['year']}-{self.month}-{self.day} {self.hour}-{self.minute}-{self.second}.txt")


def quit_game():
    consts.running = False
    consts.LOGGER.info("Pygame", "Stopping...")
    consts.LOGGER.stop()
    quit()


def constrain(value, low, high):
    return max(min(value, high), low)


def bind(value, currentStart, currentStop, targetStart, targetStop, withinBounds):
    new_value = (value - currentStart) / (currentStop - currentStart) * (targetStop - targetStart) + targetStart
    if not withinBounds:
        return new_value

    if targetStart < targetStop:
        return constrain(new_value, targetStart, targetStop)
    else:
        return constrain(new_value, targetStop, targetStart)


def create_settings_file():
    with open("settings.json", "w") as file:
        json.dump(consts.SETTINGS_TEMPLATE, file)
    file.close()

    consts.LOGGER.info("Valhalla", "Saving settings to file")


def save_to_settings_file():
    with open("settings.json", "w") as file:
        json.dump(consts.SETTINGS, file)
    file.close()

    consts.LOGGER.info("Valhalla", "Saving settings to file")


def load_settings_file():
    try:
        with open("settings.json", "r") as file:
            consts.LOGGER.info("Valhalla", "Loading settings from file")
            consts.SETTINGS = json.load(file)
        file.close()
        consts.LOGGER.info("Valhalla", "Finished loading setting from file")
    except FileNotFoundError:
        consts.LOGGER.error("Valhalla", "The settings file could not be read because the file does not exist")
        create_settings_file()
    except IOError as e:
        consts.LOGGER.error("Valhalla", f"An error occurred: {e}")
    finally:
        for template_key in consts.SETTINGS_TEMPLATE:
            if template_key not in consts.SETTINGS:
                consts.SETTINGS[template_key] = consts.SETTINGS_TEMPLATE[template_key]
                save_to_settings_file()

        if consts.SETTINGS['RESOLUTION']['WIDTH'] > ctypes.windll.user32.GetSystemMetrics(0):
            consts.SETTINGS['RESOLUTION']['WIDTH'] = ctypes.windll.user32.GetSystemMetrics(0)
        if consts.SETTINGS['RESOLUTION']['HEIGHT'] > ctypes.windll.user32.GetSystemMetrics(1):
            consts.SETTINGS['RESOLUTION']['HEIGHT'] = ctypes.windll.user32.GetSystemMetrics(1)
