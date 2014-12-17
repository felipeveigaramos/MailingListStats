#coding:utf-8

from db.database import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import *
from sqlalchemy import and_

def conecta_banco():
    engine = create_engine("mysql://root:root@localhost/mlstats", encoding='utf8', convert_unicode=True)
    Session = sessionmaker(bind=engine)
    return Session()

def main():
    session = conecta_banco()
    q = session.query(People)
    p = People(email_address="teste@teste.tst", name="testerson", username="testerson", domain_name="@teste.tst", top_level_domain="tst")
    session.add(p)
    try:
        session.commit()
    except exception,e:
        print e
    p2=q.filter(People.email_address == "teste@teste.tst").one()
    print p2.__repr__()

main()
