import gradio as gr

class ModuloAvancadoMonstro:
    def __init__(self):
        pass

    def gerar_biologia(self, estrutura, ambiente, poder):
        dietas = {
            "vulcão": "Carnívoro/Litófago (consome minérios e enxofre para manter a temperatura interna).",
            "pico gelado": "Carnívoro (caçador de emboscada com alto acúmulo de gordura corporal).",
            "pantano": "Detritívoro/Hospedeiro (filtra toxinas da água e absorve matéria orgânica em decomposição)."
        }
        
        dieta = dietas.get(ambiente.lower(), "Onívoro adaptável ao ecossistema local.")
        
        biologia = (
            f"🧬 **ANÁLISE BIOLÓGICA DO MONSTRO**\n\n"
            f"• **Sistema Digestivo & Dieta:** {dieta}\n\n"
            f"• **Anatomia Interna:** Possui órgãos reforçados para suportar a energia do poder '{poder}'. "
            f"Sua estrutura ({estrutura}) apresenta articulações densas para estabilidade no habitat.\n\n"
            f"• **Termorregulação:** Adaptada estritamente ao ambiente {ambiente}, utilizando seu revestimento corporal para dissipar ou reter calor.\n\n"
            f"• **Ciclo de Vida:** Crescimento lento com pele/carapaça altamente resistente a traumas físicos."
        )
        return biologia

    def processar_visual_e_biologia(self, nome, estrutura, poder, ambiente, estilo_render):
        if not nome or not estrutura:
            return "Preencha as informações do monstro primeiro.", "Aguardando dados...", None

        # 1. Análise Biológica
        biologia_result = self.gerar_biologia(estrutura, ambiente, poder)

        # 2. Prompt e Configuração
        prompt_imagem = (
            f"Concept art sheet of a monster named {nome}, {estilo_render}, "
            f"front view and side view, simple background, clean design. "
            f"Base structure: {estrutura}. Environment traits: {ambiente}. Power source: {poder}."
        )

        status_prompt = (
            f"🎨 **Prompt Gerado para Imagem:**\n`{prompt_imagem}`\n\n"
            f"📌 **Estilo Selecionado:** {estilo_render}\n\n"
            f"📐 **Visualização:** Vista Frontal + Vista Lateral"
        )

        # Placeholder de imagem para exibição gráfica
        imagem_exemplo = "https://placehold.co/600x400/222/orange?text=Conceito+Visual+Gerado"

        return biologia_result, status_prompt, imagem_exemplo

modulo_extra = ModuloAvancadoMonstro()

# CSS Customizado para aproximar do layout da imagem (bordas arredondadas e destaque laranja)
custom_css = """
.orange-border {
    border: 2px solid #ff7700 !important;
    border-radius: 18px !important;
}
.sidebar-box {
    border: 2px solid #ff7700 !important;
    border-radius: 20px !important;
    padding: 10px !important;
}
button.primary-btn {
    background-color: #ff5500 !important;
    color: white !important;
    border-radius: 12px !important;
}
"""

with gr.Blocks(title="Gerador Avançado de Monstros", css=custom_css, theme=gr.themes.Base()) as app_completo:
    
    with gr.Row():
        # --- Barra Lateral (Estilo da Interface de Origem) ---
        with gr.Column(scale=1, min_width=200, elem_classes=["sidebar-box"]):
            gr.Markdown("### ⚙️ Opções")
            btn_nova_conversa = gr.Button("+ Nova conversa", variant="secondary")
            gr.Markdown("---")
            gr.Markdown("📚 **Biblioteca**")
            gr.Markdown("⚙️ **Account / Configurações**")

        # --- Painel Principal ---
        with gr.Column(scale=4):
            gr.Markdown("# 🐉 Gerador de Monstros - Biologia e Conceito Visual")

            with gr.Tab("Análise Biológica e Concept Art"):
                gr.Markdown("Insira os dados do monstro para gerar a biologia e o modelo visual (Frontal/Lateral)")
                
                with gr.Row():
                    in_nome = gr.Textbox(label="Nome do Monstro", value="Ignisdrake")
                    in_ambiente = gr.Dropdown(["Vulcão", "Pico Gelado", "Pantano"], label="Ambiente", value="Vulcão")
                
                with gr.Row():
                    in_estrutura = gr.Textbox(label="Estrutura do Monstro", value="Quadrúpede escamado")
                    in_poder = gr.Textbox(label="Poder Principal", value="Sopro de Impacto")

                with gr.Row():
                    in_estilo = gr.Radio(
                        ["Modelo 2D (Sprite/Concept Art)", "Modelo 3D (Render/Wireframe)"],
                        label="Estilo de Renderização",
                        value="Modelo 2D (Sprite/Concept Art)"
                    )

                btn_gerar_tudo = gr.Button(
                    "Analisar Biologia e Gerar Conceito Visual",
                    variant="primary",
                    elem_classes=["primary-btn"]
                )

                # --- Exibição de Resultados em Lado a Lado ---
                with gr.Row():
                    with gr.Column(scale=1):
                        out_biologia = gr.Markdown(label="Biologia")
                    with gr.Column(scale=1):
                        out_imagem = gr.Image(label="Preview do Monstro", interactive=False)
                        out_status_visual = gr.Markdown(label="Configuração Visual")

                btn_gerar_tudo.click(
                    fn=modulo_extra.processar_visual_e_biologia,
                    inputs=[in_nome, in_estrutura, in_poder, in_ambiente, in_estilo],
                    outputs=[out_biologia, out_status_visual, out_imagem]
                )

            # Barra de interação inferior (estilo input de chat)
            with gr.Row(elem_classes=["orange-border"]):
                in_chat = gr.Textbox(
                    placeholder="Inicie sua conversa ou insira comandos adicionais...",
                    show_label=False,
                    container=False
                )

if __name__ == "__main__":
    app_completo.launch()
            
