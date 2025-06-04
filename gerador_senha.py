
import random
import string

def gerar_senha_aleatoria(tamanho):
    """
    Gera uma senha aleatória com base no tamanho fornecido.
    A senha inclui letras maiúsculas, minúsculas, dígitos e caracteres especiais.

    Args:
        tamanho (int): O número de caracteres que a senha deve ter.

    Returns:
        str: A senha aleatória gerada.
    """
    # Define os conjuntos de caracteres que podem ser usados na senha
    letras_minusculas = string.ascii_lowercase
    letras_maiusculas = string.ascii_uppercase
    digitos = string.digits # '0123456789'
    # Caracteres especiais (pontuação), removendo aspas e barra invertida para evitar problemas comuns
    caracteres_especiais = string.punctuation.replace("'", "").replace('"', '').replace('\\', '')
    
    # Combina todos os tipos de caracteres em um único pool
    todos_caracteres = letras_minusculas + letras_maiusculas + digitos + caracteres_especiais
    
    # Garante que a senha tenha pelo menos um de cada tipo, se o tamanho permitir
    # Esta parte garante a 'diversidade' se o tamanho for suficiente
    senha = []
    if tamanho >= 4: # Se a senha for grande o suficiente, garanta diversidade
        senha.append(random.choice(letras_minusculas))
        senha.append(random.choice(letras_maiusculas))
        senha.append(random.choice(digitos))
        senha.append(random.choice(caracteres_especiais))
        # Preenche o restante da senha com caracteres aleatórios do pool completo
        for _ in range(tamanho - 4):
            senha.append(random.choice(todos_caracteres))
    else: # Para senhas menores, apenas sorteia do pool completo
        for _ in range(tamanho):
            senha.append(random.choice(todos_caracteres))
            
    # Embaralha a lista de caracteres para garantir a aleatoriedade
    random.shuffle(senha)
    
    # Converte a lista de caracteres de volta para uma string
    return "".join(senha)

def main():
    while True:
        try:
            # Pede o tamanho desejado da senha ao usuário
            tamanho_str = input("Informe a quantidade de caracteres para a senha (ou 'sair' para finalizar): ")
            
            if tamanho_str.lower() == 'sair':
                print("Saindo do gerador de senhas.")
                break
            
            tamanho_senha = int(tamanho_str)
            
            if tamanho_senha <= 0:
                print("Por favor, digite um número inteiro positivo para o tamanho da senha.")
                continue
            
            # Gera a senha
            senha_gerada = gerar_senha_aleatoria(tamanho_senha)
            
            print(f"Senha gerada: {senha_gerada}")
            print("-" * 30) # Linha separadora
            
        except ValueError:
            print("Entrada inválida. Por favor, digite um número inteiro.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

if __name__ == "__main__":
    main()
    