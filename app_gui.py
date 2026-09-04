import gradio as gr
import random

class ModuloAvancadoMonstro:
    def __init__(self):
        pass

    def gerar_biologia(self, estrutura, ambiente, poder):
        """Gera uma análise biológica resumida baseada nos dados do monstro."""
        dietas = {
            "vulcão": "Carnívoro/Litófago (consome minérios e enxofre para manter a temperatura interna).",
            "pico gelado": "Carnívoro (caçador de emboscada com alto acúmulo de gordura corporal).",
            "pantano": "Detritívoro/Ospedeiro (filtra toxinas da água e absorve matéria orgânica em decomposição)."
        }
        
        dieta = dietas.get(ambiente.lower(), "Onívoro adaptável ao ecossistema local.")
        
        biologia = (
            f"🧬 **ANÁLISE BIOLÓGICA DO MONSTRO**\n\n"
            f"• **Sistema Digestivo & Dieta:** {dieta}\n"
            f"• **Anatomia Interna:** Possui órgãos reforçados para suportar a energia do poder '{poder}'. "
            f"Sua estrutura ({estrutura}) apresenta articulações densas para estabilidade no habitat.\n"
            f"• **Termorregulação:** Adaptada estritamente ao ambiente {ambiente}, utilizando seu revestimento corporal para dissipar ou reter calor.\n"
            f"• **Ciclo de Vida:** Crescimento lento com pele/carapaça altamente resistente a traumas físicos."
        )
        return biologia

    def processar_visual_e_biologia(self, nome, estrutura, poder, ambiente, estilo_render):
        if not nome or not estrutura:
            return "Preencha as informações do monstro primeiro.", "Aguardando dados..."

        # 1. Análise Biológica
        biologia_result = self.gerar_biologia(estrutura, ambiente, poder)

        # 2. Construção do Prompt Simplificado para Imagem (Frontal e Lateral)
        # Substituído 'dimensao_estilo' por 'estilo_render'
        prompt_imagem = (
            f"Concept art sheet of a monster named {nome}, {estilo_render}, "
            f"front view and side view, simple background, clean design. "
            f"Base structure: {estrutura}. Environment traits: {ambiente}. Power source: {poder}."
        )

        status_prompt = (
            f"🎨 **Prompt Gerado para Imagem:**\n`{prompt_imagem}`\n\n"
            f"📌 **Estilo Selecionado:** {estilo_render}\n"
            f"📐 **Visualização:** Vista Frontal + Vista Lateral"
        )

        return biologia_result, status_prompt

# Instância do módulo complementar
modulo_extra = ModuloAvancadoMonstro()

# --- Construção da Interface Gradio ---
with gr.Blocks(title="Gerador Avançado de Monstros") as app_completo:
    gr.Markdown("# 🐉 Gerador de Monstros - Biologia e Conceito Visual")

    with gr.Tab("Análise Biológica e Concept Art"):
        gr.Markdown("### Insira os dados do monstro para gerar a biologia e o modelo visual (Frontal/Lateral)")
        
        with gr.Row():
            in_nome = gr.Textbox(label="Nome do Monstro", value="Ignisdrake")
            in_ambiente = gr.Dropdown(["Vulcão", "Pico Gelado", "Pantano"], label="Ambiente", value="Vulcão")
        
        with gr.Row():
            in_estrutura = gr.Textbox(label="Estrutura do Monstro", value="Quadrúpede escamado")
            in_poder = gr.Textbox(label="Poder Principal", value="Sopro de Impacto")

        with gr.Row():
            in_estilo = gr.Radio(["Modelo 2D (Sprite/Concept Art)", "Modelo 3D (Render/Wireframe)"], label="Estilo de Renderização", value="Modelo 2D (Sprite/Concept Art)")

        btn_gerar_tudo = gr.Button("Analisar Biologia e Gerar Conceito Visual", variant="primary")

        out_biologia = gr.Markdown(label="Biologia")
        out_status_visual = gr.Markdown(label="Configuração Visual")

        btn_gerar_tudo.click(
            fn=modulo_extra.processar_visual_e_biologia,
            inputs=[in_nome, in_estrutura, in_poder, in_ambiente, in_estilo],
            outputs=[out_biologia, out_status_visual]
        )

if __name__ == "__main__":
    app_completo.launch()