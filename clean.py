import re


# full replacements for keys
KEY_MAP = {
    'Street': 'addr:street',
    'Telefon': 'phone',
    'hrsz': 'addr:hrsz',
    'postal_code': 'addr:postcode',
    'hrsz': 'addr:hrsz',
    'acess': 'access',
    'architectq': 'architect',
    'disusedhighway': 'disused:highway'
}


# full replacements for postcodes
POSTCODE_MAP = {
    '1130': '1131',
    '1231': '1213',
    '2128': '2821',
    '1519': '1111'
}


# full replacements for city names
CITY_MAP = {
    u'Alcsutdoboz': u'Alcs\xfatdoboz',
    u'1085': u'Budapest',
    u'budapest': u'Budapest',
    u'Budapest V': u'Budapest',
    u'Budapest,': u'Budapest',
    u'Budapeste': u'Budapest',
    u'hatvan': u'Hatvan',
    u'kisoroszi': u'Kisoroszi',
    u'nagyk\xe1ta': u'Nagyk\xe1ta',
    u'Pom\ufffdz': u'Pom\xe1z',
    u'\xe9rd': u'\xc9rd',
    u'\u0150\xe9cel': u'P\xe9cel',
    u'v\xe1c': u'V\xe1c',
    u'S\u0171lys\xe1p': u'S\xfclys\xe1p',
    u'Ag\xe1ed': u'G\xe1rdony-Ag\xe1rd',
    u'Ag\xe1rd': u'G\xe1rdony-Ag\xe1rd',
    u'Agosty\xe1n': u'Tata-Agosty\xe1n',
    u'Torny\xf3puszta': u'Tarj\xe1n-Torny\xf3puszta',
    u'Bikolpuszta': u'S\xfctt\u0151-Bikolpuszta',
    u'Dinny\xe9s': u'G\xe1rdony-Dinny\xe9s',
    u'B\xf6rzs\xf6nyliget': u'Kismaros-B\xf6rzs\xf6nyliget',
    u'Domonyv\xf6lgy': u'Domony-Domonyv\xf6lgy',
    u'undefined': None
}

# partial replacements for street names
STREET_REPLACE_MAP = {
    u'krt.': u'k\u00F6r\u00FAt',
    u'Tere': u'tere',
    u'Park': u'park',
    u'\u0171t': u'\u00FAt',
    u'\u00E9pcs\u00F6': u'\u00E9pcs\u0151',
    u'uca': u'utca',
    u'u.': u'utca',
    u' u ': u'utca',
    u'Szz\u00E1ll\u00E1s': u'Sz\u00E1ll\u00E1s',
    u'p\xe1lyaudvar': u'P\xe1lyaudvar',
    u'Kereng\u0151': u'kereng\u0151',
    u'\u00FAtca': u'utca'
}


# full replacements for street names
STREET_MAP = {
    u'Gy\u00F6rgyutca': u'Gy\u00F6rgy utca',
    u'Palota-kert': u'Palotakert',
    u'Mariav\u00F6lgy': u'M\u00E1riav\u00F6lgy',
    u'\xdajbuda K\xf6zpont': u'\xdajbuda-k\xf6zpont',
    u'Vaci ut': u'V\xe1ci \xfat',
    u'M\xe1ramaros ut': u'M\xe1ramaros \xfat',
    u'D\xf3zsa Gy\xf6rgyutca': u'D\xf3zsa Gy\xf6rgy utca',
    u'Bev\xe1s\xe1rl\xf3utca2': u'Bev\xe1s\xe1rl\xf3 utca 2',
    u'Stef\xe1nia ut': u'Stef\xe1nia \xfat',
    u'Z\xf6ldfa utca (XXII ker\xfclet)': u'Z\xf6ldfa utca (XXII. ker\xfclet)'
}


# identify Slovakian postcodes
re_postcode_slovakian = re.compile(r'^\d{3}\s\d{2}$')
re_postcode_slovakian_invalid = re.compile(r'^\d{5}$')


# use to identify typographical number values
re_hrsz = re.compile(r'hrsz', re.I)


# use to clean house number values
re_housenumber = [

    # '12/A fsz.' -> '12/A/1' (fsz. = ground floor)
    (re.compile(r'\s+FSZ\.'), '/1/'),

    # '123.' -> '123'
    (re.compile(r'\.'), ''),

    # '12/B ??' -> '12/B',
    (re.compile(r'\?'), ''),

    # '26;33' -> '26,33'
    (re.compile(r'\;'), ','),

    # '10, 12, 14' -> '10,12,14'
    (re.compile(r',\s+'), ','),

    # '1 / A - 3 / C' -> '1/A-3/C'
    (re.compile(r'\s+([\/\-])\s+'), r'\1'),

    # '4/' -> '4'
    # '13-' -> '13'
    (re.compile(r'[\/\-]$'), ''),

    # '16 A' -> '16/A'
    (re.compile(r'(\d)\s+([A-Z]{1})'), r'\1/\2'),

    # '100A-100B' -> '100/A-100/B'
    (re.compile(r'(\d)([A-Z])'), r'\1/\2')
]


# full replacements for house numbers
HOUSENUMBER_MAP = {
    # fix issue caused by str.upper
    u'19/KM PIHEN\u0150': u'19/km pihen\u0151'
}


# understand as: COLUMN_SHIFT_MAP[key_from][value_from][key_to] = value_to
COLUMN_SHIFT_MAP = {

    # cloumn shift issues in house numbers
    'housenumber': {
        '0135/36': {
            'hrsz': '0135/36'
        },
        '0152': {
            'hrsz': '0152'
        },
        '019/8 hrsz': {
            'hrsz': '019/8'
        },
        '0192/34': {
            'hrsz': '0192/34'
        },
        '06/79': {
            'hrsz': '06/79'
        },
        '081/15 hrsz': {
            'hrsz': '081/15'
        },
        '15/7 hrsz': {
            'hrsz': '15/7'
        }
    },

    # column shift issues in streets
    'street': {

        u'Szent Istv\xe1n k\xf6r\xfat 13': {
            'street': u'Szent Istv\xe1n k\xf6r\xfat',
            'housenumber': '13'
        },

        u'V\xe1ci \xfat 46/B': {
            'street': u'V\xe1ci \xfat ',
            'housenumber': '46/B'
        },

        u'V\xe1ci \xfat 46/B.': {
            'street': u'V\xe1ci \xfat',
            'housenumber': '46/B'
        },

        u'Gy\xf6ngyvir\xe1g utca (L\xf3nyaytelep) 8': {
            'street': u'Gy\xf6ngyvir\xe1g utca',
            'housenumber': '8'
        },

        u'Vak Botty\xe1n utca 75/a': {
            'street': u'Vak Botty\xe1n utca',
            'housenumber': '75/a'
        },

        u'Dob utca 55': {
            'street': u'Dob utca',
            'housenumber': '55'
        },

        u'Bev\xe1s\xe1rl\xf3 utca 2': {
            'street': u'Bev\xe1s\xe1rl\xf3 utca',
            'housenumber': '2'
        },

        u'Liszenk\xf3 telep 0318 hrsz.': {
            'street': u'Liszenk\xf3 telep',
            'hrsz': '0318'
        },

        u'K\xfclter\xfclet 0195/18 hrsz': {
            'street': u'K\xfclter\xfclet',
            'hrsz': '0195/18'
        }
    }
}


def clean_key(key, key_map=KEY_MAP):
    """ Clean a key. """
    key = key.replace('.', ':')
    if key in key_map:
        return key_map[key]
    return key


def clean_postcode(postcode, postcode_map=POSTCODE_MAP):
    """ Clean a postcode. """
    if re_postcode_slovakian.search(postcode) is not None:
        return postcode
    if re_postcode_slovakian_invalid.search(postcode) is not None:
        return '{0} {1}'.format(postcode[:3], postcode[3:])
    if postcode in postcode_map:
        return postcode_map[postcode]
    return postcode


def clean_city(city, city_map=CITY_MAP):
    """ Clean a city name. """
    city = city.replace(' - ', '-')
    if city in city_map:
        return city_map[city]
    return city


def clean_street(street,
                 street_replace_map=STREET_REPLACE_MAP,
                 street_map=STREET_MAP):
    """ Clean a street name. """
    for key in street_replace_map.keys():
        if key in street:
            street = street.replace(key, street_replace_map[key])
    if street in street_map:
        street = street_map[street]
    return street[0].capitalize() + street[1:]


def clean_state(state):
    """ Clean a state name. """
    return state.title()


def clean_housenumber(housenumber, housenumber_map=HOUSENUMBER_MAP):
    """ Clean a house number. """
    # do not clean typographical numbers
    if re_hrsz.search(housenumber) is not None:
        return housenumber
    # standardize characters to uppercase
    housenumber = housenumber.upper()
    # replace UNICODE minus sign with dash symbol
    housenumber = housenumber.replace(u'\u2013', '-')
    # standardize format
    for pattern, replacement in re_housenumber:
        if pattern.search(housenumber) is not None:
            housenumber = pattern.sub(replacement, housenumber)
    housenumber = housenumber.strip()
    if housenumber in housenumber_map:
        return housenumber_map[housenumber]
    return housenumber


def clean_value(key, value):
    """ Clean a key and a value. """
    key = clean_key(key)
    if key == 'addr:postcode':
        value = clean_postcode(value)
    if key == 'addr:city':
        value = clean_city(value)
    if key == 'addr:street':
        value = clean_street(value)
    if key == 'addr:state':
        value = clean_state(value)
    if key == 'addr:housenumber':
        value = clean_housenumber(value)
    return key, value


def clean_address(address):
    """ Clean an address, fix column shift errors. """
    for key_from in COLUMN_SHIFT_MAP.keys():
        if key_from in address:
            value_from = address[key_from]
            if value_from in COLUMN_SHIFT_MAP[key_from]:
                values_to = COLUMN_SHIFT_MAP[key_from][value_from]
                keys_to = values_to.keys()
                # update keys
                for key_to in keys_to:
                    address[key_to] = values_to[key_to]
                # delete the original key if it has not been updated
                if key_from not in keys_to:
                    del address[key_from]
    return address
