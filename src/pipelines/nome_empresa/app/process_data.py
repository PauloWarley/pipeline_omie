from datetime import datetime 
import pandas as pd
import json
import os

from pipelines.nome_empresa.stages.extract.extract import Extract

from pipelines.nome_empresa.stages.normalizedObj.normalizedObj import NormalizeObj
from pipelines.nome_empresa.stages.transform.transform import Transform
from pipelines.nome_empresa.stages.mergeTables.mergeTables import MergeTables
class ProcessData:
    def __init__(self, empresa: dict):
        self.extractor = Extract(
            nome=empresa["nome"],
            app_key=empresa["app_key"],
            app_secret=empresa["app_secret"]
        )
        self.transformer = Transform()
        self.empresa = empresa["nome"]

    def run_etl(self):
        # Extrair os dados
        # notas_fiscais = self.extractor.extract_notas_fiscais()
        # notas_fiscais_produtos = self.extractor.extract_notas_fiscais()
        
        # empresas = self.extractor.extract_empresas()
        # contacorrente = self.extractor.extract_contacorrente()
        # clientes = self.extractor.extract_clientes()
        # departamentos = self.extractor.extract_depatamentos()
        # projetos = self.extractor.extract_projetos()
        # categorias = self.extractor.extract_categorias()
        # contareceber = self.extractor.extract_conta_receber()
        # contapagar = self.extractor.extract_conta_pagar()

        # Extração do movimento financeiro (mf)
        mf = self.extractor.extract_mf()

        # Transformar os dados
        empresas_df = self.transformer.transform_empresas(empresas)
        # contacorrente_df = self.transformer.transform_contacorrente(contacorrente)
        # clientes_df = self.transformer.transform_clientes(clientes)
        # departamentos_df = self.transformer.transform_departamentos(departamentos)
        # projetos_df = self.transformer.transform_projetos(projetos)
        # categorias_df = self.transformer.transform_categorias(categorias)
        # contareceber_df = self.transformer.transform_conta_receber(contareceber)
        # contapagar_df = self.transformer.transform_conta_pagar(contapagar)
        
        # notas_fiscais_df = self.transformer.transform_notas_fiscais(notas_fiscais)
        # notas_fiscais_produtos_df = self.transformer.transform_notas_fiscais_produtos(notas_fiscais_produtos)

        
        if not os.path.exists(f"./results/{self.empresa}"):
            os.makedirs(f"./results/{self.empresa}")

        # Salvar os dados em arquivos Excel
        empresas_df.to_excel(f"./results/{self.empresa}/empresas.xlsx", index=None)
        # contacorrente_df.to_excel(f"./results/{self.empresa}/contacorrente.xlsx", index=None)
        # clientes_df.to_excel(f"./results/{self.empresa}/clientes.xlsx", index=None)
        # departamentos_df.to_excel(f"./results/{self.empresa}/departamentos.xlsx", index=None)
        # projetos_df.to_excel(f"./results/{self.empresa}/projetos.xlsx", index=None)
        # categorias_df.to_excel(f"./results/{self.empresa}/categorias.xlsx", index=None)
        # contareceber_df.to_excel(f"./results/{self.empresa}/contareceber.xlsx", index=None)
        # contapagar_df.to_excel(f"./results/{self.empresa}/contapagar.xlsx", index=None)
        
        # notas_fiscais_df.to_excel(f"./results/{self.empresa}/notasfiscais.xlsx", index=None)
        # notas_fiscais_produtos_df.to_excel(f"./results/{self.empresa}/notasfiscaisproduto.xlsx", index=None)

        # Linearizar
        normObj = NormalizeObj()
        lnrz = normObj.linearilize_object
        mf_linearized = [lnrz(object=i) for i in mf]

        pd.DataFrame.from_records(mf_linearized).to_excel(f"./results/{self.empresa}/movimento.xlsx", index=None)

        merger = MergeTables()
        merger.merge()
with open("./pipelines/nome_empresa/app/empresas.json", "r") as arquivo_json:
    empresas = json.load(arquivo_json)

print(datetime.now())

for empresa in empresas:
    etl = ProcessData(empresa)
    etl.run_etl()

print(datetime.now())