import os
import codecs
import json
import xml.etree.cElementTree as ET
import clean


CREATED = ['version', 'changeset', 'timestamp', 'user', 'uid']
POS = ['lat', 'lon']


def validate_key(key):
    """
    Check whether the given key is a valid MongoDB field name.
    http://docs.mongodb.org/manual/reference/limits/#Restrictions-on-Field-Names
    """
    return len(key) > 0 and key[0] != '$' and '.' not in key


def shape_element(element):
    """ Shape an element. """

    # we are only interested in <bode> and <way> elements
    if element.tag not in ['node', 'way']:
        return None

    node = {}

    # store node type
    node['type'] = element.tag

    # parse attributes
    for key in element.attrib.keys():
        value = element.attrib[key]
        key, value = clean.clean_value(key, value)

        # skip problematic keys
        if validate_key(key) is False:
            continue

        # store 'pos' keys
        if key in POS:
            if 'pos' not in node:
                node['pos'] = []
            node['pos'].insert(0, float(value))

        # store 'created' keys
        elif key in CREATED:
            if 'created' not in node:
                node['created'] = {}
            node['created'][key] = value

        # store all other keys
        else:
            node[key] = value

    # parse <tag> elements
    for tag in element.iter('tag'):
        key = tag.attrib['k']
        value = tag.attrib['v']
        key, value = clean.clean_value(key, value)

        # skip problematic keys
        if validate_key(key) is False:
            continue

        # store address details
        if key[:5] == 'addr:':

            # skip if more than one colons found
            if ':' in key[5:]:
                continue

            # store address
            if 'address' not in node:
                node['address'] = {}
            node['address'][key[5:]] = value

        # store all other keys
        else:
            node[key] = value

    # parse <nd> elements
    for nd in element.iter('nd'):
        if 'ref' in nd.attrib:
            if 'node_refs' not in node:
                node['node_refs'] = []
            node['node_refs'].append(nd.attrib['ref'])

    # clean address, solve column shift issues
    if 'address' in node:
        node['address'] = clean.clean_address(node['address'])

    return node


def main():
    dir = os.path.dirname(__file__)
    filename_in = os.path.join(dir, 'budapest_hungary.osm')
    filename_out = os.path.join(dir, 'budapest_hungary.json')
    with codecs.open(filename_out, 'w', 'utf-8') as file_out:
        for _, element in ET.iterparse(filename_in):
            node = shape_element(element)
            if node is not None:
                file_out.write(json.dumps(node, ensure_ascii=False) + '\n')


main()
