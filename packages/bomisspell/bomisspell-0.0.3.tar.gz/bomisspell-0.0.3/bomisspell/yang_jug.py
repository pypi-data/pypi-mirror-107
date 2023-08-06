

def get_yang_jug_options(syl_parts):
    """Return different combination yangjug on syllable

    Args:
        syl_parts (dict): consit of all the possible component of a syllable which are sngonjug, mingzhi, jesjug and yangjug

    Returns:
        list: combinations that can be obtain using yangjug
    """
    options = []
    sngon_jug = syl_parts.get('sngon_jug', '')
    mingzhi = syl_parts.get('mingzhi', '')
    jes_jug = syl_parts.get('jes_jug', '')
    yang_jug = syl_parts.get('yang_jug', '')
    syl_parts['yang_jug'] = ''
    if yang_jug:
        if yang_jug == 'ད':
            options.append(f'{sngon_jug}{mingzhi}{jes_jug}་')
            options.append(f'{sngon_jug}{mingzhi}{jes_jug}ས་')
        else:
            options.append(f'{sngon_jug}{mingzhi}{jes_jug}་')
            options.append(f'{sngon_jug}{mingzhi}{jes_jug}ད་')
    else:
        options.append(f'{sngon_jug}{mingzhi}{jes_jug}ས་')
        options.append(f'{sngon_jug}{mingzhi}{jes_jug}ད་')
    return options  
