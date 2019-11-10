import telegram, yaml, os

# Cache
def load_cache():
    return yaml.safe_load(open("data/cache.yaml", "r"))

def save_cache(cache):
    yaml.safe_dump(cache, open("data/cache.yaml", "w"))

# User data
def create_user_data(chat_id):
    default_data = load_user_data("__default")

    default_data["chat_id"] = chat_id

    return save_user_data(chat_id, default_data)

def save_user_data(chat_id, data):
    yaml.safe_dump(data, open("data/users/{}.yaml".format(chat_id), "w"))
    return data

def load_user_data(chat_id):
    return yaml.safe_load(open("data/users/{}.yaml".format(chat_id), "r"))

def has_user_data(chat_id):
    return os.path.exists("data/users/{}.yaml".format(chat_id))

# Form data
def create_form_data(form_id):
    return save_form_data(form_id, load_form_data("__default"))

def load_form_data(form_id):
    return yaml.safe_load(open("data/forms/{}.yaml".format(form_id), "r"))

def save_form_data(form_id, data):
    yaml.safe_dump(data, open("data/forms/{}.yaml".format(form_id), "w"))
    return data

def delete_form_data(form_id):
    os.remove("data/forms/{}.yaml".format(form_id))

def has_form_data(form_id):
    return os.path.exists("data/forms/{}.yaml".format(form_id))