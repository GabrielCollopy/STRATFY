# 🚀 Projeto: Stratfy

## 📋 Sumário

O projeto Stratfy é um site que tem como princípio possibilitar que seus usuários criem **dashboards para controle financeiro** de maneira dinâmica, com base em seus dados reais de extratos ou adicionados manualmente. O site conta com funcionalidades de criação de **gráficos e cartões personalizados** para atender às necessidades de cada usuário.

---

## ✨ Funcionalidades Principais

* **Criação de Dashboards Personalizadas:** Ferramentas para construir painéis financeiros dinâmicos.
* **Gestão de Dados Financeiros:** Importação de extratos (CSV) ou adição manual de dados.
* **Visualizações Interativas:** Geração de gráficos e cartões financeiros customizados.

---

## 🛠️ Tecnologias Utilizadas

O Stratfy é construído com uma arquitetura dividida entre Python e C#.

* **Backend Principal e Frontend:**
    * **C# (.NET 8+ SDK):** Utilizado no modelo ASP.NET MVC para o backend principal da aplicação e a renderização do frontend.
* **APIs e Geração de Dashboards:**
    * **Python 3.11:** Responsável pelas APIs de processamento de dados e a lógica de geração das dashboards.
    * **Bibliotecas Python Principais:**
        * `streamlit==1.45.1`: Para construção de interfaces interativas e dashboards.
        * `Flask==3.1.0`: Framework web para as APIs Python.
        * `flask-cors==6.0.1`: Para lidar com políticas de CORS nas APIs.
        * `scikit-learn==1.7.0`: Biblioteca de Machine Learning.
        * `scipy==1.15.3`: Biblioteca para computação científica.
        * `pandas`: Para manipulação e análise de dados.
        * `numpy`: Para computação numérica eficiente.
        * `pdfplumber`: Para extração de texto e dados de PDFs (possivelmente extratos).
        * `matplotlib`: Para geração de gráficos estáticos.
        * `plotly`: Para gráficos interativos.

---

## 💻 Pré-requisitos

Para configurar e rodar o projeto Stratfy, você precisará ter as seguintes ferramentas instaladas:

### 1. Linguagens e Runtimes

* **Python:** Versão 3.11
    * **Como instalar:** Faça o download em [python.org](https://www.python.org/downloads/).
* **SDK do .NET:** Versão compatível com .NET 8 ou superior.
    * **Como instalar:** Faça o download em [dotnet.microsoft.com/download](https://dotnet.microsoft.com/download).

### 2. Ambientes de Desenvolvimento (IDEs)

Embora o projeto possa ser executado via linha de comando, as seguintes IDEs são recomendadas para uma melhor experiência de desenvolvimento e depuração:

* **Visual Studio Code:** Para o desenvolvimento Python e gerenciamento geral do projeto.
    * **Como instalar:** Faça o download em [code.visualstudio.com](https://code.visualstudio.com/).
* **Visual Studio (Community Edition é suficiente):** Para o desenvolvimento em C# e ASP.NET MVC.
    * **Como instalar:** Faça o download em [visualstudio.microsoft.com/vs/community/](https://visualstudio.microsoft.com/vs/community/).

---

## ⚙️ Configuração do Projeto

### 1. Obtenção do Código-Fonte

* **Clone o repositório:**
    ```
    git clone https://github.com/GabrielCollopy/STRATFY.git
    ```
* **Download direto:** Caso você tenha recebido o projeto via arquivo ZIP, descompacte-o em um diretório de sua preferência.

### 2. Configuração e Criação do Banco de Dados

* Baixe o arquivo `CREATE DATABASE Stratfy.txt`  e execute seus comandos no SQL Server Management Studio para criar o banco de dados.

### 3. Configuração da Seção Python

* **Navegue até o diretório Python do projeto:**
    ```
    cd STRATFY\STRATFY Python
    ```
* **Instale as bibliotecas Python:** O projeto conta com um arquivo `requirements.txt` que lista todas as dependências Python. Execute o comando a seguir para instalá-las:
    ```
    pip install -r requirements.txt
    ```

---

## 🚀 Como Iniciar o Sistema

O Stratfy é composto por duas partes principais (Python e C#) que precisam ser executadas separadamente para que o sistema funcione corretamente.

### 1. Iniciar a Seção Python (APIs e Geração da Dashboard)

1.  **Verifique se você está no diretório correto:** O arquivo principal é `main.py` dentro de `STRATFY\STRATFY Python`.
    ```
    cd STRATFY\STRATFY Python
    ```
2.  **Execute o servidor Python:**
    ```
    python main.py
    ```
    Este comando iniciará as APIs Python responsáveis pela leitura de arquivos CSV e pela criação de dashboards. **Mantenha este terminal aberto enquanto estiver utilizando o sistema.**

### 2. Iniciar a Seção C# (Frontend e Backend Principal)

1.  **Navegue até o diretório raiz do projeto C#:**
    ```
    cd STRATFY\STRATFY
    ```
2.  **Execute a aplicação C#:**
    ```
    dotnet run
    ```
    Este comando compilará e iniciará a aplicação ASP.NET MVC. O terminal indicará o endereço (URL) onde a aplicação estará acessível, geralmente algo como `http://localhost:XXXX` (onde `XXXX` é um número de porta).

### 3. Acessando o Stratfy

Após iniciar ambas as seções (Python e C#), abra seu navegador web e acesse a URL fornecida pelo comando `dotnet run`. Você verá a interface do site Stratfy.

---

## 🧪 Testes C#

O projeto C# conta com testes. Para executá-los, você tem duas opções:

### Opção 1: Via Linha de Comando

* **Navegue até o diretório raiz do projeto C#:**
    ```
    cd STRATFY\STRATFY
    ```
* **Execute os testes:**
    ```
    dotnet test
    ```

### Opção 2: Via Visual Studio (Test Explorer)

* Abra a `solution (.sln)` do projeto Stratfy no Visual Studio.
* No menu superior, vá em "Test" > "Test Explorer".
* No painel do "Test Explorer", clique em "Run All Tests" (o ícone de um triângulo verde).
Você também pode selecionar testes específicos e executá-los individualmente.

---
