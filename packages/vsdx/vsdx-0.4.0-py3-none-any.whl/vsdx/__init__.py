from __future__ import annotations
import zipfile
import shutil
import os
import re
from jinja2 import Template
from typing import Optional, List

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

import xml.dom.minidom as minidom   # minidom used for prettyprint

namespace = "{http://schemas.microsoft.com/office/visio/2012/main}"  # visio file name space


# utility functions
def to_float(val: str):
    try:
        if val is None:
            return
        return float(val)
    except ValueError:
        return 0.0


class VisioFile:
    """Represents a vsdx file

    :param filename: filename the :class:`VisioFile` was created from
    :type filename: str
    :param pages: a list of pages in the VisioFile
    :type pages: list of :class:`Page`
    :param master_pages: a list of master pages in the VisioFile
    :type master_pages: list of :class:`Page`

    Contains :class:`Page`, :class:`Shape`, :class:`Connect` and :class:`Cell` sub-classes
    """
    def __init__(self, filename, debug: bool = False):
        """VisioFile constructor

        :param filename: the vsdx file to load and create the VisioFile object from
        :type filename: str
        :param debug: enable/disable debugging
        :type debug: bool, default to False
        """
        self.debug = debug
        self.filename = filename
        if debug:
            print(f"VisioFile(filename={filename})")
        self.directory = f"./{filename.rsplit('.', 1)[0]}"
        self.pages_xml = None
        self.pages_xml_rels = None
        self.content_types_xml = None
        self.app_xml = None
        self.page_xml_by_file_path = dict()  # list of XML objects by file path, populated by open_vsdx_file()
        self.pages = list()  # list of Page objects, populated by open_vsdx_file()
        self.page_max_ids = dict()  # maximum shape id, used to add new shapes with a unique Id
        self.master_page_xml_by_file_path = dict()  # list of XML objects by file path, populated by open_vsdx_file()
        self.master_pages = list()  # list of Page objects, populated by open_vsdx_file()
        self.open_vsdx_file()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_vsdx()

    @staticmethod
    def pretty_print_element(xml: Element) -> str:
        if type(xml) is Element:
            return minidom.parseString(ET.tostring(xml)).toprettyxml()
        else:
            return f"Not an Element. type={type(xml)}"

    def open_vsdx_file(self) -> dict:  # returns a dict of each page as ET with filename as key
        with zipfile.ZipFile(self.filename, "r") as zip_ref:
            zip_ref.extractall(self.directory)

        # load each page file into an ElementTree object
        self.load_pages()
        self.load_master_pages()

        return self.page_xml_by_file_path

    def _pages_filename(self):
        page_dir = f'{self.directory}/visio/pages/'
        pages_filename = page_dir + 'pages.xml'  # pages.xml contains Page name, width, height, mapped to Id
        return pages_filename

    def load_pages(self):
        rel_dir = f'{self.directory}/visio/pages/_rels/'
        page_dir = f'{self.directory}/visio/pages/'

        rel_filename = rel_dir + 'pages.xml.rels'
        rels = file_to_xml(rel_filename).getroot()  # rels contains page filenames
        self.pages_xml_rels = file_to_xml(rel_filename)  # store pages.xml.rels so pages can be added or removed
        if self.debug:
            print(f"Relationships({rel_filename})", VisioFile.pretty_print_element(rels))
        relid_page_dict = {}

        for rel in rels:
            rel_id=rel.attrib['Id']
            page_file = rel.attrib['Target']
            relid_page_dict[rel_id] = page_file

        pages_filename = page_dir + 'pages.xml'  # pages contains Page name, width, height, mapped to Id
        pages = file_to_xml(pages_filename).getroot()  # this contains a list of pages with rel_id and filename
        self.pages_xml = file_to_xml(pages_filename)  # store xml so pages can be removed
        if self.debug:
            print(f"Pages({pages_filename})", VisioFile.pretty_print_element(pages))
        page_dict = {}  # dict with filename as index

        for page in pages:  # type: Element
            rel_id = page[1].attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            page_name = page.attrib['Name']

            page_path = page_dir + relid_page_dict.get(rel_id, None)
            page_dict[page_path] = file_to_xml(page_path)

            if self.debug:
                print(f"Page({page_path})", VisioFile.pretty_print_element(page_dict[page_path].getroot()))
            self.page_max_ids[page_path] = 0  # initialise page_max_ids dict for each page

            self.pages.append(VisioFile.Page(file_to_xml(page_path), page_path, page_name, self))

        self.page_xml_by_file_path = page_dict

        self.content_types_xml = file_to_xml(f'{self.directory}/[Content_Types].xml')
        # TODO: add correctness cross-check. Or maybe the other way round, start from [Content_Types].xml
        #       to get page_dir and other paths...

        self.app_xml = file_to_xml(f'{self.directory}/docProps/app.xml')

    def load_master_pages(self):
        # get data from /visio/masters folder
        master_rel_path = f'{self.directory}/visio/masters/_rels/masters.xml.rels'

        master_rels_data = file_to_xml(master_rel_path)
        master_rels = master_rels_data.getroot() if master_rels_data else None
        if self.debug:
            print(f"Master Relationships({master_rel_path})", VisioFile.pretty_print_element(master_rels))
        if master_rels:
            for rel in master_rels:
                master_id = rel.attrib.get('Id')
                master_path = f"{self.directory}/visio/masters/{rel.attrib.get('Target')}"  # get path from rel
                master_data = file_to_xml(master_path)  # contains master page xml
                master = master_data.getroot() if master_data else None
                if master:
                    self.master_page_xml_by_file_path[master_path] = master  # add master xml to VisioFile.master_pages
                    master_page = VisioFile.Page(master_data, master_path, master_id, self)
                    self.master_pages.append(master_page)
                    if self.debug:
                        print(f"Master({master_path}, id={master_id})", VisioFile.pretty_print_element(master))

        masters_path = f'{self.directory}/visio/masters/masters.xml'
        masters_data = file_to_xml(masters_path)  # contains more info about master page (i.e. Name, Icon)
        masters = masters_data.getroot() if masters_data else None
        if self.debug:
            print(f"Masters({masters_path})", VisioFile.pretty_print_element(masters))

        return

    def get_page(self, n: int):
        try:
            return self.pages[n]
        except IndexError:
            return None

    def get_page_names(self):
        return [p.name for p in self.pages]

    def get_page_by_name(self, name: str):
        """Get page from VisioFile with matching name

                :param name: The name of the new page
                :type name: str, optional

                :return: :class:`Page` object representing the page (or None if not found)
                """
        for p in self.pages:
            if p.name == name:
                return p

    def remove_page_by_index(self, index: int):
        """Remove zero-based nth page from VisioFile object

        :param index: Zero-based index of the page
        :type index: int

        :return: None
        """

        # remove Page element from pages.xml file - zero based index
        # todo:  similar function by page id, and by page title
        page = self.pages_xml.find(f"{namespace}Page[{index+1}]")
        if page:
            self.pages_xml.getroot().remove(page)
            page = self.pages[index]  # type: VisioFile.Page
            del self.page_xml_by_file_path[page.filename]
            del self.pages[index]

    def add_page_at(self, index: int, name: Optional[str] = None) -> VisioFile.Page:
        """Add a new page at the specified index of the VisioFile

        :param index: zero-based index where the new page will be placed
        :type index: int

        :param name: The name of the new page
        :type name: str, optional

        :return: :class:`Page` object representing the new page
        """

        # Create visio\pages\pageX.xml file
        # Add to visio\pages\_rels\pages.xml.rels
        # Add to visio\pages\pages.xml
        # Add to [Content_Types].xml
        # Add to docProps\app.xml

        page_dir = f'{self.directory}/visio/pages/'

        # create page.xml
        #TODO: figure out the best way to define this default page XML
        new_page_xml = ET.ElementTree(ET.fromstring(f"<?xml version='1.0' encoding='utf-8' ?><PageContents xmlns='{namespace[1:-1]}' xmlns:r='http://schemas.openxmlformats.org/officeDocument/2006/relationships' xml:space='preserve'/>"))
        new_page_filename = f'page{len(self.page_xml_by_file_path) + 1}.xml'
        new_page_path = page_dir+new_page_filename

        # update pages.xml.rels
        max_relid = max(self.pages_xml_rels.getroot(), key=lambda rel: int(rel.attrib['Id'][3:]), default=None)  # 'rIdXX' -> XX
        max_relid = int(max_relid.attrib['Id'][3:]) if max_relid is not None else 0
        new_page_relid = f'rId{max_relid + 1}'  # Most likely will be equal to len(self.pages)+1

        new_page_rel = {
            'Target': new_page_filename,
            'Type'  : 'http://schemas.microsoft.com/visio/2010/relationships/page',
            'Id'    : new_page_relid
        }
        self.pages_xml_rels.getroot().append(Element('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship', new_page_rel))

        # update pages.xml
        page_names = [page.name for page in self.pages]
        new_page_name = name or f'Page-{len(self.page_xml_by_file_path) + 1}'
        i = 1
        while new_page_name in page_names:
            new_page_name = f'{new_page_name}-{i}'  # Page-X-i
            i += 1

        max_page_id = max(self.pages_xml.getroot(), key=lambda page: int(page.attrib['ID']))
        max_page_id = int(max_page_id.attrib['ID'])

        new_page_attribs = {
            'ID'   : str(max_page_id + 1),
            'NameU': new_page_name,
            'Name' : new_page_name
        }

        new_pagesheet_attribs = {
            'FillStyle': '0',
            'LineStyle': '0',
            'TextStyle': '0'
        }
        new_page_rel = {
            '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id' : new_page_relid
        }

        new_page_element = Element(f'{namespace}Page', new_page_attribs)
        # TODO: figure out the best way to define this default pagesheet XML
        # For example, python-docx has a 'template.docx' file which is copied.
        new_pagesheet_element = Element(f'{namespace}PageSheet', new_pagesheet_attribs)
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageWidth', 'V':'8.26771653543307'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageHeight', 'V':'11.69291338582677'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwOffsetX', 'V':'0.1181102362204724'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwOffsetY', 'V':'-0.1181102362204724'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageScale', 'U':'MM', 'V':'0.03937007874015748'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'DrawingScale', 'U':'MM', 'V':'0.03937007874015748'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'DrawingSizeType', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'DrawingScaleType', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'InhibitSnap', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageLockReplace', 'U':'BOOL', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageLockDuplicate', 'U':'BOOL', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'UIVisibility', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwType', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwObliqueAngle', 'V':'0'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'ShdwScaleFactor', 'V':'1'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'DrawingResizeType', 'V':'1'}))
        new_pagesheet_element.append(Element(f'{namespace}Cell', {'N':'PageShapeSplit', 'V':'1'}))

        new_page_element.append(new_pagesheet_element)
        new_page_element.append(Element(f'{namespace}Rel', new_page_rel))
        self.pages_xml.getroot().insert(index, new_page_element)

        # update [Content_Types].xml
        content_types = self.content_types_xml.getroot()
        content_types_attribs = {
            'PartName'   : f'/visio/pages/{new_page_filename}',
            'ContentType': 'application/vnd.ms-visio.page+xml'
        }
        cont_types_namespace = '{http://schemas.openxmlformats.org/package/2006/content-types}'
        content_types_element = Element(f'{cont_types_namespace}Override', content_types_attribs)

        # add the new element after the last such element
        # first find the index:
        all_page_overrides = content_types.findall(
            f'{cont_types_namespace}Override[@ContentType="application/vnd.ms-visio.page+xml"]'
        )
        idx = list(content_types).index(all_page_overrides[-1])

        # then add it:
        content_types.insert(idx+1, content_types_element)

        # update app.xml
        # strictly speaking, this is optional, but we're doing what MS Visio does.
        ext_prop_namespace = '{http://schemas.openxmlformats.org/officeDocument/2006/extended-properties}'
        vt_namespace = '{http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes}'

        TitlesOfParts = self.app_xml.getroot().find(f'{ext_prop_namespace}TitlesOfParts')
        vector = TitlesOfParts.find(f'{vt_namespace}vector')

        lpstr = Element(f'{vt_namespace}lpstr')
        lpstr.text = new_page_name
        vector.append(lpstr)
        vector_size = int(vector.attrib['size'])
        vector.set('size', str(vector_size+1))

        # Update VisioFile object
        new_page = VisioFile.Page(new_page_xml, new_page_path, new_page_name, self)

        self.pages.append(new_page)
        self.page_xml_by_file_path[new_page_path] = new_page_xml
        self.page_max_ids[new_page_path] = 0

        return new_page

    def add_page(self, name: Optional[str] = None) -> VisioFile.Page:
        """Add a new page at the end of the VisioFile

        :param name: The name of the new page
        :type name: str, optional

        :return: Page object representing the new page
        """
        end_of_file = len(self.pages)
        return self.add_page_at(end_of_file, name)

    def get_shape_max_id(self, shape_xml: ET.Element):
        max_id = int(self.get_shape_id(shape_xml))
        if shape_xml.attrib['Type'] == 'Group':
            for shape in shape_xml.find(f"{namespace}Shapes"):
                new_max = self.get_shape_max_id(shape)
                if new_max > max_id:
                    max_id = new_max
        return max_id

    def set_page_max_id(self, page_path) -> ET:

        page = self.page_xml_by_file_path[page_path]  # type: Element
        max_id = 0
        shapes_xml = page.find(f"{namespace}Shapes")
        if shapes_xml is not None:
            for shape in shapes_xml:
                id = self.get_shape_max_id(shape)
                if id > max_id:
                    max_id = id

        self.page_max_ids[page_path] = max_id

        return max_id

    # TODO: dead code - never used
    def get_sub_shapes(self, shape: Element, nth=1):
        for e in shape:
            if 'Shapes' in e.tag:
                nth -= 1
                if not nth:
                    return e

    @staticmethod
    def get_shape_location(shape: Element) -> (float, float):
        x, y = 0.0, 0.0
        cell_PinX = shape.find(f'{namespace}Cell[@N="PinX"]')  # type: Element
        cell_PinY = shape.find(f'{namespace}Cell[@N="PinY"]')
        x = float(cell_PinX.attrib['V'])
        y = float(cell_PinY.attrib['V'])

        return x, y

    @staticmethod
    def set_shape_location(shape: Element, x: float, y: float):
        cell_PinX = shape.find(f'{namespace}Cell[@N="PinX"]')  # type: Element
        cell_PinY = shape.find(f'{namespace}Cell[@N="PinY"]')
        cell_PinX.attrib['V'] = str(x)
        cell_PinY.attrib['V'] = str(y)

    @staticmethod
    # TODO: is this never used?
    def get_shape_text(shape: ET) -> str:
        # technically the below is not an exact replacement of the above...
        text = ""
        text_elem = shape.find(f"{namespace}Text")
        if text_elem is not None:
            text = "".join(text_elem.itertext())
        return text

    @staticmethod
    # TODO: is this never used?
    def set_shape_text(shape: ET, text: str):
        t = shape.find(f"{namespace}Text")  # type: Element
        if t is not None:
            if t.text:
                t.text = text
            else:
                t[0].tail = text

    # context = {'customer_name':'codypy.com', 'year':2020 }
    # example shape text "For {{customer_name}}  (c){{year}}" -> "For codypy.com (c)2020"
    @staticmethod
    def apply_text_context(shapes: Element, context: dict):

        def _replace_shape_text(shape: Element, context: dict):
            text = VisioFile.get_shape_text(shape)

            for key in context.keys():
                r_key = "{{" + key + "}}"
                text = text.replace(r_key, str(context[key]))
            VisioFile.set_shape_text(shape, text)

        for shape in shapes.findall(f"{namespace}Shapes"):
                VisioFile.apply_text_context(shape, context)  # recursive call
                _replace_shape_text(shape, context)

        for shape in shapes.findall(f"{namespace}Shape"):
            _replace_shape_text(shape, context)

    def jinja_render_vsdx(self, context: dict):
        # parse each shape in each page as Jinja2 template with context
        for page in self.pages:  # type: VisioFile.Page
            loop_shape_ids = list()
            for shapes in page.shapes:  # type: VisioFile.Shape
                prev_shape = None
                for shape in shapes.sub_shapes():  # type: VisioFile.Shape
                    # manage for loops in template
                    loop_shape_id = VisioFile.jinja_create_for_loop_if(shape, prev_shape)
                    if loop_shape_id:
                        loop_shape_ids.append(loop_shape_id)
                    prev_shape = shape
                    # manage 'set self' statements
                    VisioFile.jinja_set_selfs(shape)

            source = ET.tostring(page.xml.getroot(), encoding='unicode')
            source = VisioFile.unescape_jinja_statements(source)  # unescape chars like < and > inside {%...%}
            template = Template(source)
            output = template.render(context)
            page.xml = ET.ElementTree(ET.fromstring(output))  # create ElementTree from Element created from output

            # update loop shape IDs
            page.set_max_ids()
            for shape_id in loop_shape_ids:
                shapes = page.find_shapes_by_id(shape_id)
                if shapes and len(shapes) > 1:
                    delta = 0
                    for shape in shapes[1:]:  # from the 2nd onwards - leaving original unchanged
                        # increment each new shape duplicated by the jinja loop
                        self.increment_sub_shape_ids(shape, page.filename)
                        delta += shape.height  # automatically move each duplicate down
                        shape.move(0, -delta)  # move duplicated shapes so they are visible

    @staticmethod
    def jinja_set_selfs(shape: VisioFile.Shape):
        # apply any {% self self.xxx = yyy %} statements in shape properties
        jinja_source = shape.text
        matches = re.findall('{% set self.(.*?)\s?=\s?(.*?) %}', jinja_source)  # non-greedy search for all {%...%} strings
        for m in matches:  # type: tuple  # expect ('property', 'value') such as ('x', '10') or ('y', 'n*2')
            property_name = m[0]
            value = "{{ "+m[1]+" }}"  # Jinja to be processed
            # todo: replace any self references in value with actual value - i.e. {% set self.x = self.x+1 %}
            if property_name in ['x', 'y']:
                print(f"DEBUG: setting prop:{property_name}={value} for shape id={shape.ID}")
                shape.__setattr__(property_name, value)

        # remove any {% set self %} statements, leaving any remaining text
        matches = re.findall('{% set self.*?%}', jinja_source)
        for m in matches:
            jinja_source = jinja_source.replace(m, '')  # remove Jinja 'set self' statement
            print(f"DEBUG: removed '{m}' from shape.text id={shape.ID}")
        shape.text = jinja_source

    @staticmethod
    def unescape_jinja_statements(jinja_source):
        # unescape any text between {% ... %}
        jinja_source_out = jinja_source
        matches = re.findall('{%(.*?)%}', jinja_source)  # non-greedy search for all {%...%} strings
        for m in matches:
            unescaped = m.replace('&gt;', '>').replace('&lt;', '<')
            jinja_source_out = jinja_source_out.replace(m, unescaped)
        return jinja_source_out

    def increment_sub_shape_ids(self, shape: VisioFile.Shape, page_path, id_map: dict=None):
        id_map = self.increment_shape_ids(shape.xml, page_path, id_map)
        self.update_ids(shape.xml, id_map)
        for s in shape.sub_shapes():
            id_map = self.increment_shape_ids(s.xml, page_path, id_map)
            self.update_ids(s.xml, id_map)
            if s.sub_shapes():
                id_map = self.increment_sub_shape_ids(s, page_path, id_map)
        return id_map

    @staticmethod
    def jinja_create_for_loop_if(shape: VisioFile.Shape, previous_shape:VisioFile):
        # update a Shapes tag where text looks like a jinja {% for xxxx %} loop
        # move text to start of Shapes tag and add {% endfor %} at end of tag
        text = shape.text
        jinja_loop_text = text[:text.find(' %}') + 3] if text.startswith('{% for ') and text.find(' %}') else ''
        if jinja_loop_text:
            # move the for loop to start of shapes element (just before first Shape element)
            if previous_shape:
                previous_shape.xml.tail = jinja_loop_text  # add jinja loop text after previous shape, before this element
            else:
                shape.parent_xml.text = jinja_loop_text  # add jinja loop at start of parent, just before this element
            shape.text = text.lstrip(jinja_loop_text)  # remove jinja loop from <Text> tag in element

            # add closing 'endfor' to just inside the shapes element, after last shape
            shape.xml.tail = '{% endfor %}'  # add text at end of Shape element

            return shape.ID  # return shape ID if it is a loop

        # jinja_show_if - translate non-standard {% showif statement %} to valid jinja if statement
        jinja_show_if = text[:text.find(' %}') + 3] if text.startswith('{% showif ') and text.find(' %}') else ''
        if jinja_show_if:
            jinja_show_if = jinja_show_if.replace('{% showif ', '{% if ')  # translate to actual jinja if statement
            # move the for loop to start of shapes element (just before first Shape element)
            if previous_shape:
                previous_shape.xml.tail = str(previous_shape.xml.tail or '')+jinja_show_if  # add jinja loop text after previous shape, before this element
            else:
                shape.parent_xml.text = str(shape.parent_xml.text or '')+jinja_show_if  # add jinja loop at start of parent, just before this element

            shape.text = ''  # remove jinja loop from <Text> tag in element

            # add closing 'endfor' to just inside the shapes element, after last shape
            shape.xml.tail = '{% endif %}'  # add text at end of Shape element

    @staticmethod
    def get_shape_id(shape: ET) -> str:
        return shape.attrib['ID']

    def copy_shape(self, shape: Element, page: ET, page_path: str) -> ET:
        """Insert shape into first Shapes tag in destination page, and return the copy.

        If destination page does not have a Shapes tag yet, create it.

        Parameters:
            shape (Element): The source shape to be copied. Use Shape.xml
            page (ElementTree): The page where the new Shape will be placed. Use Page.xml
            page_path (str): The filename of the page where the new Shape will be placed. Use Page.filename

        Returns:
            ElementTree: The new shape ElementTree

        """

        new_shape = ET.fromstring(ET.tostring(shape))

        self.set_page_max_id(page_path)

        # find or create Shapes tag
        shapes_tag = page.find(f"{namespace}Shapes")
        if shapes_tag is None:
            shapes_tag = Element(f"{namespace}Shapes")
            page.getroot().append(shapes_tag)

        id_map = self.increment_shape_ids(new_shape, page_path)
        self.update_ids(new_shape, id_map)
        shapes_tag.append(new_shape)

        self.page_xml_by_file_path[page_path] = page
        return new_shape

    def insert_shape(self, shape: Element, shapes: Element, page: ET, page_path: str) -> ET:
        # insert shape into shapes tag, and return updated shapes tag
        id_map = self.increment_shape_ids(shape, page_path)
        self.update_ids(shape, id_map)
        shapes.append(shape)
        return shapes

    def increment_shape_ids(self, shape: Element, page_path: str, id_map: dict=None):
        if id_map is None:
            id_map = dict()
        self.set_new_id(shape, page_path, id_map)
        for e in shape.findall(f"{namespace}Shapes"):
            self.increment_shape_ids(e, page_path, id_map)
        for e in shape.findall(f"{namespace}Shape"):
            self.set_new_id(e, page_path, id_map)

        return id_map

    def set_new_id(self, element: Element, page_path: str, id_map: dict):
        if element.attrib.get('ID'):
            current_id = element.attrib['ID']
            max_id = self.page_max_ids[page_path] + 1
            id_map[current_id] = max_id  # record mappings
            element.attrib['ID'] = str(max_id)
            self.page_max_ids[page_path] = max_id
            return max_id  # return new id for info
        else:
            print(f"no ID attr in {element.tag}")

    def update_ids(self, shape: Element, id_map: dict):
        # update: <ns0:Cell F="Sheet.15! replacing 15 with new id using prepopulated id_map
        # cycle through shapes looking for Cell tag inside a Shape tag, which may be inside a Shapes tag
        for e in shape.findall(f"{namespace}Shapes"):
            self.update_ids(e, id_map)
        for e in shape.findall(f"{namespace}Shape"):
            # look for Cell elements
            cells = e.findall(f"{namespace}Cell[@F]")
            for cell in cells:
                f = str(cell.attrib['F'])
                if f.startswith("Sheet."):
                    # update sheet refs with new ids
                    shape_id = f.split('!')[0].split('.')[1]
                    new_id = id_map[shape_id]
                    new_f = f.replace(f"Sheet.{shape_id}",f"Sheet.{new_id}")
                    cell.attrib['F'] = new_f
        return shape

    def close_vsdx(self):
        try:
            # Remove extracted folder
            shutil.rmtree(self.directory)
        except FileNotFoundError:
            pass

    def save_vsdx(self, new_filename=None):
        """save the VisioFile object as new vsdx file

        :param new_filename: path to save vsdx file
        :type new_filename: str

        """
        # write pages.xml.rels
        xml_to_file(self.pages_xml_rels, f'{self.directory}/visio/pages/_rels/pages.xml.rels')

        # write pages.xml file - in case pages added removed
        xml_to_file(self.pages_xml, self._pages_filename())

        # write the pages to file
        for page in self.pages:  # type: VisioFile.Page
            xml_to_file(page.xml, page.filename)

        # write [content_Types].xml
        xml_to_file(self.content_types_xml, f'{self.directory}/[Content_Types].xml')

        # write app.xml
        xml_to_file(self.app_xml, f'{self.directory}/docProps/app.xml')

        # wrap up files into zip and rename to vsdx
        base_filename = self.filename[:-5]  # remove ".vsdx" from end
        if new_filename.find(os.sep) > 0:
            directory = new_filename[0:new_filename.rfind(os.sep)]
            if directory:
                if not os.path.exists(directory):
                    os.mkdir(directory)
        shutil.make_archive(base_filename, 'zip', self.directory)
        if not new_filename:
            shutil.move(base_filename + '.zip', base_filename + '_new.vsdx')
        else:
            if new_filename[-5:] != '.vsdx':
                new_filename += '.vsdx'
            shutil.move(base_filename + '.zip', new_filename)
        self.close_vsdx()

    class Cell:
        def __init__(self, xml: Element, shape: VisioFile.Shape):
            self.xml = xml
            self.shape = shape

        @property
        def value(self):
            return self.xml.attrib.get('V')

        @value.setter
        def value(self, value: str):
            self.xml.attrib['V'] = str(value)

        @property
        def name(self):
            return self.xml.attrib.get('N')

        @property
        def func(self):  # assume F stands for function, i.e. F="Width*0.5"
            return self.xml.attrib.get('F')

        def __repr__(self):
            return f"Cell: name={self.name} val={self.value} func={self.func}"

    class Shape:
        """Represents a single shape, or a group shape containing other shapes
        """
        def __init__(self, xml: Element, parent_xml: Element, page: VisioFile.Page):
            self.xml = xml
            self.parent_xml = parent_xml
            self.tag = xml.tag
            self.ID = xml.attrib.get('ID', None)
            self.master_shape_ID = xml.attrib.get('MasterShape', None)
            self.master_ID = xml.attrib.get('Master', None)
            self.shape_type = xml.attrib.get('Type', None)
            self.page = page

            # get Cells in Shape
            self.cells = dict()
            for e in self.xml.findall(f"{namespace}Cell"):
                cell = VisioFile.Cell(xml=e, shape=self)
                self.cells[cell.name] = cell

        def __repr__(self):
            return f"<Shape tag={self.tag} ID={self.ID} type={self.shape_type} text='{self.text}' >"

        def copy(self, page: Optional[VisioFile.Page] = None) -> VisioFile.Shape:
            """Copy this Shape to the specified destination Page, and return the copy.

            If the destination page is not specified, the Shape is copied to its containing Page.

            :param page: The page where the new Shape will be placed.
                If not specified, the copy will be placed in the original shape's page.
            :type page: :class:`Page` (Optional)

            :return: :class:`Shape` the new copy of shape
            """
            # set parent_xml: location for new shape tag to be added
            if page:
                # set parent_xml to first page Shapes tag if destination page passed
                parent_xml = page.xml.find(f"{namespace}Shapes")
            else:
                # or set parent_xml to source shapes own parent
                parent_xml = self.parent_xml

            page = page or self.page
            new_shape_xml = self.page.vis.copy_shape(self.xml, page.xml, page.filename)
            return VisioFile.Shape(xml=new_shape_xml, parent_xml=parent_xml, page=page)

        def cell_value(self, name: str):
            cell = self.cells.get(name)
            return cell.value if cell else None

        def set_cell_value(self, name: str, value: str):
            cell = self.cells.get(name)
            if cell:  # only set value of existing item
                cell.value = value

        @property
        def x(self):
            return to_float(self.cell_value('PinX'))

        @x.setter
        def x(self, value: float or str):
            self.set_cell_value('PinX', str(value))

        @property
        def y(self):
            return to_float(self.cell_value('PinY'))

        @y.setter
        def y(self, value: float or str):
            self.set_cell_value('PinY', str(value))

        @property
        def begin_x(self):
            return to_float(self.cell_value('BeginX'))

        @begin_x.setter
        def begin_x(self, value: float or str):
            self.set_cell_value('BeginX', str(value))

        @property
        def begin_y(self):
            return to_float(self.cell_value('BeginY'))

        @begin_y.setter
        def begin_y(self, value: float or str):
            self.set_cell_value('BeginY', str(value))

        @property
        def end_x(self):
            return to_float(self.cell_value('EndX'))

        @end_x.setter
        def end_x(self, value: float or str):
            self.set_cell_value('EndX', str(value))

        @property
        def end_y(self):
            return to_float(self.cell_value('EndY'))

        @end_y.setter
        def end_y(self, value: float or str):
            self.set_cell_value('EndY', str(value))

        def move(self, x_delta: float, y_delta: float):
            self.x = self.x + x_delta
            self.y = self.y + y_delta

        @property
        def height(self):
            return to_float(self.cell_value('Height'))

        @height.setter
        def height(self, value: float or str):
            self.set_cell_value('Height', str(value))

        @property
        def width(self):
            return to_float(self.cell_value('Width'))

        @width.setter
        def width(self, value: float or str):
            self.set_cell_value('Width', str(value))

        @staticmethod
        def clear_all_text_from_xml(x: Element):
            x.text = ''
            x.tail = ''
            for i in x:
                VisioFile.Shape.clear_all_text_from_xml(i)

        @property
        def text(self):
            text = ""
            t = self.xml.find(f"{namespace}Text")
            if t is not None:
                text = "".join(t.itertext())
            return text

        @text.setter
        def text(self, value):
            t = self.xml.find(f"{namespace}Text")  # type: Element
            if t is not None:
                VisioFile.Shape.clear_all_text_from_xml(t)
                t.text = value

        def sub_shapes(self):
            shapes = list()
            # for each shapes tag, look for Shape objects
            # self can be either a Shapes or a Shape
            # a Shapes has a list of Shape
            # a Shape can have 0 or 1 Shapes (1 if type is Group)

            if self.shape_type == 'Group':
                parent_element = self.xml.find(f"{namespace}Shapes")
            else:  # a Shapes
                parent_element = self.xml

            shapes = [VisioFile.Shape(shape, parent_element, self.page) for shape in parent_element]
            return shapes

        def find_shape_by_id(self, shape_id: str) -> VisioFile.Shape:  # returns Shape
            # recursively search for shapes by text and return first match
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if shape.ID == shape_id:
                    return shape
                if shape.shape_type == 'Group':
                    found = shape.find_shape_by_id(shape_id)
                    if found:
                        return found

        def find_shapes_by_id(self, shape_id: str) -> List[VisioFile.Shape]:
            # recursively search for shapes by text and return first match
            found = list()
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if shape.ID == shape_id:
                    found.append(shape)
                if shape.shape_type == 'Group':
                    sub_found = shape.find_shapes_by_id(shape_id)
                    if sub_found:
                        found.extend(sub_found)
            return found  # return list of matching shapes

        def find_shape_by_text(self, text: str) -> VisioFile.Shape:  # returns Shape
            # recursively search for shapes by text and return first match
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if text in shape.text:
                    return shape
                if shape.shape_type == 'Group':
                    found = shape.find_shape_by_text(text)
                    if found:
                        return found

        def find_shapes_by_text(self, text: str, shapes: list[VisioFile.Shape] = None) -> list[VisioFile.Shape]:
            # recursively search for shapes by text and return all matches
            if not shapes:
                shapes = list()
            for shape in self.sub_shapes():  # type: VisioFile.Shape
                if text in shape.text:
                    shapes.append(shape)
                if shape.shape_type == 'Group':
                    found = shape.find_shapes_by_text(text)
                    if found:
                        shapes.extend(found)
            return shapes

        def apply_text_filter(self, context: dict):
            # check text against all context keys
            text = self.text
            for key in context.keys():
                r_key = "{{" + key + "}}"
                text = text.replace(r_key, str(context[key]))
            self.text = text

            for s in self.sub_shapes():
                s.apply_text_filter(context)

        def find_replace(self, old: str, new: str):
            # find and replace text in this shape and sub shapes
            text = self.text
            self.text = text.replace(old, new)

            for s in self.sub_shapes():
                s.find_replace(old, new)

        def remove(self):
            self.parent_xml.remove(self.xml)

        def append_shape(self, append_shape: VisioFile.Shape):
            # insert shape into shapes tag, and return updated shapes tag
            id_map = self.page.vis.increment_shape_ids(append_shape.xml, self.page.filename)
            self.page.vis.update_ids(append_shape.xml, id_map)
            self.xml.append(append_shape.xml)

        @property
        def connects(self):
            # get list of connect items linking shapes
            connects = list()
            for c in self.page.connects:
                if self.ID in [c.shape_id, c.connector_shape_id]:
                    connects.append(c)
            return connects

        @property
        def connected_shapes(self):
            # return a list of connected shapes
            shapes = list()
            for c in self.connects:
                if c.connector_shape_id != self.ID:
                    shapes.append(self.page.find_shape_by_id(c.connector_shape_id))
                if c.shape_id != self.ID:
                    shapes.append(self.page.find_shape_by_id(c.shape_id))
            return shapes

    class Connect:
        def __init__(self, xml: Element):
            self.xml = xml
            self.from_id = xml.attrib.get('FromSheet')  # ref to the connector shape
            self.connector_shape_id = self.from_id
            self.to_id = xml.attrib.get('ToSheet')  # ref to the shape where the connector terminates
            self.shape_id = self.to_id
            self.from_rel = xml.attrib.get('FromCell')  # i.e. EndX / BeginX
            self.to_rel = xml.attrib.get('ToCell')  # i.e. PinX

        def __repr__(self):
            return f"Connect: from={self.from_id} to={self.to_id} connector_id={self.connector_shape_id} shape_id={self.shape_id}"

    class Page:
        """Represents a page in a vsdx file

        :param vis: the VisioFile object the page belongs to
        :type vis: :class:`VisioFile`
        :param name: the name of the page
        :type name: str
        :param connects: a list of Connect objects in the page
        :type connects: List of :class:`Connect`

        """
        def __init__(self, xml: ET.ElementTree, filename: str, page_name: str, vis: VisioFile):

            self._xml = xml
            self.filename = filename
            self.name = page_name
            self.vis = vis
            self.connects = self.get_connects()
            self.max_id = 0

        def __repr__(self):
            return f"<Page name={self.name} file={self.filename} >"

        @property
        def xml(self):
            return self._xml

        @xml.setter
        def xml(self, value):
            self._xml = value

        @property
        def shapes(self):
            """Return a list of :class:`Shape` objects

            Note: typically returns one :class:`Shape` object which itself contains :class:`Shape` objects

            """
            return [VisioFile.Shape(shapes, self.xml, self) for shapes in self.xml.findall(f"{namespace}Shapes")]

        def set_max_ids(self):
            # get maximum shape id from xml in page
            self.max_id = self.vis.set_page_max_id(self.filename)
            return self.max_id

        def get_connects(self):
            elements = self.xml.findall(f".//{namespace}Connect")  # search recursively
            connects = [VisioFile.Connect(e) for e in elements]
            return connects

        def get_connectors_between(self, shape_a_id: str='', shape_a_text: str='',
                                  shape_b_id: str='', shape_b_text: str=''):
            shape_a = self.find_shape_by_id(shape_a_id) if shape_a_id else self.find_shape_by_text(shape_a_text)
            shape_b = self.find_shape_by_id(shape_b_id) if shape_b_id else self.find_shape_by_text(shape_b_text)
            connector_ids = set(a.ID for a in shape_a.connected_shapes).intersection(
                set(b.ID for b in shape_b.connected_shapes))

            connectors = set()
            for id in connector_ids:
                connectors.add(self.find_shape_by_id(id))
            return connectors

        def apply_text_context(self, context: dict):
            for s in self.shapes:
                s.apply_text_filter(context)

        def find_replace(self, old: str, new: str):
            for s in self.shapes:
                s.find_replace(old, new)

        def find_shape_by_id(self, shape_id) -> VisioFile.Shape:
            for s in self.shapes:
                found = s.find_shape_by_id(shape_id)
                if found:
                    return found

        def find_shapes_by_id(self, shape_id) -> List[VisioFile.Shape]:
            # return all shapes by ID
            found = list()
            for s in self.shapes:
                found = s.find_shapes_by_id(shape_id)
                if found:
                    return found
            return found

        def find_shape_by_text(self, text: str) -> VisioFile.Shape:
            for s in self.shapes:
                found = s.find_shape_by_text(text)
                if found:
                    return found

        def find_shapes_by_text(self, text: str) -> list[VisioFile.Shape]:
            shapes = list()
            for s in self.shapes:
                found = s.find_shapes_by_text(text)
                if found:
                    shapes.extend(found)
            return shapes


def file_to_xml(filename: str) -> ET.ElementTree:
    """Import a file as an ElementTree"""
    try:
        tree = ET.parse(filename)
        return tree
    except FileNotFoundError:
        pass  # return None


def xml_to_file(xml: ET.ElementTree, filename: str):
    """Save an ElementTree to a file"""
    xml.write(filename)
