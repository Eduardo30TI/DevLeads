import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import os
from glob import glob
from pages.telas import Cadastro,Menu
import socket as s
from SQL import SQL
import time

sql=SQL()

tabelas={

    'user':

    """

    CREATE TABLE IF NOT EXISTS user(
    
        CNPJ VACHAR(250) NOT NULL,
        EMPRESA VARCHAR(250) NOT NULL,
        EMAIL TEXT NOT NULL,
        SENHA VARCHAR(250) NOT NULL,
        LOG SMALLINT NOT NULL

    )

    """
}

sql.Table(querys=tabelas.values())

IP=s.gethostbyname(s.gethostname())

temp_path=os.path.join(os.getcwd(),'Icone','*.ico*')
icone=glob(temp_path)

with open(icone[-1],'rb') as file:

    st.set_page_config('DevLeads',layout='centered',page_icon=file.read())

    pass

def main():

    placeholder=st.empty()

    path_base=os.path.join(os.getcwd(),IP)
    os.makedirs(path_base,exist_ok=True)
    temp_path=os.path.join(path_base,'*.txt*')
    arq=glob(temp_path)

    temp_dict=dict()

    if len(arq):

        placeholder.empty()

        with open(arq[-1],'r',encoding='UTF-8') as file:

            nome=str(file.read()).strip()

            pass

        if nome.lower().find('cadastro')>=0:

            tela=Cadastro(nome)
            tela.main()

            pass

        elif nome.lower().find('menu')>=0:

            tela=Menu(nome)
            tela.main()

            pass

        pass

    else:

        #aplicar css
        path_css=os.path.join(os.getcwd(),'CSS','style.css')
        arq=glob(path_css)

        with open(arq[-1]) as file:

            st.markdown(f'<style>{file.read()}</style>',unsafe_allow_html=True)

            pass
            
        with placeholder.container():

            temp_path=os.path.join(os.getcwd(),'Imagem','foguete.png')
            arq=glob(temp_path)

            if len(arq)>0:

                with open(arq[-1],'rb') as file:

                    st.image(image=file.read(),width=120)
                    st.header('DevLeads')

                    pass

                pass

            st.markdown('----')

            temp_dict['email']=st.text_input('E-mail',key='email').lower()
            temp_dict['senha']=st.text_input('Senha',type='password',key='senha')

            btn1,btn2=st.columns(2)

            btn_log=btn1.button('Logar',use_container_width=True,type='primary',key='btn_log')
            btn_cad=btn2.button('Cadastro',use_container_width=True,type='secondary',key='btn_cad')

            pass

        if btn_cad:

            placeholder.empty()
            name='Cadastro de Usuário'

            temp_path=os.path.join(path_base,'tela.txt')
            with open(temp_path,'w',encoding='UTF-8') as file:

                file.write(name)

                pass
                    
            placeholder.empty()
            tela=Cadastro(name)
            tela.main()

            pass

        if btn_log:
            
            resp=validarCampos(temp_dict)

            if resp!=None:

                mensagem=st.warning(resp)
                time.sleep(1)
                mensagem.empty()

                pass

            else:

                querys={

                    'user':

                    """

                    SELECT * FROM user

                    """,

                    'UPDATE':

                    """

                    UPDATE user
                    SET LOG=1
                    WHERE EMAIL='{0}'

                    """.format(temp_dict['email'])
                }

                df=sql.Get(querys,tabela=['user'])

                log_user=df['user'].loc[(df['user']['EMAIL']==temp_dict['email'])&(df['user']['SENHA']==temp_dict['senha']),'LOG'].values
                log_user=log_user if len(log_user)>0 else 0
                senha=df['user'].loc[(df['user']['EMAIL']==temp_dict['email']),'SENHA'].unique().tolist()
                
                if log_user>0:

                    mensagem=st.warning(f'Usuário: {temp_dict["email"]} já está logado no sistema!')
                    time.sleep(1)
                    mensagem.empty()

                    pass

                elif len(senha)<=0:

                    mensagem=st.warning('Usuário não encontrado no sistema.')
                    time.sleep(1)
                    mensagem.empty()

                    pass             

                if len(senha)>0:

                    if senha[-1]!=temp_dict['senha']:
                    
                        mensagem=st.warning('Senha inválida!')
                        time.sleep(1)
                        mensagem.empty()

                        pass

                    else:
                        
                        name='Menu'

                        info_dict={'tela.txt':name,'user.txt':temp_dict['email']}

                        for k,v in info_dict.items():

                            if k!='user.txt':
                        
                                temp_path=os.path.join(os.getcwd(),IP,k)

                                pass

                            else:

                                path_base=os.path.join(path_base,'User')
                                os.makedirs(path_base,exist_ok=True)
                                temp_path=os.path.join(path_base,k)

                                pass

                            with open(temp_path,'w') as file:

                                file.write(v)

                                pass

                            pass

                        mensagem=st.success('Seja bem vindo')
                        time.sleep(1)
                        mensagem.empty()
                        time.sleep(1)

                        placeholder.empty()
                        tela=Menu(name)
                        tela.main()

                        pass

                    pass

                pass

            pass

        pass

    pass

def validarCampos(campos:dict):

    temp_dict={0:None}

    for k,v in campos.items():

        if v=='':

            temp_dict[0]=f'Informe {k}'
                
            break

        pass

    return temp_dict[0]

    pass


if __name__=='__main__':

    main()

    pass