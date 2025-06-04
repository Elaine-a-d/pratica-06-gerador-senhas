
import requests # Para fazer requisições HTTP
import json     # Para trabalhar com JSON

def consultar_cep(cep):
    """
    Consulta informações de endereço na API ViaCEP a partir de um CEP.

    Args:
        cep (str): O CEP a ser consultado (apenas números).

    Returns:
        dict or None: Um dicionário com logradouro, bairro, cidade e estado,
                      ou None se o CEP for inválido ou ocorrer um erro.
    """
    # Remove qualquer caractere não numérico do CEP
    cep = ''.join(filter(str.isdigit, cep))

    # Verifica se o CEP tem o tamanho correto (8 dígitos)
    if len(cep) != 8:
        print("Erro: O CEP deve conter 8 dígitos.")
        return None

    # URL da API ViaCEP
    api_url = f"https://viacep.com.br/ws/{cep}/json/"

    try:
        # Faz a requisição GET para a API
        response = requests.get(api_url)
        
        # Levanta um erro HTTP para status de erro (4xx ou 5xx)
        response.raise_for_status() 
        
        # Analisa a resposta JSON
        dados_cep = response.json()
        
        # Verifica se o CEP foi encontrado (a ViaCEP retorna 'erro' se não encontrar)
        if 'erro' in dados_cep and dados_cep['erro'] == True:
            print(f"CEP '{cep}' não encontrado ou inválido.")
            return None
        
        # Extrai as informações relevantes
        logradouro = dados_cep.get('logradouro', 'Não informado')
        bairro = dados_cep.get('bairro', 'Não informado')
        cidade = dados_cep.get('localidade', 'Não informado') # 'localidade' é a cidade
        estado = dados_cep.get('uf', 'Não informado')         # 'uf' é o estado
        
        return {
            "logradouro": logradouro,
            "bairro": bairro,
            "cidade": cidade,
            "estado": estado
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API ViaCEP: {e}")
        return None
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON da API.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

def main():
    print("--- Consulta de Endereço por CEP ---")
    
    while True:
        cep_input = input("Digite o CEP (apenas números, ou 'sair' para finalizar): ")
        
        if cep_input.lower() == 'sair':
            print("Saindo do programa.")
            break
        
        # Remove caracteres não numéricos para garantir que apenas dígitos sejam passados
        cep_limpo = ''.join(filter(str.isdigit, cep_input))

        if not cep_limpo:
            print("Por favor, digite um CEP válido.")
            continue

        print(f"Consultando CEP: {cep_limpo}...")
        informacoes_endereco = consultar_cep(cep_limpo)
        
        if informacoes_endereco:
            print(f"\n--- Endereço Encontrado ---")
            print(f"Logradouro: {informacoes_endereco['logradouro']}")
            print(f"Bairro:     {informacoes_endereco['bairro']}")
            print(f"Cidade:     {informacoes_endereco['cidade']}")
            print(f"Estado:     {informacoes_endereco['estado']}")
            print(f"--------------------------\n")
        else:
            print("Não foi possível obter o endereço para o CEP fornecido. Tente novamente.")
            print("-" * 30) # Linha separadora

if __name__ == "__main__":
    main()
    