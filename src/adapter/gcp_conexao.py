from src.port.conexao import ConexaoPort



class GCPConexao(ConexaoPort):
    def __init__(self, credentials_json: str, project_id: str):
        # self.credentials_json = credentials_json
        # self.project_id = project_id
        self.client = self.conectar(credentials_json, project_id)

    #Interface methods
    async def autenticar(self) -> bool:
        ...