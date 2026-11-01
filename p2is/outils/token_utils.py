import re
from p2is.outils.audit_eboot import encode_string

TAG_REGEX = re.compile(r'(<[0-9A-Fa-f]{4}>|<S[0-9A-Fa-f]{4}>|<001E>|\[SP\])')

def tokenize(text):
    """Splits text into atomic units: tags (<XXXX>, [SP]), or single characters."""
    tokens = []
    pos = 0
    for m in TAG_REGEX.finditer(text):
        start, end = m.span()
        if start > pos:
            for ch in text[pos:start]:
                tokens.append(ch)
        tokens.append(m.group(0))
        pos = end
    if pos < len(text):
        for ch in text[pos:]:
            tokens.append(ch)
    return tokens

def safe_fit(text, slot_size):
    """Ensures text fits into slot_size without breaking tags.
    If text ends with a tag (like <FF03>), preserves that trailing tag.
    """
    enc = encode_string(text.replace('[SP]', '\u3000'))
    if len(enc) <= slot_size:
        return text

    # Extract any trailing tag(s) like <FF03> or <0004><FF03>
    trailing_tags = []
    temp = text
    while True:
        m = re.search(r'(<[0-9A-Fa-f]{4}>|<S[0-9A-Fa-f]{4}>|\[SP\])$', temp)
        if m:
            trailing_tags.insert(0, m.group(0))
            temp = temp[:m.start()]
        else:
            break

    trail_str = ''.join(trailing_tags)
    trail_bytes = len(encode_string(trail_str.replace('[SP]', '\u3000')))
    avail_bytes = slot_size - trail_bytes

    if avail_bytes < 0:
        # Extreme edge case: slot cannot even hold trailing tags
        return ""

    tokens = tokenize(temp)
    out_tokens = []
    current_bytes = 0
    for tok in tokens:
        tok_bytes = len(encode_string(tok.replace('[SP]', '\u3000')))
        if current_bytes + tok_bytes <= avail_bytes:
            out_tokens.append(tok)
            current_bytes += tok_bytes
        else:
            break

    res = ''.join(out_tokens) + trail_str
    return res

