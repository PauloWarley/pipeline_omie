import os
import pandas as pd

class MergeTables:
    def __init__(self, base_dir="./tabelas", output_dir="./tabelas_unificadas"):
        self.base_dir = base_dir
        self.output_dir = output_dir
        self.tabelas = {
            "categorias": [],
            "clientes": [], 
            "contacorrente": [],
            "contapagar": [],
            "contareceber": [],
            "departamentos": [],
            "empresas": [],
            "projetos": [],
            "movimento": []
        }

    def merge(self):
        arquivos = os.listdir(self.base_dir)

        # Unir as tabelas
        for tabela in self.tabelas:
            for arquivo in arquivos:
                if tabela in arquivo:
                    df = pd.read_excel(os.path.join(self.base_dir, arquivo))
                    df["origem"] = arquivo
                    colunas = list(df.keys())
                    if "Unnamed: 0" in colunas:
                        colunas.remove("Unnamed: 0")
                    df = df[colunas]
                    self.tabelas[tabela].append(df)

        df_unificadas = []
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        for tabela in self.tabelas:
            tbl_unificada = pd.concat(self.tabelas[tabela])
            tbl_unificada.to_excel(os.path.join(self.output_dir, f"{tabela}.xlsx"), index=None)
            df_unificadas.append(tbl_unificada)

        # Tratamento específico para a tabela movimento
        df = pd.read_excel(os.path.join(self.output_dir, "movimento.xlsx"))
        colunas = list(df.keys())
        if "Unnamed: 0" in colunas:
            colunas.remove("Unnamed: 0")

        df = df[colunas]
        novas_colunas = {coluna: coluna[coluna.find(".")+1:] for coluna in colunas}
        df = df.rename(columns=novas_colunas)
        df.to_excel(os.path.join(self.output_dir, "movimento.xlsx"), index=None)
