from drivers.omie.connector import Omie  # Certifique-se de que o caminho está correto

class Extract:
    def __init__(self, nome, app_key, app_secret) -> None:
        self.omie = Omie(nome, app_key, app_secret)
    
    # Função geral que recebe todos os parâmetros necessários
    def extract(self, route, call, result_id, param=None, campos=None) -> dict:
        return self.omie.get(route, call, result_id, param=param, campos=campos)
    
    # Funções para extrair os dados
    def extract_empresas(self) -> dict:
        return self.extract("/v1/geral/empresas/", "ListarEmpresas", "empresas_cadastro")
    
    # PASSAR OS PARAMETROS AQUI
    def extract_notas_fiscais(self) -> dict:
        return self.extract("/v1/produtos/nfconsultar/", "ListarNF", "nfCadastro", param={"pagina": 1,
            "registros_por_pagina": 20,
            "apenas_importado_api": "N",
            "ordenar_por": "CODIGO"})
    
    def extract_contacorrente(self) -> dict:
        return self.extract("/v1/geral/contacorrente/", "ListarContasCorrentes", "ListarContasCorrentes")
    
    def extract_clientes(self):
        return self.extract("/v1/geral/clientes/", "ListarClientes", "clientes_cadastro")
    
    def extract_depatamentos(self):
        return self.extract("/v1/geral/departamentos/", "ListarDepartamentos", "departamentos")
    
    def extract_projetos(self):
        return self.extract("/v1/geral/projetos/", "ListarProjetos", "cadastro")
    
    def extract_categorias(self):
        return self.extract("/v1/geral/categorias/", "ListarCategorias", "categoria_cadastro")
    
    def extract_conta_receber(self):
        return self.extract("/v1/financas/contareceber/", "ListarContasReceber", "conta_receber_cadastro")
    
    def extract_conta_pagar(self):
        return self.extract("/v1/financas/contapagar/", "ListarContasPagar", "conta_pagar_cadastro")
    
    def extract_mf(self):
        return self.extract("/v1/financas/mf/", "ListarMovimentos", "movimentos", 
            param={
                "nPagina": 1,
                "nRegPorPagina": 100,
                "cTpLancamento": "CC",
            }, 
            campos={
                "detalhes": ["dDtConcilia", "cCPFCNPJCliente", "cCodCateg", "cGrupo", "cNatureza", "cNumParcela", "cOrigem", "cStatus", "cTipo", "dDtEmissao", "dDtPagamento", "dDtPrevisao", "dDtRegistro", "dDtVenc", "nCodCC", "nCodCliente", "nCodTitRepet", "nCodTitulo", "nValorTitulo", "cNumDocFiscal", "nValorCOFINS", "nValorCSLL", "nValorIR", "nValorPIS", "cNumTitulo", "cChaveNFe", "cCodProjeto", "cOperacao", "nCodNF"],
                "departamentos": ["nDistrValor"],
            })
