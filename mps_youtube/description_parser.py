"""
    Module for trying to parse and retrieve song data from descriptions
"""
import re
import random


def calculate_certainty(line):
    """ Determine if a line contains a  """
    certainty_indexes = [
        {'regex': r"(?:\(?(?:\d{0,4}:)?\d{0,2}:\d{0,2}\)?(?: - )?){1,2}",
         'weight': 1},
        {'regex': r"(([\w&()\[\]'\.\/ ]+)([ ]?[-]+[ ]?)([\w&()\[\]'\.\/ ]+))+",
         'weight': 0.75},
        {'regex': r"^([\d]+[. ]+)",
         'weight': 1}
    ]

    certainty = 0.0
    for method in certainty_indexes:
        if re.match(method['regex'], line):
            certainty += method['weight']

    return certainty / len(certainty_indexes)


def has_artist(text):
    """ Determine if the strìng has artist or not """
    regex = r"(?:([\w&()\[\]'\.\/ ]+)(?:[ ]?[-]+[ ]?)([\w&()\[\]'\.\/ ]+))+"
    return not re.match(regex, text)


def strip_string(text, single=False):
    """ Strip an artist-combo string """
    # Removes timestamps
    ts_reg = r"(?:\(?(?:\d{0,4}:)?\d{1,2}:\d{1,2}\)?(?: - )?){1,2}"
    text = re.sub(ts_reg, "", text)

    # Removes Tracknumbers.
    text = re.sub(r"^([\d]+[. ]+)", "", text)

    # Removes starting with non words
    text = re.sub(r"^[^\w&()\[\]'\.\/]", "", text, flags=re.MULTILINE)

    artist, track = None, None
    if not single:
        rgex = r"(?:([\w&()\[\]'\.\/ ]+)(?:[ ]?[-]+[ ]?)([\w&()\[\]'\.\/ ]+))+"
        artist, track = (re.findall(rgex, text)[0])
    else:
        track = text

    return artist, track


def long_substr(data):
    """ https://stackoverflow.com/a/2894073 """
    substr = ''
    if len(data) > 1 and len(data[0]) > 0:
        for i in range(len(data[0])):
            for j in range(len(data[0])-i+1):
                if j > len(substr) and is_substr(data[0][i:i+j], data):
                    substr = data[0][i:i+j]
    return substr


def is_substr(find, data):
    """ Check if is substring """
    if len(data) < 1 and len(find) < 1:
        return False
    for i, _ in enumerate(data):
        if find not in data[i]:
            return False
    return True


def artist_from_title(title):
    """ Try to determine an artist by doing a search on the video
        and try to find the most common element by n number of times looking
        for the most common substring in a subset of the results from youtube
    """
    query = {}
    query['q'] = title
    query['type'] = 'video'
    query['fields'] = "items(snippet(title))"
    query['maxResults'] = 50
    query['part'] = "snippet"

    results = None#pafy.call_gdata('search', query)['items']
    titles = [x['snippet']['title'].upper() for x in results]

    alts = {}
    for _ in range(100):
        random.shuffle(titles)
        subset = titles[:10]
        string = long_substr(subset).strip()
        if len(string) > 3:
            alts[string] = alts.get(string, 0) + 1

    best_string = None
    if len(alts) == 1:
        best_string = list(alts.keys())[0].capitalize()
    else:
        best_guess = 99999
        best_string = None

        for key in list(alts.keys()):
            current_guess = title.upper().find(key)
            if current_guess < best_guess:
                best_guess = current_guess
                best_string = key.capitalize()

    best_string = re.sub(r"([^\w]+)$", "", best_string)
    best_string = re.sub(r"^([^\w]+)", "", best_string)
    return best_string


def parse(text, title="Unknown"):
    """ Main function"""

    # Determine a certainty index for each line
    lines = []
    for line in text.split('\n'):
        lines.append((calculate_certainty(line), line))

    # Get average from all strings
    certainty_average = sum([x[0] for x in lines]) / len(lines)

    # Single out lines with above average certainty index
    lines = filter(lambda a: a is not None,
                   [x if x[0] > certainty_average else None for x in lines])

    # Determine if they are artist combo strings or only title
    cmbs = []
    for line in lines:
        is_ac = has_artist(line[1])
        cmbs.append(strip_string(line[1], is_ac))

    # No or very few tracklists will ommit aritsts or add artist information
    # on only a few select number of tracks, therefore we count entries with
    # and without artist, and remove the anomalities IF the number of
    # anomalities are small enough

    counters = {'has': 0, 'not': 0}
    for combo in cmbs:
        counters['has' if combo[0] else 'not'] += 1

    dominant = 'has' if counters['has'] > counters['not'] else 'not'

    diff = abs(counters['has'] - counters['not'])
    if diff > sum([counters['has'], counters['not']]):
        print("Too many anomalities detected")
        return []

    if dominant == 'has':
        cmbs = filter(lambda a: a is not None,
                      [x if x[0] is not None else None for x in cmbs])
    else:
        arti = artist_from_title(title)
        cmbs = filter(lambda a: a is not None,
                      [(arti, x[1]) if x[0] is None else None for x in cmbs])
    return list(cmbs)
