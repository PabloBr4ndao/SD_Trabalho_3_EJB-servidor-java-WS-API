# EJB-servidor-java-WS-API

# 🍴 API de Gerenciamento de Restaurante - Trabalho 3 (SD)

Este projeto consiste na implementação de um sistema distribuído para gerenciamento de um restaurante, utilizando uma arquitetura de **API REST**. O trabalho substitui a comunicação RMI/Sockets do trabalho anterior por um protocolo de requisição/resposta baseado em HTTP e JSON.

O sistema simula o fluxo de pedidos de um restaurante, onde múltiplos clientes (Web, Mobile/Terminal) consomem uma API centralizada, com processamento assíncrono de pedidos (Cozinha e Logística).

**👥Dupla:** Pablo Brandão Passos e Pedro Wilson Coelho Parreira.

---

## 🏛️ Arquitetura do Sistema

O projeto é composto por 3 camadas principais operando de forma independente:

1.  **Servidor Central (Backend - Java):**
    * Responsável pela lógica de negócios e persistência em memória.
    * Gerencia concorrência via **Threads** (Simulação de tempo de preparo e entrega).
    * Expõe endpoints REST (GET/POST) via HTTP.
    
2.  **Clientes (Frontend Heterogêneo):**
    * **Dashboard Web (Python + Streamlit):** Interface gráfica para clientes e painel administrativo em tempo real.
    * **Cliente CLI (Node.js):** Script de automação para simular pedidos via terminal.
    * **Cliente CLI (Python):** Script básico de interação via console.

3.  **Protocolo de Comunicação:**
    * Troca de mensagens via **JSON**, garantindo interoperabilidade entre linguagens diferentes.

---

## 🚀 Tecnologias Utilizadas

* **Java 17+** (Maven, Spark Framework, GSON)
* **Python 3.x** (Streamlit, Requests, Pandas)
* **Node.js** (Axios)
* **Batch Script** (Automação de execução no Windows)

---

## 📦 Como Executar o Projeto

### Pré-requisitos
* Java JDK (17 ou superior) e Maven instalados.
* Python instalado.
* Node.js instalado.

### 1. Instalação das Dependências

**Python (Bibliotecas do Streamlit):**
Na raiz do projeto, instale as dependências listadas:
```bash
pip install -r requirements.txt
```

---

**Node.js (Bibliotecas do Cliente):**
Entre na pasta do cliente node e instale o axios:
```bash
cd cliente-node
npm install axios
cd ..
```

### 2. Rodando o Sistema (Modo Automático 🚀)

Para facilitar a apresentação e testes, foi criado um script executável para Windows.

1.  Na pasta raiz do projeto, dê um clique duplo no arquivo **`init.bat`**.
2.  O script irá automaticamente:
    * Compilar o projeto Java (*Maven Clean Package*).
    * Iniciar o **Servidor API** (Porta 8080).
    * Iniciar o **Dashboard Admin** em background (Porta 8502).
    * Iniciar o **Site do Restaurante** em background (Porta 8501).
3.  Um menu interativo aparecerá no terminal mostrando o **IP da sua máquina** e as opções de controle.

### 3. Interagindo com o Sistema

Após rodar o `init.bat`, o Servidor será iniciado e você terá as seguintes opções de acesso:

* **📱 Acesso via Celular (Rede Local):**
    * Conecte o celular na mesma rede Wi-Fi do computador.
    * Acesse no navegador do celular: `http://[SEU_IP_MOSTRADO_NO_TERMINAL]:8501`
    * Realize pedidos e veja-os chegando no servidor.

* **💻 Acesso Admin (Computador):**
    * Abra no seu navegador: `http://localhost:8502`
    * Visualize os gráficos e status dos pedidos em tempo real.

* **⌨️ Clientes de Script (Menu do Terminal):**
    * No menu do `init.bat`, digite **`p`** e dê Enter para rodar o cliente de teste em **Python**.
    * No menu do `init.bat`, digite **`j`** e dê Enter para rodar o cliente de teste em **Node.js**.

---

## 📡 Endpoints da API

O servidor expõe as seguintes rotas principais:

| Método | Rota | Descrição |
| :--- | :--- | :--- |
| `GET` | `/cardapio` | Retorna a lista de itens disponíveis. |
| `POST` | `/pedido` | Recebe um novo pedido (JSON). |
| `GET` | `/pedidos` | Retorna todos os pedidos (Visão Admin). |
| `GET` | `/pedidos/{id}` | Retorna o status de um pedido específico (Polling). |

---

## 📝 Observações para Avaliação

* **Interoperabilidade:** O sistema demonstra clientes Python e Node conversando com o mesmo backend Java.
* **Concorrência:** O servidor processa pedidos em background (Cozinha/Entrega) sem bloquear novas requisições.
* **Mobilidade:** O sistema está configurado (`0.0.0.0`) para aceitar conexões externas na rede local, demonstrando transparência de localização.