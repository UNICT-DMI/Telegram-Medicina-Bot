import telegram

def load_markdown_document(document_id):
    in_file = open("markdown/{}.md".format(document_id), "r")
    text = in_file.read()
    in_file.close()

    return text 
