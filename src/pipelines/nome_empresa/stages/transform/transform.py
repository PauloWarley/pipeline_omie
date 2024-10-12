import pandas as pd
from pipelines.eucaliptus.stages.normalizedObj.normalizedObj import NormalizeObj

class Transform:
    def __init__(self) -> None:
        pass
    
    #Cada função serve para fazer a transformação em cada tabela, ou seja, se quisermos fazer um tratamento diferente para tal tabela, podemos fazer por estas funções
    def transform_empresas(self, empresas_data: dict) -> pd.DataFrame:
        df = pd.DataFrame.from_records(empresas_data)
        return df
    
    # ALTERAR PARA NOTAS FISCAIS
    def transform_notas_fiscais(self, notas_fiscais: dict) -> pd.DataFrame:
        lista_nota_fiscal = []
        for nota_fiscal in notas_fiscais:
            del nota_fiscal["det"]
            del nota_fiscal["titulos"]
            normObj = NormalizeObj()
            lista_nota_fiscal.append( normObj.linearilize_object(nota_fiscal) )
        df = pd.DataFrame.from_records(lista_nota_fiscal)
        return df
    
    # ALTERAR PARA NOTAS FISCAIS
    def transform_notas_fiscais_produtos(self, notas_fiscais: dict) -> pd.DataFrame:
        lista_nota_fiscal_produtos = []
        for nota_fiscal in notas_fiscais:
            keys_to_keep = ["det", "compl"]
            nota_fiscal_produto = {chave: nota_fiscal[chave] for chave in keys_to_keep}
            normObj = NormalizeObj()
            lista_nota_fiscal_produtos.append(normObj.linearilize_object(nota_fiscal_produto) )

            # nota_fiscal_prods = []
            for prod in nota_fiscal_produto["det"]:
                nf_prod = {}
                nf_prod["compl"] = nota_fiscal_produto["compl"]
                nf_prod["det"] = normObj.linearilize_object( prod)
                
                lista_nota_fiscal_produtos.append(normObj.linearilize_object( nf_prod ))

        df = pd.DataFrame.from_records(lista_nota_fiscal_produtos)
        df = df.drop('det', axis=1)
        return df

    def transform_contacorrente(self, contacorrente_data: dict) -> pd.DataFrame:
        df = pd.DataFrame.from_records(contacorrente_data)
        return df

    def transform_clientes(self, clientes_data: dict) -> pd.DataFrame:
        df = pd.DataFrame.from_records(clientes_data)
        return df

    def transform_departamentos(self, departamentos_data: dict) -> pd.DataFrame:
        df = pd.DataFrame.from_records(departamentos_data)
        return df

    def transform_projetos(self, projetos_data: dict) -> pd.DataFrame:
        df = pd.DataFrame.from_records(projetos_data)
        return df

    def transform_categorias(self, categorias_data: dict) -> pd.DataFrame:
        df = pd.DataFrame.from_records(categorias_data)
        return df

    def transform_conta_receber(self, conta_receber_data: dict) -> pd.DataFrame:
        df = pd.DataFrame.from_records(conta_receber_data)
        return df

    def transform_conta_pagar(self, conta_pagar_data: dict) -> pd.DataFrame:
        df = pd.DataFrame.from_records(conta_pagar_data)
        return df

    def apply_transformations(self, data: dict, data_type: str) -> pd.DataFrame:
        if data_type == "empresas":
            return self.transform_empresas(data)
        elif data_type == "contacorrente":
            return self.transform_contacorrente(data)
        elif data_type == "clientes":
            return self.transform_clientes(data)
        elif data_type == "departamentos":
            return self.transform_departamentos(data)
        elif data_type == "projetos":
            return self.transform_projetos(data)
        elif data_type == "categorias":
            return self.transform_categorias(data)
        elif data_type == "conta_receber":
            return self.transform_conta_receber(data)
        elif data_type == "conta_pagar":
            return self.transform_conta_pagar(data)
        else:
            raise ValueError(f"Tipo de dado desconhecido: {data_type}")
