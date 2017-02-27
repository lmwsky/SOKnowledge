#!/usr/bin/python
# -*- coding: utf-8 -*-
import sqlite3
import os
import xml.etree.cElementTree as etree
import logging

ANATHOMY = {
    'badges': {
        'Id': 'INTEGER',
        'UserId': 'INTEGER',
        'Name': 'TEXT',
        'Date': 'DATETIME',
    },
    'comments': {
        'Id': 'INTEGER',
        'PostId': 'INTEGER',
        'Score': 'INTEGER',
        'Text': 'TEXT',
        'CreationDate': 'DATETIME',
        'UserId': 'INTEGER',
        'UserDisplayName': 'TEXT'
    },
    'posts': {
        'Id': 'INTEGER',
        'PostTypeId': 'INTEGER',  # 1: Question, 2: Answer
        'ParentID': 'INTEGER',  # (only present if PostTypeId is 2)
        'AcceptedAnswerId': 'INTEGER',  # (only present if PostTypeId is 1)
        'CreationDate': 'DATETIME',
        'Score': 'INTEGER',
        'ViewCount': 'INTEGER',
        'Body': 'TEXT',
        'OwnerUserId': 'INTEGER',  # (present only if user has not been deleted)
        'OwnerDisplayName': 'TEXT',
        'LastEditorUserId': 'INTEGER',
        'LastEditorDisplayName': 'TEXT',  # ="Rich B"
        'LastEditDate': 'DATETIME',  # ="2009-03-05T22:28:34.823"
        'LastActivityDate': 'DATETIME',  # ="2009-03-11T12:51:01.480"
        'CommunityOwnedDate': 'DATETIME',  # (present only if post is community wikied)
        'Title': 'TEXT',
        'Tags': 'TEXT',
        'AnswerCount': 'INTEGER',
        'CommentCount': 'INTEGER',
        'FavoriteCount': 'INTEGER',
        'ClosedDate': 'DATETIME'
    },
    'votes': {
        'Id': 'INTEGER',
        'PostId': 'INTEGER',
        'UserId': 'INTEGER',
        'VoteTypeId': 'INTEGER',
        # -   1: AcceptedByOriginator
        # -   2: UpMod
        # -   3: DownMod
        # -   4: Offensive
        # -   5: Favorite
        # -   6: Close
        # -   7: Reopen
        # -   8: BountyStart
        # -   9: BountyClose
        # -  10: Deletion
        # -  11: Undeletion
        # -  12: Spam
        # -  13: InformModerator
        'CreationDate': 'DATETIME',
        'BountyAmount': 'INTEGER'
    },
    'posthistory': {
        'Id': 'INTEGER',
        'PostHistoryTypeId': 'INTEGER',
        'PostId': 'INTEGER',
        'RevisionGUID': 'INTEGER',
        'CreationDate': 'DATETIME',
        'UserId': 'INTEGER',
        'UserDisplayName': 'TEXT',
        'Comment': 'TEXT',
        'Text': 'TEXT'
    },
    'postlinks': {
        'Id': 'INTEGER',
        'CreationDate': 'DATETIME',
        'PostId': 'INTEGER',
        'RelatedPostId': 'INTEGER',
        'PostLinkTypeId': 'INTEGER',
        'LinkTypeId': 'INTEGER'
    },
    'users': {
        'Id': 'INTEGER',
        'Reputation': 'INTEGER',
        'CreationDate': 'DATETIME',
        'DisplayName': 'TEXT',
        'LastAccessDate': 'DATETIME',
        'WebsiteUrl': 'TEXT',
        'Location': 'TEXT',
        'Age': 'INTEGER',
        'AboutMe': 'TEXT',
        'Views': 'INTEGER',
        'UpVotes': 'INTEGER',
        'DownVotes': 'INTEGER',
        'EmailHash': 'TEXT',
        'AccountId': 'INTEGER',
        'ProfileImageUrl': 'TEXT'
    },
    'tags': {
        'Id': 'INTEGER',
        'TagName': 'TEXT',
        'Count': 'INTEGER',
        'ExcerptPostId': 'INTEGER',
        'WikiPostId': 'INTEGER'
    }
}


def dump_files(file_names,
               anathomy,
               xml_file_path='.',
               dump_path='.',
               dump_database_name='so-dump.db',
               log_filename='so-parser.log',
               create_query='CREATE TABLE IF NOT EXISTS {table} ({fields})',
               insert_query='INSERT INTO {table} ({columns}) VALUES ({values})'
               ):
    logging.basicConfig(filename=os.path.join(dump_path, log_filename), level=logging.INFO)
    db = sqlite3.connect(os.path.join(dump_path, dump_database_name))
    for file in file_names:
        print
        "Opening {0}.xml".format(file)
        with open(os.path.join(xml_file_path, file + '.xml')) as xml_file:
            tree = etree.iterparse(xml_file)
            table_name = file

            sql_create = create_query.format(
                table=table_name,
                fields=", ".join(['{0} {1}'.format(name, type) for name, type in anathomy[table_name].items()]))
            print('Creating table {0}'.format(table_name))

            try:
                logging.info(sql_create)
                db.execute(sql_create)
            except Exception, e:
                logging.warning(e)

            for events, row in tree:
                try:
                    if row.attrib.values():
                        logging.debug(row.attrib.keys())
                        query = insert_query.format(
                            table=table_name,
                            columns=', '.join(row.attrib.keys()),
                            values=('?, ' * len(row.attrib.keys()))[:-2])
                        db.execute(query, row.attrib.values())
                        print ".",
                except Exception, e:
                    logging.warning(e)
                    print "x",
                finally:
                    row.clear()
            print "\n"
            db.commit()
            del (tree)


def parse_xml_db(xml_file_names,
                 xml_file_path=".",
                 dump_path=".",
                 dump_database_name='so-dump.db',
                 log_filename='so-parser.log'):
    legal_file_names = ANATHOMY.keys()

    for file_name in xml_file_names:
        if file_name not in legal_file_names:
            print file_name, ' is not a legal file name\n'
            print 'following are the legal file name:\n',
            print legal_file_names
            return
    dump_files(xml_file_names, ANATHOMY, xml_file_path, dump_path, dump_database_name, log_filename)


def usage():
    usageStr = {
        "-h": "show the usage",
        "--xmlpath": "the path of the xmls file dir",
        "--xmlnames": "the name of the xml files without file type suffix,such as post,tags,votes,if there are more than one,connect the name with ','",
        "--logname": "the name of the parse log file.default:so-parser.log",
        "--dbname": "the name of the database file name,must end with .db.default:so-dump.db",
        "--dbpath": "the path of the database file name",
    }
    team = "\n".join(['{0}  :{1}'.format(command, description) for command, description in usageStr.items()])
    print(team)


if __name__ == '__main__':
    import sys, getopt

    opts, args = getopt.getopt(sys.argv[1:], "h", ["xmlnames=", "logname=", "dbname=", "xmlpath=", "dbpath="])

    xml_file_names = []
    dump_path = "."
    dump_database_name = 'so-dump.db'
    log_filename = 'so-parser.log'
    xml_path = "."
    for op, value in opts:
        if op == "--xmlnames":
            xml_file_names = value.split(',')
        elif op == "--dbpath":
            dump_path = value
        elif op == "--dbname":
            dump_database_name = value
        elif op == "--xmlpath":
            xml_path = value
        elif op == "--logname":
            log_filename = value
        elif op == "-h":
            usage()
            sys.exit()

    if len(xml_file_names) > 0:
        print xml_file_names
        parse_xml_db(xml_file_names)
    else:
        print "xml file names are not setted"
