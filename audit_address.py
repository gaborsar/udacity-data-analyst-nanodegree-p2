import os
import xml.etree.cElementTree as ET
import clean
from validation import Validation
import collections


KEYS = ['addr:city', 'addr:postcode', 'addr:street', 'addr:housenumber']


def get_address(element, keys=KEYS):
    """ Get and address dictionary from an XML element. """

    if element.tag not in ['node', 'way']:
        return None

    address = None
    for tag in element.iter('tag'):
        if 'k' in tag.attrib and 'v' in tag.attrib:
            key = tag.attrib['k']
            value = tag.attrib['v'].strip()
            key, value = clean.clean_value(key, value)
            if key in KEYS and value is not None:
                if address is None:
                    address = {}
                address[key[5:]] = value

    if address is not None:
        address = clean.clean_address(address)

    return address


def main():
    validation = Validation('standard_data.json')
    invalid = collections.defaultdict(set)

    dir = os.path.dirname(__file__)
    filename_in = os.path.join(dir, 'budapest_hungary.osm')
    for _, element in ET.iterparse(filename_in):
        address = get_address(element)
        if address is not None:

            # validate each keys one by one
            for key in address.keys():
                value = address[key]

                # do not have to validate if we know it is invalid
                if value not in invalid[key]:

                    # if invalid
                    if validation.validate(key, value) is False:

                        # store it to make sure we do not repeat this report
                        invalid[key].add(value)

                        # report the invalid value
                        print 'Invalid {0}: "{1}"'\
                            .format(key, value.encode('utf-8'))


main()
