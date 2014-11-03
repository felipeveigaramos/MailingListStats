# coding: latin


import difflib

from sqlalchemy import and_, or_, text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import *


def gera_banco():
    engine = create_engine('mysql://root:root@localhost/mlstats', encoding='utf8', convert_unicode=True)
    Session = sessionmaker(bind=engine)
    return Session()

def lista_novatos():
    session = gera_banco()
    quantidade_mensagens = 0
    #statement = 'All of my past & future contributions to LibreOffice may be licensed under the MPL/LGPLv3+ dual license'
    m_query = session.query(Messages).from_statement(text("select * from messages where message_body like '%future contributions%' AND (message_body like '%MPL%' OR message_body like '%GNU%' OR message_body like '%Mozilla%' "\
"or message_body like '%gpl%' or message_body like '%licenses that the code base is under%' or message_body like '%CURRENT PROJECT LICENSES%' or message_body like '%licenses used by this project%') and is_response_of = ''"))
    mp_query = session.query(MessagesPeople)
    p_query = session.query(People)

    for message in m_query.all():
        #if difflib.SequenceMatcher(None, message.message_body, statement).find_longest_match(0,len(message.message_body),0,len(statement)) >= 17:
        messagesPeople = mp_query.filter(and_(MessagesPeople.message_id == message.message_id, MessagesPeople.mailing_list_url == message.mailing_list_url)).one()
        people = p_query.filter(People.email_address == messagesPeople.email_address).one()
        print  message.message_body.encode('latin-1', 'ignore') + people.__repr__().encode('latin-1', 'ignore')
        quantidade_mensagens+=1
    print str(quantidade_mensagens)


lista_novatos()
