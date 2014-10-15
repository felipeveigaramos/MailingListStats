# coding: latin


import difflib

from sqlalchemy import and_
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import *


def gera_banco():
    engine = create_engine("mysql://root:root@localhost/mlstats", encoding='utf8', convert_unicode=True)
    Session = sessionmaker(bind=engine)
    return Session()

def lista_novatos():
    session = gera_banco()
    quantidade_mensagens = 0
    statement = 'All of my past & future contributions to LibreOffice may be licensed under the MPL/LGPLv3+ dual license'
    #for message in session.query(Messages).filter(Messages.message_body.like('%'+statement+'%')):
    for message in session.query(Messages):
        #if difflib.SequenceMatcher(None, message.message_body, statement).find_longest_match(0,len(message.message_body),0,len(statement)) >= 17:
        if statement in message.message_body:
            print str(quantidade_mensagens+1)
            messagesPeople = session.query(MessagesPeople).filter(and_(MessagesPeople.message_id == message.message_id, MessagesPeople.mailing_list_url == message.mailing_list_url)).one()
            people = session.query(People).filter(People.email_address == messagesPeople.email_address).one()
            print (u'' + people.__repr__()).encode('latin-1', 'ignore')
            quantidade_mensagens+=1
    print str(quantidade_mensagens)


lista_novatos()
