import streamlit as st
from streamlit_js_eval import streamlit_js_eval
import os
from glob import glob
import pandas as pd
import socket as s
from Moeda import Moeda
import altair as alt
from DownloadXLSX import ExcelDW
from datetime import datetime

IP=s.gethostbyname(s.gethostname())

class Dashboard:

    def __init__(self,titulo):

        self.titulo=titulo

        pass


    def main(self):


        placeholder=st.empty()

        temp_dict=dict()

        btn_reset=False
        with placeholder.container():

            st.title(self.titulo)
            st.markdown('----')

            temp_path=os.path.join(os.getcwd(),IP,'User','*.txt*')
            arq=glob(temp_path)

            with open(arq[-1],'r') as file:

                user_name=str(file.read()).strip()

                pass

            temp_path=os.path.join(os.getcwd(),IP,user_name,'*.xlsx*')
            arquivos=glob(temp_path)

            df=pd.DataFrame()
            for arq in arquivos:

                excel_df=pd.read_excel(arq,dtype='object')
                df=pd.concat([df,excel_df],axis=0,ignore_index=True)

                pass

            df.drop_duplicates(inplace=True)
            
            if len(df)>0:

                df['Grupo']=df['Segmento'].apply(lambda info: str(info).split()[0])

                with st.sidebar:

                    lista=df['Grupo'].unique().tolist()
                    temp_dict['Grupo']=st.multiselect(label='Grupo',options=lista,key='select_grupo')

                    lista=df['Segmento'].unique().tolist()
                    temp_dict['Segmento']=st.multiselect(label='Segmento',options=lista,key='select_segmento')

                    lista=df['Cidade'].unique().tolist()
                    temp_dict['Cidade']=st.multiselect(label='Cidade',options=lista,key='select_cidade') 

                    lista=df['Bairro'].unique().tolist()
                    temp_dict['Bairro']=st.multiselect(label='Bairro',options=lista,key='select_bairro')             

                    btn_reset=st.button('Reset',key='btn_reset',use_container_width=True,type='primary')                          

                    pass

                for k,v in temp_dict.items():

                    if len(v)<=0:

                        continue

                    df=df.loc[df[k].isin(v)]

                    pass

                qtde=Moeda.Numero(len(df['Empresa'].unique().tolist()))
                st.caption(f'Você tem em sua base {qtde} leads, que foram extraídas do google.',unsafe_allow_html=True)

                with st.expander('Lista de Clientes'):

                    st.dataframe(df,use_container_width=True,hide_index=False)

                    data=ExcelDW.DownloadXLSX(df)
                    dt_now=datetime.strftime(datetime.now().date(),'%d_%m_%Y')
                    st.download_button('Download XLSX',type='primary',data=data,file_name=f'Lista de Clientes {dt_now}.xlsx')

                    pass
                
                bar=alt.Chart(df.groupby(['Grupo'],as_index=False).agg({'Empresa':'count'})).mark_bar().encode(

                    x=alt.X('Grupo',sort='-y'),
                    y='Empresa'
                )

                rotulo=bar.mark_text(

                    dy=-10,
                    size=17

                ).encode(text='Empresa')

                st.caption('Leads por Grupo')
                st.altair_chart(bar+rotulo,use_container_width=True)

                #por segmento

                bar=alt.Chart(df.groupby(['Segmento'],as_index=False).agg({'Empresa':'count'})).mark_bar().encode(

                    x=alt.X('Segmento',sort='-y'),
                    y='Empresa'
                )

                rotulo=bar.mark_text(

                    dy=-12,
                    size=17

                ).encode(text='Empresa')

                st.caption('Leads por Segmento')
                st.altair_chart(bar+rotulo,use_container_width=True)

                div1,div2=st.columns(2)

                #por cidade
                bar=alt.Chart(df.groupby(['Cidade'],as_index=False).agg({'Empresa':'count'})).mark_bar().encode(

                    x=alt.X('Cidade',sort='-y'),
                    y='Empresa'
                )

                rotulo=bar.mark_text(

                    dy=-10,
                    size=17

                ).encode(text='Empresa')

                div1.caption('Leads por Cidade')
                div1.altair_chart(bar+rotulo,use_container_width=True)       

                #por bairro
                bar=alt.Chart(df.groupby(['Bairro'],as_index=False).agg({'Empresa':'count'})).mark_bar().encode(

                    x=alt.X('Bairro',sort='-y'),
                    y='Empresa'
                )

                rotulo=bar.mark_text(

                    dy=-10,
                    size=17

                ).encode(text='Empresa')

                div2.caption('Leads por Bairro')
                div2.altair_chart(bar+rotulo,use_container_width=True)


                pass           


            pass


        if btn_reset:

            temp_path=os.path.join(os.getcwd(),IP,user_name,'*.xlsx*')
            arq=glob(temp_path)

            for a in arq:

                os.remove(a)

                pass

            streamlit_js_eval(js_expressions='parent.window.location.reload()')

            pass


        pass


    pass