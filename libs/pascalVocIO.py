import sys, os
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from xml.dom import minidom
from lxml import etree

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from libs.shape import Shape


class PascalVocWriter:
    def __init__(self,
                 foldername,
                 filename,
                 imgSize,
                 databaseSrc='Unknown',
                 localImgPath=None,
                 shape_type=None,
                 framegrabber=None,
                 append=True,
                 savefilename=None):

        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.shape_type = shape_type
        self.framegrabber = framegrabber
        self.savefilename = savefilename

        if append and os.path.exists(savefilename):
            # read previous annotations and add them to boxlist
            reader = PascalVocReader(savefilename)
            shapes = reader.getShapes()

            for label, points, line_color, fill_color, shape_type, instance_id, frame in shapes:
                if not frame == self.framegrabber.get_position():
                    self.addPolygon(points, label, instance_id, frame)

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        return etree.tostring(root, pretty_print=True)

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        '''
        if self.filename is None or \
                        self.foldername is None or \
                        self.imgSize is None or \
                        len(self.boxlist) <= 0:
        '''
        if self.filename is None or \
                len(self.boxlist) <= 0:
            return None

        top = Element('annotation')
        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        localImgPath = SubElement(top, 'path')
        self.localImgPath = self.localImgPath.split('/')[-1]
        localImgPath.text = self.localImgPath

        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = self.databaseSrc

        if self.framegrabber is not None:
            videometa = SubElement(top, 'video-meta-data')
            frames = SubElement(videometa, 'n_frames')
            duration = SubElement(videometa, 'duration')
            fps = SubElement(videometa, 'fps')

            frames.text = str(self.framegrabber.get_nframes())
            duration.text = str(self.framegrabber.get_duration())
            fps.text = str(self.framegrabber.get_fps())

        if self.imgSize:
            size_part = SubElement(top, 'size')
            width = SubElement(size_part, 'width')
            height = SubElement(size_part, 'height')
            depth = SubElement(size_part, 'depth')
            width.text = str(self.imgSize[1])
            height.text = str(self.imgSize[0])
            if len(self.imgSize) == 3:
                depth.text = str(self.imgSize[2])
            else:
                depth.text = '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        shape_type = SubElement(top, 'shape_type')
        shape_type.text = self.shape_type
        return top

    def addBndBox(self, xmin, ymin, xmax, ymax, name):
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        bndbox['name'] = name
        self.boxlist.append(bndbox)

    def addPolygon(self, shape, name, instance_id, frame=None):
        polygon = {}
        i = 0
        for point in shape:
            polygon[i] = point
            i = i + 1
        polygon['name'] = name
        polygon['point_num'] = str(len(shape))
        polygon['instance_id'] = instance_id
        polygon['frame'] = frame
        self.boxlist.append(polygon)

    def appendObjects(self, top):
        for each_object in self.boxlist:
            # print(each_object)
            object_item = SubElement(top, 'object')
            if each_object['name']:
                name = SubElement(object_item, 'name')
                name.text = unicode(each_object['name'])

            if self.framegrabber is not None:
                # record which frame this object belongs to
                frame = SubElement(object_item, 'frame')
                if each_object['frame'] is None:
                    frame.text = str(self.framegrabber.get_position())
                else:
                    frame.text = str(each_object['frame'])

            pose = SubElement(object_item, 'pose')
            pose.text = "Unspecified"
            if 'instance_id' in each_object.keys():
                instance_id = SubElement(object_item, 'instance_id')
                instance_id.text = str(each_object['instance_id'])
            truncated = SubElement(object_item, 'truncated')
            truncated.text = "0"
            difficult = SubElement(object_item, 'difficult')
            difficult.text = "0"
            if self.shape_type == 'RECT':
                bndbox = SubElement(object_item, 'bndbox')
                xmin = SubElement(bndbox, 'xmin')
                xmin.text = str(each_object['xmin'])
                ymin = SubElement(bndbox, 'ymin')
                ymin.text = str(each_object['ymin'])
                xmax = SubElement(bndbox, 'xmax')
                xmax.text = str(each_object['xmax'])
                ymax = SubElement(bndbox, 'ymax')
                ymax.text = str(each_object['ymax'])
            elif self.shape_type == 'POLYGON':
                polygon = SubElement(object_item, 'polygon')
                for i in xrange(int(each_object['point_num'])):
                    point = SubElement(polygon, 'point' + str(i))
                    point.text = str(int(each_object[i][0])) + ',' + str(
                        int(each_object[i][1]))
                    # print i, point.text

    def save(self, targetFile=None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = open(self.filename + '.xml', 'w')
        else:
            out_file = open(targetFile, 'w')
        out_file.write(self.prettify(root))
        # out_file.write(root)
        out_file.close()


class PascalVocReader:
    def __init__(self, filepath):
        # shapes type:
        ## [label, [(x1,y1), (x2,y2), (x3,y3)], color, color, shape_type, instance_id, frame]
        self.shapes = []
        self.filepath = filepath
        self.shape_type = None
        self.image_size = []
        self.parseXML()

    def getShapes(self):
        return self.shapes

    def getShapeType(self):
        return self.shape_type

    def addPolygonShape(self, label, points, instance_id=0, frame=None):
        points = [(point[0], point[1]) for point in points]
        self.shapes.append((label, points, None, None, 1, instance_id, frame))

    def get_img_size(self):
        if self.image_size:
            return self.image_size

    def addShape(self, label, rect, instance_id=0, frame=None):
        xmin = rect[0]
        ymin = rect[1]
        xmax = rect[2]
        ymax = rect[3]
        points = [(xmin, ymin), (xmin, ymax), (xmax, ymax), (xmax, ymin)]
        self.shapes.append((label, points, None, None, 0, instance_id, frame))

    def parseXML(self):
        assert self.filepath.endswith('.xml'), "Unsupport file format"
        parser = etree.XMLParser(encoding='utf-8')
        xmltree = ElementTree.parse(self.filepath, parser=parser).getroot()
        filename = xmltree.find('filename').text
        if xmltree.find('shape_type') is not None:
            self.shape_type = xmltree.find('shape_type').text
        else:
            self.shape_type = 'RECT'
        self.image_size.append(int(xmltree.find('size').find('width').text))
        self.image_size.append(int(xmltree.find('size').find('height').text))
        if self.shape_type == 'RECT':
            for object_iter in xmltree.findall('object'):
                rects = []
                bndbox = object_iter.find("bndbox")
                rects.append([int(it.text) for it in bndbox])
                label = object_iter.find('name').text
                if object_iter.find('frame') is not None:
                    frame = int(object_iter.find('frame').text)
                for rect in rects:
                    self.addShape(label, rect, frame)

            return True
        elif self.shape_type == 'POLYGON':
            for object_iter in xmltree.findall('object'):
                points = []
                polygons = object_iter.find("polygon")
                label = object_iter.find('name').text
                for point in polygons:
                    point = point.text.split(',')
                    point = [int(dot) for dot in point]
                    points.append(point)
                if object_iter.find('instance_id') is not None:
                    instance_id = int(object_iter.find('instance_id').text)

                if object_iter.find('frame') is not None:
                    frame = int(object_iter.find('frame').text)
                else:
                    frame = None
                self.addPolygonShape(label, points, instance_id, frame)
        else:
            print 'unsupportable shape type'


# tempParseReader = PascalVocReader('test.xml')
# print tempParseReader.getShapes()
"""
# Test
tmp = PascalVocWriter('temp','test', (10,20,3))
tmp.addBndBox(10,10,20,30,'chair')
tmp.addBndBox(1,1,600,600,'car')
tmp.save()
"""
