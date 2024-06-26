import dice
from termcolor import colored
import json
import os

mult = 5

spends = ["gp", "sp", "cp"]
skills = ["str", "dex", "con", "int", "wis", "cha"]

def save(data: dict):
    path = "C:/Users/N68029/Documents/crash.json"

    with open(path, "w") as f:
        f.write(json.dumps(data))

def load():
    path = "C:/Users/N68029/Documents/crash.json"

    if not os.path.isfile(path):
        with open(path, "x") as f:
            pass

    data: dict = {}

    with open(path, "r") as f:
        data = json.loads(f.read())

    return data

if __name__ == "__main__":
    while True:
        data = load()

        print("")
        val = input("query:  ")

        try:
            try:
                dice_str = val.strip()

                for skill in skills:
                    if skill in dice_str:
                        try:
                            if data[skill] is not None:
                                dice_str.replace(skill, str(data[skill]))

                            else:
                                data[skill] = input(f"No value exists for {{{skill}}}, what is the value? ")

                        except:
                                data[skill] = input(f"No value exists for {{{skill}}}, what is the value? ")
                                dice_str.replace(skill, str(data[skill]))

                response = dice.roll(dice_str)
                max_dice = dice_str.replace(" ", "").strip().split("+")[0].split("-")[0].split("d")[1]
                formatted = response.copy()

                for index, roll in enumerate(response):
                    if roll == 1:
                        formatted[index] = f"{colored(roll, 'red')}"

                    elif int(roll) == int(max_dice):
                        formatted[index] = f"{colored(roll, 'green')}"

                    else:
                        formatted[index] = f"{roll}"

                print(formatted)

                if len(response) > 1:
                    print(f"Total: {sum(response)}")

            except:
                if "d" in val.strip():
                    split = val.split(" ")
                    dice_str = split[1]
                    response = dice.roll(dice_str)
                    print(response)

                    if len(response) > 1:
                        print(f"Total: {sum(response)}")

                elif "psi" in val.strip():
                    data["dice"] = data["dice"] - 1
                    response = dice.roll('1d6')
                    print(f"Spent 1 psi dice: {response}")

                elif val.strip().startswith("s") and (val.strip().endswith(v) for v in spends):
                    arg = val.strip().split(" ")[1]

                    if "gp" in arg:
                        parsed = int(arg.removesuffix("gp"))
                        data["gp"] = data["gp"] - parsed
                        print(f"Spent {parsed}gp")

                    elif "sp" in arg:
                        parsed = int(arg.removesuffix("sp"))
                        rem = parsed % 100

                        if parsed > 100:
                            req = parsed / 100
                            data["gp"] = data["gp"] - req
                            print(f"Spent {req}gp")

                        while data["sp"] < parsed:
                            data["gp"] = data["gp"] - 1
                            data["sp"] = data["sp"] + 100
                            print(f"Converted 1gp to 100sp")

                        data["sp"] = data["sp"] - parsed
                        print(f"Spent {parsed % 100}sp")

                    elif "cp" in arg:
                        parsed = int(arg.removesuffix("cp"))
                        rem = parsed % 100

                        if parsed > 100:
                            req = parsed / 100

                            if data["sp"] >= req:
                                data["sp"] = data["sp"] - req
                                print(f"Spent {req}sp")

                            else:
                                data["gp"] = data["gp"] - 1
                                data["sp"] = data["sp"] + 100
                                print(f"Converted 1gp to 100sp")
                                data["sp"] = data["sp"] - req
                                print(f"Spent {req}sp")

                        while data["cp"] < parsed:
                            if data["sp"] >= 1:
                                data["sp"] = data["sp"] - 1
                                data["cp"] = data["cp"] + 100
                                print(f"Converted 1sp to 100cp")

                            else:
                                data["gp"] = data["gp"] - 1
                                data["sp"] = data["sp"] + 100
                                print(f"Converted 1gp to 100sp")
                                data["sp"] = data["sp"] - 1
                                data["cp"] = data["cp"] + 100
                                print(f"Converted 1sp to 100cp")

                        data["cp"] = data["cp"] - parsed
                        print(f"Spent {parsed % 100}cp")

                elif val.strip().startswith("c"):
                    split = val.split(" ")
                    level = int(split[1].strip())
                    sub = level * mult
                    data["current"] = int(data["current"]) - int(sub)
                    print(f"Spent {sub} spell points")
                    print(f"Remaining points: {data['current']}")

                elif val.strip() == "reset":
                    data["current"] = data["max"]
                    print(f"Remaining points: {data['current']}")
                    data["dice"] = 4
                    print(f"Remaining psi dice: {data['dice']}")

                elif val.strip() == "exit" or val.strip() == "q":
                    break

                else:
                    print("invalid command")

                save(data)
        except:
            print("invalid command")
