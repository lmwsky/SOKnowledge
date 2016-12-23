#!/usr/bin/env python
# -*- coding:utf-8 -*-
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dbConfig = {
    'user': 'root',
    'password': 'lmw1994',
    'host': '127.0.0.1',
    'post': '3306',
    'dbname': 'stackoverflow',
    'charset': 'utf8'
}

Base = declarative_base()


# 寻找Base的所有子类，按照子类的结构在数据库中生成对应的数据表信息
# Base.metadata.create_all(engine)
class Answer(Base):
    __tablename__ = 'answer'
    Id = Column(Integer, primary_key=True)
    Body = Column(Text)
    LastActivityDate = Column(DateTime)
    CommunityOwnedDate = Column(DateTime)
    LastEditorUserId = Column(Integer)
    LastEditDate = Column(DateTime)
    CommentCount = Column(Integer)
    Score = Column(Integer)
    ParentId = Column(Integer)
    OwnerUserId = Column(Integer)
    CreationDate = Column(DateTime)
    PostTypeId = Column(Integer)


class Question(Base):
    __tablename__ = 'question'
    Id = Column(Integer, primary_key=True)
    Body = Column(Text)
    ViewCount = Column(Integer)
    LastActivityDate = Column(DateTime)
    Title = Column(Text)
    LastEditorUserId = Column(Integer)
    LastEditorDisplayName = Column(String(255))
    LastEditDate = Column(DateTime)
    CommentCount = Column(Integer)
    AnswerCount = Column(Integer)
    AcceptedAnswerId = Column(Integer)
    Score = Column(Integer)
    PostTypeId = Column(Integer)
    OwnerUserId = Column(Integer)
    OwnerDisplayName = Column(String(255))
    Tags = Column(String(255))
    CreationDate = Column(DateTime)
    FavoriteCount = Column(Integer)


def reflectObjFromDict(obj, data):
    for key in data.keys():
        if hasattr(obj, key):  # 检查实例是否有这个属性
            setattr(obj, key, data.get(key))  # same as: obj.'key' = dict.get(key)
    return obj


def getEngineForMySql():
    engine = create_engine(
        "mysql+mysqldb://{0}:{1}@{2}:{3}/{4}?charset={5}".format(dbConfig.get('user'),
                                                                 dbConfig.get('password'),
                                                                 dbConfig.get('host'),
                                                                 dbConfig.get('post'),
                                                                 dbConfig.get('dbname'),
                                                                 dbConfig.get('charset'))
    )
    return engine


if __name__ == "__main__":
    Session = sessionmaker(bind=getEngineForMySql())
    session = Session()
    data = {
        "Id": 3,
        "Body": "ggggg"
    }
    # 增
    question1 = Question()
    reflectObjFromDict(question1, data)
    session.add(question1)
    session.commit()
