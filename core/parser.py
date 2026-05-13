import trafilatura


def extract_text(html):
    text = trafilatura.extract(html)

    return text or ""