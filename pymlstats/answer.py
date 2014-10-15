#coding:latin

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import *
from sqlalchemy import and_

def conecta_banco():
    engine = create_engine("mysql://root:root@localhost/mlstats", encoding='utf8', convert_unicode=True)
    Session = sessionmaker(bind=engine)
    return Session()

def print_output(text, be_quiet):
    if not be_quiet:
        print text

#def procura_respostas(session, be_quiet):
def procura_respostas(session=None, be_quiet=False):
    session = conecta_banco()

    quantidade_respostas = 0
    for ml in session.query(MailingLists).all():
        print "Verificando respostas do projeto " + str(ml.project_name)
        quantidade_respostas_lista = procura_respostas_listas(session, ml.mailing_list_url)
        print "Número de respostas encontradas no projeto: " + str(quantidade_respostas_lista)
        quantidade_respostas += quantidade_respostas_lista
    print "Número de respostas totais encontradas: " + str(quantidade_respostas)

def procura_respostas_listas(session, ml_url):
    quantidade_mensagens = 0
    for message in session.query(Messages).filter(and_(Messages.mailing_list_url == ml_url, Messages.is_response_of =='')).all():
        print "procurando resposta para mensagem de: " + message.message_id
        resposta_encontrada = encontrar_resposta_para_mensagem(session, message, ml_url)
        if resposta_encontrada:
            quantidade_mensagens+=1
            print "\a encontrada resposta para mensagem #" + quantidade_mensagens
    return quantidade_mensagens

def encontrar_resposta_para_mensagem(session, message, ml_url):
    for m in  session.query(Messages).filter(Messages.mailing_list_url ==
ml_url).all():
        if message!=m:
            if eh_pai(m, message):
                return True
                """
                message.is_response_of(m.message_id)
                try:
                    session.commit()
                    return True
                except:
                    session.rollback()
                break
                """
    return False

def eh_pai(mensagem1, mensagem2):
    '''Mensagem, Mensagem -> bool
    Verifica se a mensagem 1 é a mensagem pai  da mensagem 2.
    or (mensagem1.message_id in mensagem2.references) or  (mensagem1.message_id == mensagem2.in_reply_to)
    '''
    if ((mensagem2.subject[:3] == 're:' and mensagem1.subject == mensagem2.subject[3:]) or (mensagem2.subject[:4] == 'res:' and mensagem1.subject == mensagem2.subject[4:])):
        return True
    elif (mensagem1.message_id in mensagem2.references) or  (mensagem1.message_id == mensagem2.in_reply_to):
        return True
    return False

#procura_respostas()
