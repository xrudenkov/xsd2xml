import uuid
import requests

from xsd2xmlgenerator import Xsd2XmlGenerator

xml_name = str(uuid.uuid4())


def main():
    generator = Xsd2XmlGenerator(xsd_path="resources/xsd-test.xsd")
    generator.generate()
    generator.write(xml_path="resources/" + xml_name + ".xml")
    generator.validate(xml_path="resources/" + xml_name + ".xml")


def request():
    url = "http://localhost:8080/xml"
    headers = {'Content-Type': 'application/xml'}
    data = open('resources/' + xml_name + '.xml', 'r').read()
    r = requests.post(url, data=data, headers=headers)
    print(r)


if __name__ == "__main__":
    main()
