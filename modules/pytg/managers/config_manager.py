import telegram, yaml

def load_settings_file(file_name="settings"):
    return yaml.safe_load(open("config/{}.yaml".format(file_name)))

def save_settings_file(settings, file_name="settings"):
    yaml.safe_dump(settings, open("config/{}.yaml".format(file_name), "w"))