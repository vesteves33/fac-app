# FaC - FinOps as Code Insight Engine

**Um motor de análise e otimização de custos na nuvem, construído com FastAPI, para transformar dados de consumo em um roadmap de maturidade FinOps.**

---
## 🎯 Visão Geral do Projeto

O **FaC Insight Engine** é uma aplicação de backend desenvolvida em FastAPI que se conecta aos provedores de nuvem (AWS, Azure, GCP) para analisar dados de custo e utilização. O objetivo principal não é apenas *visualizar* os gastos, mas sim gerar um **relatório de assessment acionável**, que identifica oportunidades de otimização e mede o nível de maturidade FinOps do ambiente.

A aplicação foi projetada para capacitar equipes de Engenharia, Finanças e Negócios a colaborar e tomar decisões baseadas em dados, seguindo as melhores práticas do framework FinOps.

## ✨ Funcionalidades Principais

*   **Análise de Maturidade FinOps:** Avalia o ambiente com base no modelo **Crawl, Walk, Run**, analisando métricas como cobertura de tags, uso de modelos de compra com desconto e eficiência de recursos.
*   **Geração de Oportunidades de Otimização:** Identifica e prioriza ações concretas para reduzir custos, incluindo:
    *   **Recursos Ociosos:** Detecção de discos não atachados, IPs não associados, etc.
    *   **Rightsizing (Dimensionamento Correto):** Recomendações para redimensionar instâncias superprovisionadas com base na análise de performance histórica.
    *   **Otimização de Modelos de Compra:** Sugestões para adotar Instâncias Reservadas, Savings Plans ou Instâncias Spot.
    *   **Modernização de Cargas de Trabalho:** Identificação de oportunidades para migrar para serviços gerenciados ou arquiteturas mais eficientes.
*   **Relatórios Acionáveis:** Apresenta os resultados em um formato claro, mostrando o problema, a solução recomendada e o potencial de economia para cada oportunidade.
*   **API Robusta e Moderna:** Construída com **FastAPI**, oferecendo performance, documentação automática (Swagger/ReDoc) e facilidade de integração.

## 🛠️ Arquitetura e Tecnologias

*   **Backend:** Python 3.13+ com [FastAPI](https://fastapi.tiangolo.com/ )
*   **Conectores de Nuvem:** Bibliotecas `aioboto3` (AWS), `azure-sdk-for-python` (Azure), `google-cloud-python` (GCP).
*   **Dependências:** Gerenciadas com `Uv`.


## 🚀 Guia utilizando Docker
1. **Crie um container através da imagem**
    ```bash
    docker run vesteves33/fac-app:latest    
    ```

## 🚀 Guia utilizando Cluster Kubernetes (Minikube)
1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/vesteve33/finops_as_code_app.git
    cd finops_as_code_app
    ```    
2.  **Dê o apply dos manifestos**
    ```bash
    kubectl apply -f k8s/
    ```
3. **Exponha a URL do serviço**
    ```bash
    minikube service fac-service --url -n fac
    ```


## 🚀 Como Começar (Guia de Instalação)

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/vesteve33/finops_as_code_app.git
    cd finops_as_code_app
    ```

2.  **Instale as dependências:**
    ```bash
    uv install #TODO: Pesquisar para completar aqui
    ```

3.  **Configure as credenciais da nuvem:**
    (Instruções sobre como configurar as chaves de API para AWS/Azure/GCP, preferencialmente via variáveis de ambiente ).
    ```bash
    export AWS_ACCESS_KEY_ID="SUA_CHAVE_DE_ACESSO"
    export AWS_SECRET_ACCESS_KEY="SUA_CHAVE_SECRETA"
    export AWS_REGION="sua-regiao"
    ```

4.  **Execute a aplicação:**
    ```bash
    uvicorn src.main:app --host 0.0.0.0 --port 8080 --reload
    ```

5.  **Acesse a documentação da API:**
    Abra seu navegador e acesse `http://127.0.0.1:8080/` para ver a documentação interativa do Swagger UI. Aplicação com a rota raiz redirecionada para o Swagger


## 🗺️ Roadmap do Projeto
```
#TODO Modificar esse trecho de roadmap do projeto, ainda não há nada relacionado a esta parte
```
Consulte o nosso [Roteiro de Projeto](#2-roteiro-de-gestão-do-projeto-roadmap-inicial ) para ver as funcionalidades planejadas e o que vem a seguir. 