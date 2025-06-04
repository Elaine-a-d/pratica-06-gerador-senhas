
import requests # Para fazer requisições HTTP
import json     # Para trabalhar com JSON
from datetime import datetime # Para formatar a data/hora

def consultar_cotacao(codigo_moeda):
    """
    Consulta a cotação de uma moeda estrangeira em relação ao BRL na AwesomeAPI.

    Args:
        codigo_moeda (str): O código da moeda a ser consultada (ex: "USD", "EUR", "GBP").

    Returns:
        dict or None: Um dicionário com as informações da cotação (valor atual,
                      máximo, mínimo, data/hora), ou None se ocorrer um erro.
    """
    # Garante que o código da moeda esteja em maiúsculas
    codigo_moeda = codigo_moeda.upper()

    # Formato da URL da AwesomeAPI para cotações de última atualização
    api_url = f"https://economia.awesomeapi.com.br/json/last/{codigo_moeda}-BRL"

    try:
        # Faz a requisição GET para a API
        response = requests.get(api_url)
        
        # Levanta um erro HTTP para status de erro (4xx ou 5xx)
        response.raise_for_status() 
        
        # Analisa a resposta JSON
        dados_cotacao = response.json()
        
        # A AwesomeAPI retorna um dicionário onde a chave é o par de moedas (ex: "USDBRL")
        # ou um erro se o par não for encontrado.
        chave_par_moeda = f"{codigo_moeda}BRL"

        if chave_par_moeda not in dados_cotacao:
            print(f"Erro: Moeda '{codigo_moeda}' não encontrada ou par de cotação inválido.")
            return None
        
        informacoes_moeda = dados_cotacao[chave_par_moeda]
        
        # Extrai as informações relevantes
        valor_atual = float(informacoes_moeda['bid'])
        valor_maximo = float(informacoes_moeda['high'])
        valor_minimo = float(informacoes_moeda['low'])
        
        # A data de criação vem como timestamp, formatamos para algo legível
        # A AwesomeAPI fornece 'create_date' no formato 'YYYY-MM-DD HH:MM:SS'
        data_atualizacao_str = informacoes_moeda['create_date']
        
        return {
            "moeda": codigo_moeda,
            "atual": valor_atual,
            "maximo": valor_maximo,
            "minimo": valor_minimo,
            "ultima_atualizacao": data_atualizacao_str # Já está formatada pela API
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a API: {e}")
        return None
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON da API. Resposta inválida.")
        return None
    except ValueError:
        print("Erro ao converter valores numéricos da cotação.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

def main():
    print("--- Consulta de Cotação de Moeda ---")
    print("Moedas comuns: USD (Dólar Americano), EUR (Euro), GBP (Libra Esterlina)")
    print("------------------------------------")
    
    while True:
        codigo_moeda_input = input("Digite o código da moeda (ex: USD, EUR) ou 'sair' para finalizar: ")
        
        if codigo_moeda_input.lower() == 'sair':
            print("Saindo do programa.")
            break
        
        # Remove espaços e valida se tem 3 letras
        codigo_moeda_limpo = codigo_moeda_input.strip().upper()
        if not (len(codigo_moeda_limpo) == 3 and codigo_moeda_limpo.isalpha()):
            print("Código da moeda inválido. Por favor, digite um código de 3 letras (ex: USD, EUR).")
            continue

        print(f"Consultando cotação para {codigo_moeda_limpo}...")
        informacoes_cotacao = consultar_cotacao(codigo_moeda_limpo)
        
        if informacoes_cotacao:
            print(f"\n--- Cotação {informacoes_cotacao['moeda']}/BRL ---")
            print(f"Valor Atual (Compra): R$ {informacoes_cotacao['atual']:.4f}")
            print(f"Valor Máximo (Dia):   R$ {informacoes_cotacao['maximo']:.4f}")
            print(f"Valor Mínimo (Dia):   R$ {informacoes_cotacao['minimo']:.4f}")
            print(f"Última Atualização:   {informacoes_cotacao['ultima_atualizacao']}")
            print(f"---------------------------------\n")
        else:
            print("Não foi possível obter a cotação. Tente novamente.")
            print("-" * 30) # Linha separadora

if __name__ == "__main__":
    main()
    