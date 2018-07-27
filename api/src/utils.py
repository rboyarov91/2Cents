from yattag import Doc

def pretty_print_json(json):
    doc, tag, text = Doc().tagtext()
    with tag('html'):
        with tag('pre', id="json"):
            text('')
        with tag('script'):
            text("var data = {}\ndocument.getElementById(\"json\").innerHTML = JSON.stringify(data, undefined, 2);".format(json))
    return doc.getvalue()