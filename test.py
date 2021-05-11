def convert(phrase):
    phrase = phrase.replace(" ", "_")
    html = ""
    id = 0
    for char in phrase:
        html += f"""<span id="{id}">{char}</span>"""
        id += 1
    return html

print(convert("how are you"))
