#coding:utf-8

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
        print "Numero de respostas encontradas no projeto: " + str(quantidade_respostas_lista)
        quantidade_respostas += quantidade_respostas_lista
    print "Número de respostas totais encontradas: " + str(quantidade_respostas)

def procura_respostas_listas(session, ml_url):
    mensagens_totais = 0
    quantidade_mensagens = 0
    messages=  session.query(Messages).filter(and_(Messages.mailing_list_url == ml_url, Messages.is_response_of == '')).all()
    for message in session.query(Messages).filter(and_(Messages.mailing_list_url == ml_url, Messages.answer == '')).all():
        mensagens_totais+=1
        print "procurando resposta para mensagem de: " + message.message_id + " \n numero: " + str(mensagens_totais)
        resposta_encontrada = encontrar_resposta_para_mensagem(message, ml_url, messages)
        if resposta_encontrada:
            quantidade_mensagens+=1
            print "encontrada resposta para mensagem #" + str(quantidade_mensagens) + " / " + str(mensagens_totais)

        if mensagens_totais%1000 == 0:
            print "\a \a persistindo mensagens:"
            try:
                session.commit()
                print "mensagens salvas."
            except:
                print "erro ao salvar mensagens"
                session.rollback()
    return quantidade_mensagens

def encontrar_resposta_para_mensagem(message, ml_url, messages):
    for m in messages:
        if message!=m:
            if eh_pai(message,m):
                message.answer = m.message_id
                m.is_response_of= message.message_id
                messages.remove(m)
                return True
    return False

def eh_pai(mensagem1, mensagem2):
    '''Message, Messagem -> bool
    Verifica se a mensagem 1 é a mensagem pai  da mensagem 2.
    '''
    m2s=mensagem2.subject
    m1s=mensagem1.subject
    if (((m2s[:3]).lower() == 're:' and m1s.strip() == m2s[3:].strip()) or ((m2s[:4]).lower() == 'res:' and m1s.strip() == m2s[4:].strip())):
        return True
    elif (mensagem2.references != None and (mensagem1.message_id in mensagem2.references)) or  (mensagem1.message_id == mensagem2.in_reply_to):
        return True
    return False

procura_respostas()
