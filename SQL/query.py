import sqlite3
import pandas as pd

class SQL:

    def __init__(self) -> None:

        pass

    def Conecta(self):

        try:

            conecta=sqlite3.connect('MOINHO.db')

            return conecta

            pass

        except:

            print('Sem conexão com o banco de dados')

            pass

        pass


    def Save(self,query):

        with self.Conecta() as conecta:

            cursor=conecta.cursor()

            cursor.execute(query)

            conecta.commit()
            
            pass

        pass


    def Code(self,query):

        with self.Conecta() as conecta:

            cursor=conecta.cursor()

            cursor.execute(query)

            codigo=[c for c in cursor.fetchone()]

            pass

        return codigo[-1]

        pass


    def Get(self,querys:dict,tabela=list):

        temp_dict=dict()

        with self.Conecta() as conecta:

            for t in tabela:

                temp_dict[t]=pd.read_sql(querys[t],conecta)

                pass

            pass

        return temp_dict

        pass


    def Table(self,querys:list):

        for query in querys:

            self.Save(query)

            pass

        pass

    pass