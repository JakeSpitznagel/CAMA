from json import load


def tokenize_line(line):
    delimiters = [c for c in " ;:,.(){}[]<>=+-/*\n"]
    line_tokens = []
    curr = ""
    for c in line:
        if c in delimiters:
            if curr:
                line_tokens.append(curr)
            if c != " " and c != "\n":
                line_tokens.append(c)
            curr = ""
        else:
            curr += c
    return line_tokens


def tokenize(fname):
    with open(fname, 'r') as f:
        tokens = []
        for line in f.readlines():
            tokens.append(tokenize_line(line))
        return tokens


def classify_line(line, src):
    with open(src, 'r') as f:
        classifications = load(f)
    token = tokenize_line(line)[0] if tokenize_line(line) else ''
    result = None
    for classification, members in classifications.items():
        if token in members:
            result = classification
    return result


if __name__ == "__main__":
    f = "toke.py"
    with open(f, 'r') as f:
        for line in f.readlines():
            print(classify_line(line, "pyclassification.json"))
