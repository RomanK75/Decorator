import requests
from pprint import pprint
import datetime
import os


def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            print(args, kwargs)
            result = old_function(*args, **kwargs)
            arguments = ""
            for arg in args:
                arguments += str(arg) + ", "
            for kwargs in kwargs.values():
                arguments += str(kwargs) + ", "
            logs = {
                "function_name": old_function.__name__,
                "args": arguments,
                "function_call_time": datetime.datetime.now().ctime(),
                "result": str(result),
            }
            with open(path, "a") as file:
                for key, value in logs.items():
                    file.write(f"{key}: {value}\n")
                file.write("\n")
            return result

        return new_function

    return __logger


def main():
    path = "quest_3.log"
    if os.path.exists(path):
        os.remove(path)

    @logger(path)
    def req(url):
        heroe_list = ["Hulk", "Captain America", "Thanos"]
        response = requests.get(url, timeout=5)
        all_heroes = response.json()
        searched_hero = {"name": "", "intelligence": 0}
        for heroe in all_heroes:
            if heroe["name"] in heroe_list:
                if heroe["powerstats"]["intelligence"] > searched_hero["intelligence"]:
                    searched_hero["name"], searched_hero["intelligence"] = (
                        heroe["name"],
                        heroe["powerstats"]["intelligence"],
                    )
        return searched_hero
        pprint(searched_hero)

    url = "https://akabab.github.io/superhero-api/api/all.json"
    req(url)


if __name__ == "__main__":
    main()
