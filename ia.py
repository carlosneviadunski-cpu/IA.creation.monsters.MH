
class CriadorDeMonstros:
    def __init__(self):
        # Base de conhecimento para validação do assunto
        self.palavras_chave_monstros = [
            "monstro", "criar", "analisar", "poder", "característica", 
            "habitat", "atributo", "combate", "fraqueza", "vantagem"
        ]
        self.monstros_criados = []

    def validar_assunto(self, texto):
        """Verifica se o texto está relacionado ao universo dos monstros."""
        texto_lower = texto.lower()
        return any(palavra in texto_lower for palavra in self.palavras_chave_monstros)

    def criar_monstro(self, nome, estrutura, poder, ambiente):
        """Combina a estrutura do monstro com as características do ambiente."""
        
        # Lógica de adaptação ao ambiente
        adaptacoes = {
            "vulcão": {
                "resistencia": "Imunidade a fogo e calor extremo",
                "aparencia_extra": "Pele de rocha vulcânica com fendas incandescentes",
                "efeito_poder": f"{poder} (causa dano adicional de queimadura)"
            },
            "pico gelado": {
                "resistencia": "Imunidade ao frio intenso e congelamento",
                "aparencia_extra": "Pelagem densa ou espinhos de gelo cristalizado",
                "efeito_poder": f"{poder} (pode desacelerar os alvos)"
            },
            "pantano": {
                "resistencia": "Imunidade a veneno e toxinas",
                "aparencia_extra": "Corpo coberto por lodo escuro e musgo",
                "efeito_poder": f"{poder} (deixa os alvos envenenados)"
            }
        }

        # Seleciona as características ambientais ou gera um padrão caso não esteja na lista
        env_info = adaptacoes.get(
            ambiente.lower(), 
            {
                "resistencia": f"Adaptação padrão ao ambiente {ambiente}",
                "aparencia_extra": f"Traços sutis de integração ao ambiente {ambiente}",
                "efeito_poder": poder
            }
        )

        monstro = {
            "nome": nome,
            "estrutura_base": estrutura,
            "poder_base": poder,
            "ambiente": ambiente,
            "aparencia_final": f"{estrutura} com {env_info['aparencia_extra']}",
            "poder_ambiente": env_info['efeito_poder'],
            "passiva_ambiental": env_info['resistencia']
        }

        self.monstros_criados.append(monstro)
        return monstro

    def analisar_monstro(self, nome_ou_pergunta):
        """Analisa monstros cadastrados. Bloqueia perguntas fora do escopo."""
        if not self.validar_assunto(nome_ou_pergunta):
            return "essa informação não temos"

        # Busca pelo monstro na lista de criados
        for m in self.monstros_criados:
            if m["nome"].lower() in nome_ou_pergunta.lower():
                return (
                    f"--- Análise de Monstro: {m['nome']} ---\n"
                    f"• Estrutura: {m['estrutura_base']}\n"
                    f"• Aparência Adaptada: {m['aparencia_final']}\n"
                    f"• Habitat: {m['ambiente']}\n"
                    f"• Habilidade Especial: {m['poder_ambiente']}\n"
                    f"• Resistência Passiva: {m['passiva_ambiental']}"
                )

        return "essa informação não temos"


# --- Exemplo de Uso ---

ia = CriadorDeMonstros()

# 1. Criando um monstro adaptado ao vulcão
monstro_1 = ia.criar_monstro(
    nome="Ignisdrake",
    estrutura="Quadrupede escamado de grande porte",
    poder="Sopro de Impacto",
    ambiente="Vulcão"
)

print("Monstro criado com sucesso!\n")

# 2. Pergunta válida sobre o monstro
print("Consulta 1:")
print(ia.analisar_monstro("Qual a análise do monstro Ignisdrake?"))

print("\n" + "="*40 + "\n")

# 3. Pergunta fora do escopo de monstros
print("Consulta 2:")
print(ia.analisar_monstro("Qual é a capital da França?"))

