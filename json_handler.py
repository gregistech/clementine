import json
import asyncio
starboard_filepath = "starboard.json"
async def save_starboard(msgId, starMsgId, count):
        currStarboard = await get_starboard()
        currStarboard.append({"msgId": msgId, "starMsgId": starMsgId, "count": count})
        with open(starboard_filepath, "w") as out:
            json.dump(currStarboard, out)
async def get_starboard():
    try:
        with open(starboard_filepath, "r") as out:
            return json.loads(out.read())
    except FileNotFoundError:
        with open(starboard_filepath, "w") as out:
            out.write("[]")
            return json.loads("[]")
async def change_starboard(msgId, newCount):
    currStarboard = await get_starboard()
    counter = 0
    for v in currStarboard:
        if v["msgId"] == msgId:
             currStarboard[counter]["count"] = newCount
             break
        counter += 1
    with open(starboard_filepath, "w") as out:
        json.dump(currStarboard, out)
    return newCount
async def remove_starboard(msgId):
    currStarboard = await get_starboard()
    counter = 0
    for v in currStarboard:
        if v["msgId"] == msgId:
             del currStarboard[counter]
             break
        counter += 1
    with open(starboard_filepath, "w") as out:
        json.dump(currStarboard, out)
    return True

config_filepath = "config.json"
async def get_config_contents():
    with open(config_filepath, "r") as out:
        config = json.loads(out.read())
        return config

async def change_config_value(key, new_value, guild_id):
    config = await get_config_contents()    
    try:
        config[str(guild_id)][str(key)] = new_value
    except KeyError:
        config[str(guild_id)] = config["default"]
        config[str(guild_id)][str(key)] = new_value

    with open(config_filepath, "w") as out:
        config = json.dump(config, out)


