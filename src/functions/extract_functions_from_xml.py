from lxml import etree


def extract_function():
    with open("src/data.xml") as f:
        xml_data = f.read()

    root = etree.fromstring(xml_data)

    xml_list = find_function(root, 'is_button')

    return xml_list

def find_function(element, attribute_name, parent_tags=None):

    if parent_tags is None:
        parent_tags = []

    elements = []
    current_tag = ".".join(parent_tags + [element.tag])

    if element.get(attribute_name):
        elements.append((current_tag, [child.tag for child in element] if len(element) > 0 else element.text))
        
    for child in element:
        elements.extend(find_function(child, attribute_name, parent_tags + [element.tag]))
    
    return elements

def xml_to_list(root):
    if len(root) == 0:
        return root.text
    else:
        children = []
        for child in root:
            children.append(xml_to_list(child))
        return {root.tag : children}