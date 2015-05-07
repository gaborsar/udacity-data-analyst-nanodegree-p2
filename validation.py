import re
import json
import collections


# valid Slovakian cities
SLOVAKIAN_CITIES = [
    u'Mu\u017ela',
    u'\u0160t\xfarovo'
]


# valid Hungarian cities
# not in standard data
VALID_CITIES = [
    u'Nagyegyh\xe1za',
    u'Tarj\xe1n-Torny\xf3puszta',
    u'S\xfctt\u0151-Bikolpuszta',
    u'S\xe1rszentmih\xe1ly-S\xe1rpentele',
    u'Kismaros-B\xf6rzs\xf6nyliget',
    u'Szigetmonostor-Hor\xe1ny',
    u'Domony-Domonyv\xf6lgy'
]


# valid Slovakian streets
SLOVAKIAN_STREETS = [
    u'R\xe1k\xf3cziho',
    u'Balassiho',
    u'Mateja Bela',
    u'\u0160tef\xe1nikova',
    u'\u017deliarsky svah',
    u'Kozmonautov',
    u'Jozefa Bema',
    u'Komensk\xe9ho ulica',
    u'Hlavn\xe1',
    u'Pet\u0151fiho',
    u'Ga\u0161tanov\xe1',
    u'Jesensk\xe9ho',
    u'Bocskaiho',
    u'Sv. \u0160tefana',
    u'Dru\u017estevn\xfd rad',
    u'Kossuthova',
    u'Bart\xf3kova',
    u'Mierov\xe1',
    u'V\xf6r\xf6smarthyho',
    u'M. Zr\xednskeho',
    u'Nov\xe1',
    u'Na vyhliadke',
    u'N\xe1m. slobody',
    u'Sv\xe4toplukova',
    u'Sz\xe9ch\xe9nyiho',
    u'Smetanova',
    u'Sobieskeho',
    u'Komensk\xe9ho'
]


# valid Hungarian streets
# not in standard data
VALID_STREETS = [
    u'Pet\u0151fi h\xedd (budai h\xeddf\u0151)',
    u'Feh\xe9rk\u0151',
    u'K\xf3s Majomh\xe1z',
    u'D\xe9li P\xe1lyaudvar, kereng\u0151',
    u'Nagytemplom',
    u'Gyermekliget',
    u'Budai',
    u'Fels\u0151v\xe1r',
    u'Duna korz\xf3',
    u'Elzamajor',
    u'Kanberek',
    u'\xdajbuda-k\xf6zpont',
    u'B\xe1nyatelep',
    u'N\xe9pliget',
    u'Remetes\xe9gpuszta',
    u'Szil\xe1rd Le\xf3',
    u'B\xe1tonyi',
    u'R\xf3zsahegyi',
    u'Hossz\xfas\xe9tat\xe9r',
    u'Palotakert',
    u'Sziv\xe1rv\xe1ny',
    u'M\xe1riav\xf6lgy',
    u'Kakashegy',
    u'Szent Andr\xe1s',
    u'K\xfclter\xfclet',
    u'Belter\xfclet',
    u'M0',
    u'Arbor\xe9tum',
    u'Kast\xe9lykert',
    u'R\xe1kos-patak',
    u'Z\xf6ldfa utca (III. ker\xfclet)',
    u'Z\xf6ldfa utca (XXII. ker\xfclet)'
]


# streets that cannot be cleaned
NONCLEANABLE_STREETS = [
    'Ny', 'Osz', 'TODO2', 'V', '13', '11', '9', '1163', '69'
]


# valid street types
# not in standard data
VALID_STREET_TYPES = [
    u'Stadion',
    u'f\u0151\xfat',
    u't\xf3',
    u'lak\xf3telep',
    u'k\xf6rvas\xfatsor',
    u'temet\u0151',
    u'lak\xf3negyed',
    u'telep',
    u'le\xe1gaz\xe1s',
    u'tanya',
    u'zug',
    u'k\xfclter\xfclet',
    u'Lpt.'
]


# special and valid postcodes
# post offices, museums, supermarkets, etc...
SPECIAL_POSTCODES = [
    '1312', '1503', '1605', '1751', '1752',
    '2542', '3003', '2103', '1060', '1090',
    '1189', '1220', '1227', '1120', '2042'
]


# valid but special house numbers
VALID_HOUSENUMBERS = [
    u'19/km pihen\u0151'
]


# use to identify valid Slovakian postcodes
re_postcode_slovakian = re.compile(r'^\d{3}\s\d{2}$')


# use to identify valid postcodes
re_housenumber = re\
    .compile(r'^(?:\d+(?:\/\w+){0,3})(?:[\,\-]\w+(?:\/\w+){0,3})*$')


class Validation:

    # standard data
    standard_data = []

    # unique lists of values of standard_data
    values = collections.defaultdict(set)

    def __init__(self, filename_standard_data):
        """
        Initialize validation class, load standard data.
        Source of the data:
        http://posta.hu/static/internet/download/Iranyitoszam_Internet.XLS
        """
        with open(filename_standard_data, 'r') as file_in:
            standard_data = json.load(file_in)
            for row in standard_data:
                self.standard_data.append(row)
                # keys: postcode, city, city_part,
                # district, street, steet_type
                for key in row.keys():
                    self.values[key].add(row[key])
                if 'city_part' in row:
                    city_full = row['city'] + '-' + row['city_part']
                    self.values['city'].add(city_full)

    def validate_key(self, key):
        """
        Check whether the given key is a valid MongoDB field name.
        http://docs.mongodb.org/manual/reference/limits/#Restrictions-on-Field-Names
        """
        return len(key) > 0 and key[0] != '$' and '.' not in key

    def validate_city(self, city):
        """ Check whether the given city is a valid city name. """
        return city in self.values['city'] or\
            city in VALID_CITIES or\
            city in SLOVAKIAN_CITIES

    def validate_postcode(self, postcode):
        """ Check whether the given postcode is a valid postcode. """
        return re_postcode_slovakian.search(postcode) or\
            postcode in self.values['postcode'] or\
            postcode in SPECIAL_POSTCODES

    def validate_street(self, street):
        """ Check whether the given street is a valid street. """
        street_type = street.split(' ')[-1]
        return street in self.values['street'] or\
            street in VALID_STREETS or\
            street in NONCLEANABLE_STREETS or\
            street in SLOVAKIAN_STREETS or\
            street_type in self.values['street_type'] or\
            street_type in VALID_STREET_TYPES

    def validate_housenumber(self, housenumber):
        """ Check whether the given house number is a valid house number. """
        return re_housenumber.search(housenumber) is not None or\
            housenumber in VALID_HOUSENUMBERS

    def validate(self, key, value):
        """ Check whether the given value is valid. """
        if key == 'key':
            return self.validate_key(value)
        if key == 'city':
            return self.validate_city(value)
        if key == 'postcode':
            return self.validate_postcode(value)
        if key == 'street':
            return self.validate_street(value)
        if key == 'housenumber':
            return self.validate_housenumber(value)
        # unknown key - assume it is valid
        return True
