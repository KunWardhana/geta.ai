def sanitize_output(text: str) -> str:
        import re
        
        text = text.strip()
        regex = re.compile(r"^\s*```(\w+)?|```\s*$")
        text = regex.sub("", text).strip()

        if re.search(r'^[^"]*"$', text):
            text = text[:-1]

        if re.search(r'^"[^"]*$', text):
            text = text[1:]

        return text
    
def remove_new_lines(text: str) -> str:
    text = text.replace('\n', ' ')
    text = text.replace('  ', ' ')
    
    return text