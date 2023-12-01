from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import streamlit as st
from streamlit_js_eval import streamlit_js_eval
from streamlit_option_menu import option_menu
import time
import pandas as pd
from Acentos import Acentuacao
from DownloadXLSX import ExcelDW
from CEP import CEP
import os
from glob import glob
import socket as s

link='https://www.google.com.br/search?q=restaurante+santana+sp&sca_esv=585968432&biw=1366&bih=611&tbm=lcl&sxsrf=AM9HkKnPfd0hE_qzSOvvyib_RQOH82CJig%3A1701189093947&ei=5RVmZY-qOeir5OUP-ZK1mAg&ved=0ahUKEwjPsI-dj-eCAxXoFbkGHXlJDYMQ4dUDCAk&oq=rest&gs_lp=Eg1nd3Mtd2l6LWxvY2FsIgRyZXN0KgIIAjIEECMYJzIEECMYJzIEECMYJzIKEAAYgAQYigUYQzINEAAYgAQYigUYyQMYQzILEAAYgAQYigUYkgMyCxAAGIAEGIoFGJIDMggQABiABBixAzIKEAAYgAQYigUYQzIFEAAYgARIpFFQjzZYwDlwA3gAkAEAmAFroAGhA6oBAzEuM7gBA8gBAPgBAagCCsICBxAjGOoCGCeIBgE&sclient=gws-wiz-local#rlfi=hd:;si:;mv:[[-23.4891529,-46.6211151],[-23.5161102,-46.6431964]];tbs:lrf:!1m4!1u3!2m2!3m1!1e1!1m4!1u5!2m2!5m1!1sgcid_3brazilian_1restaurant!1m4!1u5!2m2!5m1!1sgcid_3japanese_1restaurant!1m4!1u2!2m2!2m1!1e1!1m4!1u1!2m2!1m1!1e1!1m4!1u1!2m2!1m1!1e2!2m1!1e2!2m1!1e5!2m1!1e1!2m1!1e3!3sIAEqAkJS,lf:1,lf_ui:9'

IP=s.gethostbyname(s.gethostname())

class GoogleLeads:

    def __init__(self,titulo) -> None:

        self.titulo=titulo

        self.service=Service()
        self.option=Options()
        self.option.add_argument('--headless')

        self.driver=None
        
        pass


    def main(self):

        placeholder=st.empty()

        temp_dict=dict()

        with placeholder.container():
            
            st.title(self.titulo)
            st.markdown('----')

            temp_dict['pesquisa']=st.text_input('Pesquisa',key='text_leach')

            btn_leach=st.button('Pesquisar',type='primary',key='btn_leach')

            pass

        if btn_leach:

            resp=self.validarCampos(temp_dict)

            if resp[0]!=None:

                mensagem=st.warning(resp[0])
                time.sleep(1)
                mensagem.empty()

                pass

            else:

                st.caption('Aguarde...')
                self.leachGoogle(temp_dict['pesquisa'])

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

        return temp_dict

        pass


    def leachGoogle(self,pesquisa):

        self.driver=webdriver.Chrome(service=self.service,options=self.option)
        self.driver.maximize_window()
        self.driver.get(link)
        
        while True:

            cont=len(self.driver.find_elements(By.CSS_SELECTOR,'span.ExCKkf.z1asCe.rzyADb'))
            time.sleep(1)

            if cont>0:

                break

            pass

        btn=self.driver.find_element(By.CSS_SELECTOR,'span.ExCKkf.z1asCe.rzyADb')
        btn.click()

        #APjFqb
        while True:

            cont=len(self.driver.find_elements(By.ID,'APjFqb'))
            time.sleep(1)

            if cont>0:

                break

            pass

        campo=self.driver.find_element(By.ID,'APjFqb')
        campo.send_keys(pesquisa,Keys.ENTER)

        temp=[]

        df=pd.DataFrame(columns=['Empresa','Segmento','CEP','Endereço','Bairro','Cidade','UF','Seq','Telefone']) 
        while True:

            loop=True
            while loop:

                try:

                    espera=0
                    while True:

                        cont=len(self.driver.find_elements(By.CSS_SELECTOR,'div.cXedhc div.rllt__details div.dbg0pd span.OSrXXb'))
                        time.sleep(1)
                        espera+=1

                        if cont>0 or espera>5:

                            break

                        pass

                    elements=self.driver.find_elements(By.CSS_SELECTOR,'div.cXedhc div.rllt__details div.dbg0pd span.OSrXXb')

                    for e in elements:

                        if e.text in temp:

                            continue

                        temp.append(e.text)

                        with ActionChains(self.driver) as action:

                            action.move_to_element(e).click().perform()
                            time.sleep(1)

                            pass

                        #extrair dados do cliente
                        nome=self.driver.find_element(By.CSS_SELECTOR,'div.SPZz6b h2 span').text
                        segmento=self.driver.find_elements(By.CSS_SELECTOR,'div.TLYLSe.MaBy9 span.YhemCb')
                        segmento=segmento[-1].text if len(segmento)>0 else ''
                        endereco=self.driver.find_elements(By.CSS_SELECTOR,'div.zloOqf.PZPZlf span.LrzXr')
                        endereco=endereco[0].text if len(endereco)>0 else ''
                        cep=str(endereco.split(',')[-1])
                        info_dict=CEP.GetCEP(cep)
                        telefone=self.driver.find_elements(By.CSS_SELECTOR,'div.zloOqf.PZPZlf span.LrzXr.zdqRlf.kno-fv a')
                        
                        contagem=1
                        for t in telefone:
                            
                            df.loc[len(df)]=[nome,segmento,cep,endereco,info_dict['bairro'],info_dict['cidade'],info_dict['uf'],f'Contato {contagem}',t.text]
                            contagem+=1

                            pass

                        pass

                    loop=False

                    pass

                except:

                    loop=True

                    pass

                pass

            espera=0
            while True:

                #//*[@id="pnnext"]/span[2]
                cont=len(self.driver.find_elements(By.XPATH,'//*[@id="pnnext"]/span[2]'))
                time.sleep(1)
                espera+=1

                if cont>0 or espera>5:

                    break

                pass

            if cont>0:

                btn=self.driver.find_element(By.XPATH,'//*[@id="pnnext"]/span[2]')
                
                with ActionChains(self.driver) as action:

                    action.move_to_element(btn).click().perform()
                    time.sleep(1)

                    pass

                pass

            else:

                self.driver.close()

                break

            pass

        df.drop_duplicates(inplace=True)
        df=df.pivot(index=['Empresa','Segmento','CEP','Endereço','Bairro','Cidade','UF'],columns='Seq',values='Telefone').reset_index()

        colunas=df.columns.tolist()

        for c in colunas:

            df[c]=df[c].apply(lambda info: str(info).upper())
            df[c]=df[c].apply(Acentuacao.RemoverAcento)

            pass

        if len(df)>0:
            
            temp_path=os.path.join(os.getcwd(),IP,'User','*.txt*')
            arq=glob(temp_path)

            with open(arq[-1],'r') as file:

                user_name=str(file.read()).strip()

                pass

            arq=str(pesquisa).replace(' ','_')

            temp_path=os.path.join(os.getcwd(),IP,user_name)
            os.makedirs(temp_path,exist_ok=True)
            temp_path=os.path.join(temp_path,f'{arq}.xlsx')
            df.to_excel(temp_path,index=False)

            st.caption(f'Leads {len(df)}')            
            st.dataframe(df,use_container_width=True,hide_index=False)
                        
            data=ExcelDW.DownloadXLSX(df)
            st.download_button('Download XLSX',type='primary',data=data,file_name=f'{arq}.xlsx')

            pass

        pass


    pass