
def pretty_print_json(json):
    js_script = "<script>var data = {}\ndocument.getElementById(\"json\").innerHTML = JSON.stringify(data, undefined, 2);</script>".format(json)
    return "<body><pre id=\"json\" ></pre>{}</body>".format(js_script)