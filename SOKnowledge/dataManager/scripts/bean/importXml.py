#!/usr/bin/python
# -*- coding: utf-8 -*-
import xml.sax as SAX

# 创建一个 XMLReader
from sqlalchemy.orm import sessionmaker
import scripts.bean.schema as schema

from scripts.bean.xmlHandler import XMLHandlerForPost


def parseXml(xmlPath, handler):
    parser = SAX.make_parser()
    # turn off nameSpaces
    parser.setFeature(SAX.handler.feature_namespaces, 0)
    parser.setContentHandler(handler)
    try:
        Session = sessionmaker(bind=schema.getEngineForMySql())
        session = Session()
        handler.setSession(session)
        parser.parse(xmlPath)
    finally:
        if handler.session:
            handler.session.close()


handler = XMLHandlerForPost()
xmlPathForPost = u"E:/实验室/data/Posts.xml"

parseXml(xmlPathForPost, handler)
