from numba import prange
import json

# Dictionary to handle mentions, have to manually set
MENTIONS = {
    "@Arryaaan": "Aryan",
    "@Sujaylad": "Sujay",
    "@Timesup_biche": "Deepesh",
    "@b8mann": "Pratik",
    "@vichu1999": "Vishnu",
    "@K1368908643": "Akhil"
}

# Function to process text messages
def handle_mention(text):
    """Some text messages have mentions in them, this function handles them
    Args:
        text (str or list): str or 

    Returns:
        str: message with mentions processed into names
    """
    # If message is a string there are no mentions can skip
    if type(text) is str:
        return text
    
    processed = ""
    for message in text:
        if type(message) is str:
            processed += message
        else:
            if message["text"] in MENTIONS:
                processed += MENTIONS[message["text"]]
            else:
                processed += message["text"]
    return processed


def process_json(messages):
    """Processes the json file and returns a list of messages
    Args:
        json (dict): json file

    Returns:
        list: list of messages
    """
    users = dict()
    for idx in prange(len(messages)):
        message = messages[idx]
        if message["type"] == "message":
            user_name = message["from"]
            text = message["text"]
            if user_name not in users:
                users[user_name] = []
            
            users[user_name].append(handle_mention(text))
    
    return users


if __name__ == "__main__":
    
    # Set file path for the json containing the text messages downloaded from telegram
    JSON_FILE_PATH = "telegram_chats\\result.json"

    file = json.load(open(JSON_FILE_PATH, "r", encoding="utf-8"))

    messages = file["messages"]

    users = process_json(messages)
                
    user_names = list(users.keys())

    for user_name in user_names:
        user_messages = users[user_name]
        json_d = dict()
        json_d[user_name] = user_messages
        json.dump(json_d, open("data\\" + user_name + ".json", "w", encoding="utf-8"))