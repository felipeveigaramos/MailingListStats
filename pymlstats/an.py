# coding: latin1

from datetime import datetime
from db.database import *
from sqlalchemy import and_, or_, text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

def le_arquivo():
    arq = open('e-mails e datas.txt', 'r')
    a = arq.read()
    b = a.split('\n')

    while len(b)>210:
        del b[-1]
    return b


def numero_mes(s):
    '''str->int
    Retorna o número correspondente para um dado mês, em inglês.
    >>> numero_mes('Jan')
    1
    >>> numero_mes('Dec')
    12
    >>> numero_mes('bat')
    0
    '''
    if s == 'Jan':
        return 1
    elif s == 'Feb':
        return 2
    elif s == 'Mar':
        return 3
    elif s == 'Apr':
        return 4
    elif s == 'May':
        return 5
    elif s == 'Jun':
        return 6
    elif s == 'Jul':
        return 7
    elif s == 'Aug':
        return 8
    elif s == 'Sep':
        return 9
    elif s == 'Oct':
        return 10
    elif s == 'Nov':
        return 11
    elif s == 'Dec':
        return 12
    return 0

def gera_data(data_string):
    '''string -> datetime
    Converte uma data em texto para timedate.

    '''
    data_string_list = data_string.split(' ')
    day = 1
    month = 1
    year = 1900
    horas_list = [0, 0, 0]

    if ((len(data_string) == 36 or len(data_string) == 37)
and len(data_string_list) == 7) or ((len(data_string) == 25 or len(data_string) == 26) and len(data_string_list) == 5) or ((len(data_string) == 30 or len(data_string)
== 31) and len(data_string_list) == 6):
        extra = 0 #algumas datas possuem valor maior de dados e o primeiro deve ser ignorado
        if len(data_string_list) == 7 or len(data_string_list) == 6:
            extra = 1
        horas_list = data_string_list[3+extra].split(':')
        year = data_string_list[2+extra]
        month = numero_mes(data_string_list[1+extra])
        day = data_string_list[0+extra]
        #print(str(extra) + " " + str(data_string_list[0]) + " " + str(data_string_list[1]) + " " + str(data_string_list[2]))
    elif ((len(data_string) == 24 or len(data_string) == 25) and len(data_string_list) == 5):
        horas_list = data_string_list[3].split(':')
        year = data_string_list[-1]
        month = numero_mes(data_string_list[1])
        day = data_string_list[2]
    elif len(data_string_list) ==6 and 27 <= len(data_string) <= 29:
        year = data_string_list[-1]
        month = numero_mes(data_string_list[1])
        day = data_string_list[2]
        horas_list = data_string_list[3].split(':')

    data = datetime(int(year), month, int(day), int(horas_list[0]), int(horas_list[1]), int(horas_list[2]))
    #print(data_string + " " + str(data))
    return data



class analyzer(object) :
    def gera_banco(self):
        engine_mls = create_engine('mysql://root:root@localhost/mlstats', encoding='utf8', convert_unicode=True)
        Session_mls = sessionmaker(bind=engine_mls)
        self.mls = Session_mls()

        #engine_g = create_engine('mysql://root:root@localhost/bicho', encoding='utf8', convert_unicode=True)
        #Session_g = sessionmaker(bind=engine_g)
        #self.gerrit = Session_g()

    def analyze(self):
        self.gera_banco()
        list_data = le_arquivo()
        query_messages = self.mls.query(Messages)
        query_messages_people = self.mls.query(MessagesPeople)

        if not os.path.exists('a_data'):
            os.mkdir('a_data')

        for i in range(len(list_data)):
            if i%2 == 0:
                date_txt = list_data[i+1].replace("  ", " ")
                date = gera_data(date_txt)
                #print str(i+1) + " " + str(len(date_txt)) + " " + str(len(date_txt.split(' '))) + " | " + date_txt
                print date
                if date.year != 2013 and date.year !=2014:
                    continue
                email = list_data[i]
                working_dir = 'a_data/'+email+'/'
                if not os.path.exists(working_dir):
                    os.mkdir(working_dir)
                date_a = datetime(date.year-1, date.month, date.day)
                date_b = datetime(date.year+1, date.month, date.day)
                messages_people = query_messages_people.filter(MessagesPeople.email_address == email)
                m_id_list = []
                for mp in messages_people.all():
                    m_id_list.append(mp.message_id)

                if len(m_id_list) >0:
                    messages = query_messages.filter(Messages.message_id.in_(m_id_list)).filter(and_(Messages.first_date >= date_a, Messages.first_date <= date_b))
                    print str(len(messages.all()))

                    j = 0
                    for m in messages.all():
                        arq = open(working_dir + str(j), "w")
                        j+=1
                        raw_text =m.__repr__()
                        arq.writelines(raw_text.encode("latin1", 'ignore'))

                        for m2 in query_messages.filter(Messages.is_response_of == m.message_id).all():
                            arq.writelines("\n"+ ("*"*40) + "\n")
                            raw_text =m2.__repr__()
                            arq.writelines(raw_text.encode("latin1", 'ignore'))

                        arq.close()


def main():
    a = analyzer()
    a.analyze()

main()
