from flask import Flask, request, jsonify
import pandas as pd
import pdfplumber
import re
from flask_cors import CORS
import traceback
from modelo_categorizacao import carregar_modelo, prever_categoria

app = Flask(__name__)
CORS(app)

# Carregar o modelo de machine learning treinado
modelo_categorizador = carregar_modelo()
if not modelo_categorizador:
    print("Aviso: Modelo de categorização não carregado. A categorização automática não estará disponível.")

# Mapeamento de sinônimos de colunas
sinonimos_colunas = {
    "descricao": ["histórico", "detalhes", "description", "descrição", "desc", "hist", "nome"],
    "valor": ["valor", "valor final", "valor lançamento", "valor (r$)", "amount", "val"],
    "tipo": ["tipo", "tipo operação", "tipo de lançamento", "forma pagamento", "transaction_type"],
    "data": ["data", "data operação", "data lançamento", "time", "data movimentação"]
}

# Padrões para inferir tipos a partir da descrição (manter para tipos básicos)
padroes_tipo = {
    "Pix": r'\bpix\b',
    "Débito": r'\bdébito\b|\bdebito\b',
    "Crédito": r'\bcrédito\b|\bcredito\b',
}

# Dicionário de mapeamento de nomes de categorias para IDs
categoria_nome_para_id = {
    "Moradia": 1,
    "Saúde": 2,
    "Educação": 3,
    "Transporte": 4,
    "Alimentação": 5,
    "Lazer": 6,
    "Contas": 7,
    "Vestuário": 8,
    "Taxas": 9,
    "Salário": 10,
    "Outros": 11
}

def detectar_colunas(df):
    df.columns = df.columns.str.strip().str.lower()
    colunas_detectadas = {}

    for chave, lista_sinonimos in sinonimos_colunas.items():
        match = df.columns[df.columns.str.contains('|'.join(lista_sinonimos), case=False, na=False)]
        if not match.empty:
            colunas_detectadas[chave] = match[0]

    return colunas_detectadas

def inferir_tipo(descricao):
    desc = str(descricao).lower()
    for tipo, padrao in padroes_tipo.items():
        if re.search(padrao, desc):
            return tipo
    return "Outros"

def ler_csv(file):
    try:
        df = pd.read_csv(file, sep=None, engine='python', encoding='utf-8')
    except UnicodeDecodeError:
        file.stream.seek(0)
        df = pd.read_csv(file, sep=None, engine='python', encoding='latin1')
    return df

def ler_pdf(file):
    texto = ""
    with pdfplumber.open(file) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"

    linhas = texto.strip().split("\n")
    dados = []
    max_colunas = 0

    for linha in linhas:
        partes = re.split(r'\s{2,}', linha.strip())
        if isinstance(partes, list) and all(isinstance(p, str) for p in partes):
            if partes:
                dados.append(partes)
                max_colunas = max(max_colunas, len(partes))

    if not dados:
        return pd.DataFrame()

    potenciais_cabecalhos = dados[:5]
    cabecalho_encontrado_linha = -1
    colunas_detectadas_conteudo = {}
    colunas_indices = {}

    for num_linha, linha in enumerate(potenciais_cabecalhos):
        print(f"Tipo da linha {num_linha}: {type(linha)}")
        if isinstance(linha, list):
            for i, item in enumerate(linha):
                print(f"  Tipo do item {i}: {type(item)}, Valor: '{item}'")
            possivel_cabecalho = [str(item).lower().strip() for item in linha] # Inicializa aqui
            colunas_detectadas_linha = {}
            indices_usados_linha = set()

            for chave, lista_sinonimos in sinonimos_colunas.items():
                for sinonimo in lista_sinonimos:
                    for i, coluna in enumerate(possivel_cabecalho):
                        if i not in indices_usados_linha and sinonimo in coluna:
                            colunas_detectadas_linha[chave] = i
                            indices_usados_linha.add(i)
                            break
                    if chave in colunas_detectadas_linha:
                        break

            if len(colunas_detectadas_linha) >= 3 and 'descricao' in colunas_detectadas_linha and 'valor' in colunas_detectadas_linha and 'data' in colunas_detectadas_linha:
                cabecalho_encontrado_linha = num_linha
                colunas_detectadas_conteudo = colunas_detectadas_linha
                colunas_indices = {v: k for k, v in colunas_detectadas_conteudo.items()}
                break
        else:
            print(f"  Valor da linha (não é lista): '{linha}'")
            continue # Se a linha não for uma lista, simplesmente vá para a próxima iteração

    if cabecalho_encontrado_linha != -1:
        dados_tabela = []
        if len(dados) > cabecalho_encontrado_linha + 1:
            num_cols_esperadas = len(colunas_indices)
            for linha_dados in dados[cabecalho_encontrado_linha + 1:]:
                nova_linha = {}
                if isinstance(linha_dados, list) and len(linha_dados) >= num_cols_esperadas:
                    for indice, chave in colunas_indices.items():
                        nova_linha[chave] = linha_dados[indice]
                    dados_tabela.append(nova_linha)
                elif isinstance(linha_dados, list) and linha_dados:
                    linha_preenchida = linha_dados + [None] * (num_cols_esperadas - len(linha_dados))
                    for indice, chave in colunas_indices.items():
                        if indice < len(linha_preenchida):
                            nova_linha[chave] = linha_preenchida[indice]
                        else:
                            nova_linha[chave] = None
                    dados_tabela.append(nova_linha)
            df = pd.DataFrame(dados_tabela)
        else:
            df = pd.DataFrame()
    else:
        df = pd.DataFrame(dados)

    return df

@app.route('/api/uploadcsv', methods=['POST'])
def processar_csv():
    if 'file' not in request.files:
        return jsonify({'erro': 'Arquivo ausente'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'erro': 'Arquivo vazio'}), 400

    try:
        filename = file.filename.lower()
        if filename.endswith(".pdf"):
            df = ler_pdf(file)
        else:
            df = ler_csv(file)

        if df.empty:
            return jsonify({'erro': 'Nenhum dado encontrado no arquivo'}), 400

        mapeadas = detectar_colunas(df)
        campos_necessarios = ["descricao", "valor", "data"]

        if not all(campo in mapeadas for campo in campos_necessarios):
            return jsonify({'erro': f'Colunas obrigatórias ausentes. Detectadas: {mapeadas}. Conteúdo inicial: {df.head().to_dict(orient="records")}'}), 400

        df = df.rename(columns={mapeadas[campo]: campo for campo in campos_necessarios if campo in mapeadas})

        if 'tipo' in mapeadas:
            df = df.rename(columns={mapeadas['tipo']: 'tipo'})

        try:
            df["data"] = pd.to_datetime(df["data"], errors='coerce').dt.date
        except Exception as e:
            return jsonify({'erro': f'Erro ao converter a coluna "data": {str(e)}. Conteúdo da coluna: {df["data"].head().tolist()}'}), 400

        df = df.dropna(subset=["descricao", "valor", "data"])

        movimentacoes = []
        for _, row in df.iterrows():
            descricao = str(row["descricao"]).strip()
            try:
                valor = float(str(row["valor"]).replace(',', '.'))
            except ValueError:
                continue
            data_movimentacao = row["data"].isoformat()
            tipo_detectado = None

            if "tipo" in row and pd.notna(row["tipo"]):
                tipo_detectado = str(row["tipo"]).strip()
            else:
                tipo_detectado = inferir_tipo(descricao)

            # Tentar categorizar usando o modelo de ML se carregado
            categoria_nome_predita = None
            categoria_id_predita = None
            if modelo_categorizador:
                categoria_nome_predita = prever_categoria(modelo_categorizador, descricao)
                categoria_id_predita = categoria_nome_para_id.get(categoria_nome_predita)

            movimentacoes.append({
                "Descricao": descricao,
                "Valor": valor,
                "Tipo": tipo_detectado,
                "DataMovimentacao": data_movimentacao,
                "Categoria": {"Nome": categoria_nome_predita, "Id": categoria_id_predita}
            })

        return jsonify(movimentacoes)

    except Exception as e:
        traceback.print_exc()
        return jsonify({'erro': str(e)}), 500

if __name__ == "__main__":
    app.run(port=8000, debug=True, use_reloader=False)