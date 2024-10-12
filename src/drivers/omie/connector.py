import json
import time

import requests


class Omie:
    def __init__(self, nome, app_key, app_secret) -> None:
        self.nome = nome
        self.app_key = app_key
        self.app_secret = app_secret
        self.base_api = "https://app.omie.com.br/api"

    def get(self, route: str, call: str, result_id="", page_max = None, param = None, campos = None):

        if(param is None):
            param = {
                "pagina": 1,
                "registros_por_pagina": "100",
                "apenas_importado_api": "N"
            }
        url = self.base_api + route

        page = 1
        
        result = []

        while True:
            payload = json.dumps({
                "call": call,
                "app_key": self.app_key,
                "app_secret": self.app_secret,
                "param": [param]
            })
            
            headers = {
                'Content-type': 'application/json'
            }
            
            response = requests.request("POST", url, headers=headers, data=payload).json()
            print(response)
            # quit()
            
            if (result_id not in response):
                print(response)
                
            response_result = response[result_id]
            
            # SÓ FUNCIONA PARA MF
            if (campos is not None):
                for resp in response_result:
                    for campo_existente in resp["detalhes"]:
                        
                        if (campo_existente in campos["detalhes"]):
                            campos["detalhes"].remove(campo_existente)
                
                # preeche campos faltantes
                for campo_novo in campos["detalhes"]:
                    resp[campo_novo] = ""
                    
            # SÓ FUNCIONA PARA MF
            if (campos is not None):
                
                
                for resp in response_result:
                    if "departamentos" not in resp:
                        resp["departamentos"] = {}
                        # preeche campos faltantes
                        for campo_novo in campos["departamentos"]:
                            resp[campo_novo] = ""
                
                for campo_existente in resp["departamentos"]:
                    
                    if (campo_existente in campos["departamentos"]):
                        campos["departamentos"].remove(campo_existente)
                
                # preeche campos faltantes
                for campo_novo in campos["departamentos"]:
                    resp[campo_novo] = ""
            
            result = result + response_result
            
            if (page_max is not None):
                pass

            elif ("nTotPaginas" in response):
                page_max = response["nTotPaginas"]
                
            elif ("total_de_paginas" in response):
                page_max = response["total_de_paginas"]
            
            if(page == page_max or page_max == 0):
                break
                
            page = page + 1
            
            if ("nTotPaginas" in response):
                param["nPagina"] = page
                
            if ("total_de_paginas" in response):
                param["pagina"] = page
            
            print(f"Page: {page}/{page_max}")
            time.sleep(1)
        
        return result
        










        