import re
import random
import yaml

from pathlib import Path

from bomisspell.utils import parse_syl
from bomisspell.sgnon_jung import get_sngon_jug_options
from bomisspell.mingzhi import get_mingzhi_options
from bomisspell.yang_jug import get_yang_jug_options

MINGZHI_MAPPING = yaml.safe_load(Path('./resources/mingzhi_mapping.yaml').read_text(encoding='utf-8'))

def get_misspelled_opt(syl_parts, mingzhi_mapping):
    """Return all the combination of misspelled syllable by shuffeling sngonjug, yangjug and replacing mingzhi by its similar pronounciation

    Args:
        syl_parts (dict): consit of all the possible component of a syllable which are sngonjug, mingzhi, jesjug and yangjug

    Returns:
        list: misspelled options of the syllable
    """
    options = []
    options += get_sngon_jug_options(syl_parts)
    options += get_mingzhi_options(syl_parts, mingzhi_mapping)
    options += get_yang_jug_options(syl_parts)
    return options

def get_misspelled_word(word, mingzhi_mapping = None):
    if not mingzhi_mapping:
        mingzhi_mapping = MINGZHI_MAPPING
    syl = word.replace('་', '')
    syl_parts = parse_syl(syl)
    misspelled_syls = get_misspelled_opt(syl_parts, mingzhi_mapping)
    result = random.sample(misspelled_syls, 3)
    result.append(word)
    return result
