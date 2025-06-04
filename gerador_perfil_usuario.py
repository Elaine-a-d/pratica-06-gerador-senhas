
import requests # Importa a biblioteca requests para fazer requisições HTTP
import json     # Importa o módulo json para trabalhar com dados JSON

def obter_perfil_usuario_aleatorio():
    """
    Obtém um perfil de usuário aleatório da API Random User Generator.

    Returns:
        dict or None: Um dicionário contendo os dados do usuário (nome, email, país)
                      ou None se ocorrer um erro na requisição ou parsing.
    """
    api_url = "https://randomuser.me/api/"
    
    try:
        # Faz a requisição GET para a API
        response = requests.get(api_url)
        
        # Levanta um erro HTTP para status de erro (4xx ou 5xx)
        response.raise_for_status() 
        
        # Analisa a resposta JSON
        dados = response.json()
        
        # Extrai as informações relevantes do primeiro usuário no resultado
        usuario = dados['results'][0]
        
        nome_completo = f"{usuario['name']['first']} {usuario['name']['last']}"
        email = usuario['email']
        pais = usuario['location']['country']
        
        return {
            "nome": nome_completo,
            "email": email,
            "pais": pais
        }
        
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar à API: {e}")
        return None
    except json.JSONDecodeError:
        print("Erro ao decodificar a resposta JSON da API.")
        return None
    except KeyError as e:
        print(f"Erro ao extrair dados do usuário. Chave ausente: {e}")
        return None
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return None

def main():
    print("Gerador de Perfil de Usuário Aleatório")
    print("--------------------------------------")
    
    while True:
        input("Pressione Enter para gerar um novo perfil de usuário (ou digite 'sair' para finalizar): ")
        
        comando = input().lower() # Captura a entrada do usuário após o Enter
        
        if comando == 'sair':
            print("Saindo do programa.")
            break
        
        perfil = obter_perfil_usuario_aleatorio()
        
        if perfil:
            print(f"\n--- Perfil Gerado ---")
            print(f"Nome: {perfil['nome']}")
            print(f"Email: {perfil['email']}")
            print(f"País: {perfil['pais']}")
            print(f"---------------------\n")
        else:
            print("Não foi possível gerar um perfil no momento. Tente novamente.")
            print("-" * 30)

if __name__ == "__main__":
    main()
    