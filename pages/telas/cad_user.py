import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from CNPJ import CNPJ
import socket as s
import os
from glob import glob
import time
import secrets
import string
from Senhas import Senha
from Gmail import Mail
from SQL import SQL

sql=SQL()

mail=Mail()

IP=s.gethostbyname(s.gethostname())

class Cadastro:

    def __init__(self,titulo) -> None:

        self.titulo=titulo

        pass

    def main(self):

        placeholder=st.empty()

        temp_dict=dict()
        btn_back=False
        btn_send=False
        with placeholder.container():

            st.title(self.titulo)
            st.markdown('----')

            temp_dict['cnpj']=st.text_input('CNPJ',placeholder='informe o CNPJ',key='text_cnpj')

            try:
                        
                if temp_dict['cnpj']!='':

                    cnpj=CNPJ(temp_dict['cnpj'])
                    json=cnpj.GetDados()

                    temp_dict['empresa']=st.text_input('Razão Social',key='text_razao',value=json['razao_social'],disabled=True)

                    temp_dict['email']=st.text_input('E-mail',key='email').lower()

                    btn1,btn2=st.columns(2)

                    btn_send=btn1.button('Enviar',use_container_width=True,key='btn_send',type='primary')
                    btn_back=btn2.button('Voltar',use_container_width=True,key='btn_back',type='secondary')

                    pass

                pass

            except:

                mensagem=st.error('Dados não encontrados!')
                time.sleep(1)
                mensagem.empty()
                
                pass

            pass

        if btn_back:

            placeholder.empty()
            temp_path=os.path.join(os.getcwd(),IP,'*.txt*')
            arq=glob(temp_path)

            if len(arq)>0:

                os.remove(arq[-1])

                pass
            
            streamlit_js_eval(js_expressions='parent.window.location.reload()')

            pass

        elif btn_send:

            resp=self.validarCampos(temp_dict)

            if resp!=None:

                mensagem=st.warning(resp)
                time.sleep(1)
                mensagem.empty()
                
                pass

            else:

                senha=Senha.Reload()

                querys={

                    'validar':

                    """

                    SELECT COUNT(*) FROM user WHERE EMAIL='{0}'

                    """.format(temp_dict['email']),

                    'INSERT':

                    """

                    INSERT INTO user(CNPJ,EMPRESA,EMAIL,SENHA,LOG)VALUES('{0}','{1}','{2}','{3}',{4})

                    """.format(temp_dict['cnpj'],temp_dict['empresa'],temp_dict['email'],senha,0),

                    'UPDATE':

                    """

                    UPDATE user
                    SET CNPJ='{0}'
                    EMPRESA='{1}',
                    SENHA='{3}'
                    WHERE EMAIL='{2}'

                    """.format(temp_dict['cnpj'],temp_dict['empresa'],temp_dict['email'],senha)
                }
                
                validar=sql.Code(query=querys['validar'])

                tipo='INSERT' if validar<=0 else 'UPDATE'

                sql.Save(querys[tipo])

                #enviar e-mail
                assunto='DevLeads - Senha'

                mensagem=f"""

                <p>Olá segue o e-mail para acesso a plataforma: <strong>DevLeads</strong></p>

                <p>Usuário: <strong>{temp_dict['email']}</strong></p>
                <p>Senha: <strong>{senha}</strong></p>

                """

                send_dict={'To':[temp_dict['email']],'CC':[''],'Anexo':[]}

                mail.Enviar(assunto=assunto,mensagem=mensagem,info=send_dict)

                ################
                            
                temp_path=os.path.join(os.getcwd(),IP,'*.txt*')
                arq=glob(temp_path)

                if len(arq)>0:

                    os.remove(arq[-1])

                    pass
                                            
                mensagem=st.success('Senha enviada por e-mail')
                time.sleep(1)
                mensagem.empty()
                time.sleep(1)

                streamlit_js_eval(js_expressions='parent.window.location.reload()')

                pass

            pass

        pass


    def validarCampos(self,campos:dict):

        temp_dict={0:None}

        for k,v in campos.items():

            if v=='':

                temp_dict[0]=f'Informe {k}'
                
                break

            pass

        return temp_dict[0]

        pass

    pass