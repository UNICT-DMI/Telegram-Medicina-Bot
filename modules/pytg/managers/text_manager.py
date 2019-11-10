import yaml, logging

def load_phrases(lang="en"):
    return yaml.safe_load(open("text/{}/phrases.yaml".format(lang), "r"))

def load_form_steps(form_name, lang="en"):
    return yaml.safe_load(open("text/{}/forms/{}/steps.yaml".format(lang, form_name), "r"))

def load_menu_headers(lang="en"):
    return yaml.safe_load(open("text/{}/menu_headers.yaml".format(lang), "r"))

def load_menu_titles(lang="en"):
    return yaml.safe_load(open("text/{}/menu_titles.yaml".format(lang), "r"))
