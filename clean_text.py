
def deEmojify(text):
    """Remove emojis from text."""
    if text:
        return text.encode('ascii', 'ignore').decode('ascii')
    else:
        return None