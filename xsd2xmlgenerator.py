import random
from xml.etree import ElementTree

import xmlschema
import rstr


def get_value_for_attribute(node_type):
    if node_type.local_name == "EAN" or node_type.local_name == "INN":
        ean_file = open(f'resources/{node_type.local_name}.txt', 'r')
        lines = ean_file.readlines()
        return str(int(lines[random.randrange(0, len(lines))]))
    else:
        value = list(node_type.facets.values())[0]
        if hasattr(value, "regexps"):
            regexps = list(node_type.facets.values())[0].regexps
            value = ''
            while value == '':
                value = rstr.xeger(regexps[0])
            return value
        else:
            return str(random.randrange(100, 10000))


def get_random_value():
    return int(random.randrange(2, 10))


class Xsd2XmlGenerator:

    def __init__(self, xsd_path):
        self.schema = xmlschema.XMLSchema(xsd_path)
        self.root = None

    def generate(self):
        # идем по всем рутовым элементам
        for xsd_node in self.schema.root_elements:
            self.root = ElementTree.Element(xsd_node.local_name)
            self._recur_func(xsd_node=xsd_node, xml_node=self.root, is_root=True)

    def _recur_func(self, xsd_node, xml_node, is_root=False):
        if not is_root:
            xml_node = ElementTree.SubElement(xml_node, xsd_node.local_name)

        # simple content
        if xsd_node.type.is_simple():
            xml_node.text = get_value_for_attribute(xsd_node.type)
        # complex types
        else:
            group = xsd_node.type.content._group
            for sub_node in group:
                if sub_node.occurs[1] is None:
                    i = get_random_value()
                else:
                    i = 1
                while i != 0:
                    i -= 1
                    if hasattr(sub_node, '_group'):
                        for item_node in sub_node._group:
                            self._recur_func(item_node, xml_node)
                        continue
                    self._recur_func(sub_node, xml_node)

        # attributes
        for attr, attr_obj in xsd_node.attributes.items():
            xml_node.attrib[attr] = get_value_for_attribute(attr_obj.type)

    def write(self, xml_path) -> None:
        tree = ElementTree.ElementTree(self.root)
        tree.write(xml_path, encoding="utf-8", xml_declaration=True)
        print("Generate " + xml_path + ".xml \nDone!!!")

    def validate(self, xml_path):
        self.schema.validate(xml_path)
        print(xml_path + " validates = " + str(self.schema.is_valid(xml_path)))
