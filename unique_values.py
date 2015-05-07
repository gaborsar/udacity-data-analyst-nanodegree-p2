import os
import collections
import xml.etree.cElementTree as ET


def collect_unique_values(filename):
    """ Collect unique values. """
    unique_values = collections.defaultdict(set)

    for _, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == 'node' or elem.tag == 'way':

            # get values from attributes
            for key in elem.attrib.keys():
                value = elem.attrib[key].strip()
                unique_values[key].add(value)

            # get values from tags
            for tag in elem.iter('tag'):
                if 'k' in tag.attrib and 'v' in tag.attrib:
                    key = tag.attrib['k']
                    value = tag.attrib['v'].strip()
                    unique_values[key].add(value)

    return unique_values


def write_values(filename, values):
    """ Write values into file. """
    with open(filename, 'w') as file_out:
        for value in values:
            if value is None:
                file_out.write('None\n')
            else:
                file_out.write(value.encode('utf-8') + '\n')


def main():
    dir = os.path.dirname(__file__)
    tasks = [
        ('keys', 'unique_keys.txt'),
        ('addr:city', 'unique_addr_city.txt'),
        ('addr:housenumber', 'unique_addr_housenumber.txt'),
        ('addr:postcode', 'unique_addr_postcode.txt'),
        ('addr:state', 'unique_addr_state.txt'),
        ('addr:street', 'unique_addr_street.txt')
    ]

    # collect all the unique values
    filename_in = os.path.join(dir, 'budapest_hungary.osm')
    unique_values = collect_unique_values(filename_in)
    unique_values['keys'] = set(unique_values.keys())

    # store all the unique values in "unique_<KEY>.txt" files
    for key, filename_out in tasks:
        write_values(filename_out, sorted(unique_values[key]))


main()
