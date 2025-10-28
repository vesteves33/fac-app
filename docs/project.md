# 🗺️ Roadmap do Projeto: FinOps Insight Engine

Este documento detalha o roteiro de desenvolvimento do projeto, organizado por "Épicos" que representam os principais serviços de nuvem a serem analisados. Cada épico contém um conjunto de "Features" (funcionalidades) que agregam valor de otimização para aquele serviço específico.

## 🎯 Visão Geral do Roadmap

O desenvolvimento seguirá uma abordagem modular, focando em um serviço de cada vez para construir um conjunto robusto de análises. A prioridade inicial está nos serviços com maior impacto no custo: Computação, Armazenamento e Bancos de Dados.

---

## 💻 Épico 1: Análise de Instâncias de Computação (Virtual Machines)

**Objetivo:** Identificar todas as principais oportunidades de otimização para VMs, que representam a maior parcela dos custos na maioria dos ambientes.

**Provedores:** AWS EC2, GCP Compute Engine, Azure Virtual Machines.

### Features (Funcionalidades):

*   **[ ] Feature 1.1: Análise de Rightsizing (Dimensionamento Correto)**
    *   **Descrição:** Analisar métricas de performance (CPU, Memória) para identificar instâncias superprovisionadas e recomendar um tamanho menor e mais barato.
    *   **Critérios de Aceitação:**
        *   A análise considera o pico máximo de utilização para evitar impacto na performance.
        *   A recomendação sugere um tipo de instância específico (ex: de `m5.2xlarge` para `m5.large`).
        *   O potencial de economia mensal é calculado para cada recomendação.

*   **[ ] Feature 1.2: Análise de Otimização de Modelo de Compra**
    *   **Descrição:** Identificar cargas de trabalho estáveis que se beneficiariam de modelos de compra com desconto.
    *   **Critérios de Aceitação:**
        *   Recomendar a compra de **Savings Plans** ou **Instâncias Reservadas** para cargas de trabalho 24/7.
        *   Identificar cargas de trabalho não críticas (ex: dev, processamento em lote) como candidatas para **Instâncias Spot/Spot VMs**.
        *   Calcular a economia percentual e absoluta ao adotar os modelos sugeridos.

*   **[ ] Feature 1.3: Análise de Modernização de Geração de Instâncias**
    *   **Descrição:** Identificar instâncias que estão usando famílias de geração mais antiga (ex: `t2`, `m4` na AWS) e recomendar a migração para gerações mais novas (ex: `t3`, `m5`), que oferecem melhor performance por um custo menor.
    *   **Critérios de Aceitação:**
        *   A recomendação mapeia o tamanho da instância antiga para o equivalente na nova geração.
        *   A economia e o ganho de performance são destacados.

---

## 💽 Épico 2: Análise de Armazenamento em Bloco (Block Storage)

**Objetivo:** Reduzir custos associados a discos persistentes, que frequentemente se tornam ociosos ou são superprovisionados.

**Provedores:** AWS EBS, GCP Persistent Disk, Azure Disk Storage.

### Features (Funcionalidades):

*   **[ ] Feature 2.1: Detecção de Volumes Órfãos/Não Atachados**
    *   **Descrição:** Identificar volumes de disco que não estão atachados a nenhuma instância de computação há mais de X dias (ex: 30 dias).
    *   **Critérios de Aceitação:**
        *   A análise gera uma lista de IDs de volumes ociosos.
        *   O custo mensal de cada volume ocioso é calculado para mostrar a economia ao excluí-lo.

*   **[ ] Feature 2.2: Análise de Otimização de Tipo de Disco**
    *   **Descrição:** Analisar métricas de IOPS (operações de I/O por segundo) para identificar discos superprovisionados (ex: `io2`) que poderiam ser migrados para tipos mais baratos (ex: `gp3`).
    *   **Critérios de Aceitação:**
        *   A recomendação se baseia no pico de IOPS e throughput do disco.
        *   A economia mensal ao alterar o tipo de disco é calculada.

---

## 🗄️ Épico 3: Análise de Armazenamento de Objetos (Object Storage)

**Objetivo:** Otimizar os custos de armazenamento de dados, que podem crescer silenciosamente, através da gestão inteligente do ciclo de vida dos dados.

**Provedores:** AWS S3, GCP Cloud Storage, Azure Blob Storage.

### Features (Funcionalidades):

*   **[ ] Feature 3.1: Análise de Classes de Armazenamento (Storage Tiers)**
    *   **Descrição:** Analisar os padrões de acesso aos objetos para recomendar a movimentação de dados raramente acessados para classes de armazenamento mais baratas (ex: de S3 Standard para S3 Infrequent Access ou Glacier).
    *   **Critérios de Aceitação:**
        *   A análise identifica buckets ou prefixos com dados "frios".
        *   Recomenda a criação de **Políticas de Ciclo de Vida (Lifecycle Policies)** para automatizar a transição de dados.
        *   Estima a economia com base no volume de dados a ser movido.

---

## 🌐 Épico 4: Análise de Recursos de Rede

**Objetivo:** Identificar e eliminar custos de rede que são frequentemente esquecidos.

**Provedores:** AWS (Elastic IPs, NAT Gateways), GCP (Cloud NAT), Azure (Public IPs).

### Features (Funcionalidades):

*   **[ ] Feature 4.1: Detecção de IPs Públicos Não Associados**
    *   **Descrição:** Identificar endereços de IP públicos que estão alocados mas não associados a nenhum recurso ativo (VM, Load Balancer, etc.).
    *   **Critérios de Aceitação:**
        *   Gera uma lista de IPs ociosos.
        *   Calcula o pequeno, mas constante, custo de cada IP não associado.

*   **[ ] Feature 4.2: Otimização de Tráfego de NAT Gateway**
    *   **Descrição:** Analisar os logs de fluxo (VPC Flow Logs) para identificar se o tráfego que passa pelo NAT Gateway poderia ser redirecionado para um Gateway Endpoint (ex: para S3), que é gratuito.
    *   **Critérios de Aceitação:**
        *   Identifica os principais destinos do tráfego do NAT Gateway.
        *   Se o destino for um serviço AWS compatível, recomenda a configuração de um Gateway Endpoint.
        *   Estima a economia em taxas de processamento do NAT Gateway.

---

## 📈 Épico 5: Funcionalidades da Plataforma Central

**Objetivo:** Construir a base que unifica todas as análises e entrega o valor final ao usuário.

### Features (Funcionalidades):

*   **[ ] Feature 5.1: Painel de Maturidade FinOps**
    *   **Descrição:** Calcular e apresentar uma pontuação de maturidade (Crawl, Walk, Run) com base na quantidade de oportunidades identificadas vs. resolvidas.
    *   **Critérios de Aceitação:**
        *   O painel exibe métricas chave (ex: % de custos alocados por tags).
        *   O nível de maturidade é calculado para cada Épico de serviço.

*   **[ ] Feature 5.2: Relatório de Assessment Unificado**
    *   **Descrição:** Criar um endpoint principal que agrega todas as oportunidades encontradas, prioriza-as por impacto de economia e as apresenta em um relatório coeso.
    *   **Critérios de Aceitação:**
        *   O relatório inclui um resumo executivo com a economia total potencial.
        *   As oportunidades são agrupadas por serviço e priorizadas.
