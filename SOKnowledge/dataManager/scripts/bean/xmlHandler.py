#!/usr/bin/python
# -*- coding: utf-8 -*-
"""this is a module to load a big xml file and recognise its structure,split it into small file"""
import xml.sax as SAX

import sys

import scripts.bean.schema as schema


class XMLHandlerForPost(SAX.ContentHandler):
    """a class to handle Post xml by sax and insert it into MySql"""

    def setSession(self, session):
        self.session = session

    def __init__(self):
        SAX.ContentHandler.__init__(self)
        self.session = None
        self.errorrRow = 0
        self.sucessRow = 0

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        # print ("---tag-- " + tag + " -S---")

        if tag == "row":
            if self.sucessRow<2953984:
                self.sucessRow+=1
                return
            insertData = None
            if attributes.getValue("PostTypeId") == "1":
                insertData = schema.Question()
            if attributes.getValue("PostTypeId") == "2":
                insertData = schema.Answer()

            attr = {}
            for key in attributes.keys():
                attr[key] = attributes.getValue(key)
                # print (key + "=" + attr[key])

            if insertData is None:
                print "error unknownType"
                for key in attributes.keys():
                    print (key + "=" + attr[key])
                return
            schema.reflectObjFromDict(insertData, attr)

            if self.session:
                try:
                    self.session.add(insertData)
                    self.session.commit()
                    self.sucessRow += 1
                    print ("insert successfully sucessRow=" + str(self.sucessRow))
                except:
                    print sys.exc_info()[0], sys.exc_info()[1]
                    self.errorrRow += 1
                    print ("insert wrong row=" + str(self.errorrRow))

    # 元素结束事件处理
    def endElement(self, name):
        #print ("---tag " + name + " -E---")
        pass

    # 内容事件处理
    def characters(self, content):
        if not content.isspace():
            print("content=" + str(len(content)))


"""
if __name__ == "__main__":
    # 创建一个 XMLReader
    parser = SAX.make_parser()
    # turn off nameSpaces
    parser.setFeature(SAX.handler.feature_namespaces, 0)

    handler = XMLHandlerForPost()
    parser.setContentHandler(handler)
    try:
        Session = sessionmaker(bind=schema.getEngineForMySql())
        session = Session()
        handler.setSession(session)
        # path = u"C://Users//isky//Desktop//xml//movie.xml"
        path = u"E:/实验室/data/Posts.xml"
        # path = path.encode('utf-8')
        parser.parse(path)
    finally:
        if handler.session:
            handler.session.close()
"""
