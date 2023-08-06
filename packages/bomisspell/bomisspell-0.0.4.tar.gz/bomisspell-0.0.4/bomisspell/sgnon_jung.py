

def get_sngon_jug_options(syl_parts):
    """Return different combination sngonjug on syllable

    Args:
        syl_parts (dict): consit of all the possible component of a syllable which are sngonjug, mingzhi, jesjug and yangjug

    Returns:
        list: combinations that can be obtain using sngonjug
    """
    options = []
    mingzhi = syl_parts.get('mingzhi', '')
    jes_jug = syl_parts.get('jes_jug', '')
    yang_jug = syl_parts.get('yang_jug', '')
    options.append(f'{mingzhi}{jes_jug}{yang_jug}་')
    for sngon_jug in ['ག', 'ད', 'བ', 'མ', 'འ']:
        if sngon_jug == syl_parts.get('sngon_jug', ""):
            continue
        options.append(f'{sngon_jug}{mingzhi}{jes_jug}{yang_jug}་')
    return options