import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_js_eval import streamlit_js_eval
import os
from glob import glob
import socket as s
from SQL import SQL
from .google_leads import GoogleLeads
from .dashboard import Dashboard

sql=SQL()

IP=s.gethostbyname(s.gethostname())

class Menu:

    def __init__(self,titulo) -> None:
        
        self.titulo=titulo
        
        pass


    def main(self):

        placeholder=st.empty()

        with placeholder.container():

            #aplicar css
            path_css=os.path.join(os.getcwd(),'CSS','style.css')
            arq=glob(path_css)

            with open(arq[-1]) as file:

                st.markdown(f'<style>{file.read()}</style>',unsafe_allow_html=True)

                pass

            with st.sidebar:

                temp_path=os.path.join(os.getcwd(),'Imagem','foguete.png')
                image=glob(temp_path)

                with open(image[-1],'rb') as file:

                    st.image(file.read(),width=95)
                    st.header('DevLeads')

                    pass

                st.markdown('----')

                temp_path=os.path.join(os.getcwd(),IP,'User','*.txt*')
                arq=glob(temp_path)

                with open(arq[-1],'r') as file:

                    user_name=str(file.read()).strip()

                    pass

                st.caption(f'Usuário: {user_name}')

                selected = option_menu("Menu", options=["Google",'Dashboard','Exit'], 
                    icons=['google','speedometer','box-arrow-left'], menu_icon="cast", default_index=0)
                
                pass

            pass
        
        if selected=='Google':

            tela=GoogleLeads(selected)
            tela.main()

            pass

        elif selected=='Exit':

            temp_path=os.path.join(os.getcwd(),IP,'*.txt*')
            arq=glob(temp_path)

            if len(arq)>0:

                os.remove(arq[-1])
                streamlit_js_eval(js_expressions='parent.window.location.reload()')

                pass

            pass

        elif selected=='Dashboard':

            tela=Dashboard(selected)
            tela.main()

            pass    

        pass

    pass