import gradio as gr

def gerar_analise_completa(nome, ambiente, estrutura, poder):
    # Lógica de fallback para campos vazios
    nome = nome if nome else "Ignisdrake"
    ambiente = ambiente if ambiente else "Vulcão"
    estrutura = estrutura if estrutura else "Quadrúpede escamado"
    poder = poder if poder else "Sopro de Impacto"

    # Conteúdo Biológico Simulado baseados na imagem
    biologia_html = f"""
    <div style='color: #E0E0E0; font-family: sans-serif;'>
        <h2 style='color: #FFFFFF; font-size: 1.2rem;'>🧬 ANÁLISE BIOLÓGICA DO MONSTRO</h2>
        <ul style='list-style-type: disc; padding-left: 20px; color: #E0E0E0;'>
            <li><strong>Sistema Digestivo & Dieta:</strong> Carnívoro/Litófago (consome minérios e enxofre).</li>
            <li><strong>Anatomia Interna:</strong> Possui órgãos reforçados para suportar a energia do poder '{poder}'. Sua estrutura ({estrutura}) apresenta articulações densas.</li>
            <li><strong>Termorregulação:</strong> Adaptada ao ambiente {ambiente}.</li>
            <li><strong>Ciclo de Vida:</strong> Crescimento lento com pele altamente resistente.</li>
        </ul>
    </div>
    """

    # URL de imagem simulada da imagem fornecida
    # Para uso real, você substituiria isso pelo output do seu modelo de IA.
    imagem_resultado = "https://raw.githubusercontent.com/username/repo/main/path/to/monster_concept_image.png"
    # Fallback para visualização se a URL acima não estiver configurada
    # imagem_resultado = "https://i.imgur.com/example_monster.png" # Substitua com sua imagem real

    config_visual_html = f"""
    <div style='color: #E0E0E0; font-family: sans-serif;'>
        <p>🎨 **Prompt Gerado para Imagem:** `Concept art sheet of a monster named {nome}, Model 2D (Sprite/Concept Art), front view and side view, simple background, clean design. Base structure: {estrutura}. Environment traits: {ambiente}. Power source: {poder}.`</p>
        <p>📐 **Visualização:** Vista Frontal + Vista Lateral</p>
    </div>
    """

    # O chat_box precisa de uma tupla: (mensagem_usuario, resposta_ia)
    return [("", "Análise biológica e conceito visual gerados. Veja os detalhes abaixo.")], imagem_resultado, biologia_html, config_visual_html

# CSS Customizado para emular o estilo da imagem fornecida
custom_css = """
.orange-border-box {
    border: 2px solid #D17D42 !important;
    border-radius: 20px !important;
    background-color: #1a1a1a !important;
    padding: 10px !important;
}
#sidebar-column {
    background-color: #1a1a1a;
    border-right: 1px solid #333;
    min-width: 200px !important;
    max-width: 200px !important;
}
#main-content-column {
    background-color: #1a1a1a;
}
.sidebar-item {
    color: #E0E0E0 !important;
    text-align: left !important;
    justify-content: flex-start !important;
    background: none !important;
    border: none !important;
}
.sidebar-item:hover {
    background-color: #333 !important;
}
#chat-input-row {
    border-top: 1px solid #333;
    padding-top: 10px;
}
#user-input-textbox textarea {
    background-color: #333 !important;
    color: #FFF !important;
    border: 1px solid #555 !important;
}
"""

with gr.Blocks(title="Gerador de Monstros - Biologia e Conceito Visual", css=custom_css, theme=gr.themes.Base()) as demo:
    with gr.Row():
        # --- Barra Lateral (Estilo da imagem fornecida) ---
        with gr.Column(scale=1, elem_id="sidebar-column"):
            gr.Markdown("## • • •")
            gr.Button("📚 biblioteca", variant="secondary", elem_classes=["sidebar-item"])
            gr.Button("+ nova conversa", variant="primary", elem_classes=["sidebar-item"])
            gr.Markdown("<br><br><br><br>") # Espaçamento simulado
            with gr.Row():
                gr.Image("https://cdn-icons-png.flaticon.com/512/2040/2040504.png", width=30, height=30, show_label=False)
                gr.Markdown("account")
            gr.Markdown("<br>")

        # --- Painel Principal ---
        with gr.Column(scale=4, elem_id="main-content-column"):
            gr.Markdown("# 🐉 Gerador de Monstros - Biologia e Conceito Visual")
            gr.Markdown("Análise Biológica e Concept Art")
            gr.Markdown("Insira os dados do monstro para gerar a biologia e o modelo visual (Frontal/Lateral)")

            # Área de Inputs (Estilo da imagem fornecida)
            with gr.Row(elem_classes=["orange-border-box"]):
                with gr.Column():
                    input_nome = gr.Textbox(label="Nome do Monstro", value="Ignisdrake", elem_id="monster-input-small")
                    input_ambiente = gr.Dropdown(["Vulcão", "Pico Gelado", "Pantano"], label="Ambiente", value="Vulcão", elem_id="monster-input-small")
                with gr.Column():
                    input_estrutura = gr.Textbox(label="Estrutura do Monstro", value="Quadrúpede escamado", elem_id="monster-input-small")
                    input_poder = gr.Textbox(label="Poder Principal", value="Sopro de Impacto", elem_id="monster-input-small")

            input_estilo = gr.Radio(
                ["Modelo 2D (Sprite/Concept Art)", "Modelo 3D (Render/Wireframe)"],
                label="Estilo de Renderização",
                value="Modelo 2D (Sprite/Concept Art)"
            )

            gr.Markdown("<br>")

            # Área de Saída (Estilo chat em duas colunas da imagem fornecida)
            with gr.Row():
                with gr.Column():
                    out_biologia = gr.HTML(label="Biologia", elem_classes=["orange-border-box"])
                with gr.Column():
                    # Para simular o chat da imagem, usamos componentes separados para a imagem e os prompts
                    with gr.Group(elem_classes=["orange-border-box"]):
                        out_imagem = gr.Image(label="Configuração Visual", show_label=False, interactive=False)
                        out_config_visual = gr.HTML(show_label=False)

            gr.Markdown("<br>")

            # Caixa de conversa inferior (Estilo chat da imagem fornecida)
            with gr.Row(elem_id="chat-input-row"):
                chat_box = gr.Chatbot(label="Conversa", show_label=False, elem_classes=["orange-border-box"], height=100)

            with gr.Row(elem_id="chat-input-row"):
                with gr.Column(scale=9):
                    user_input = gr.Textbox(
                        show_label=False,
                        placeholder="inicie sua conversa!",
                        container=False,
                        elem_id="user-input-textbox"
                    )
                with gr.Column(scale=1):
                    submit_btn = gr.Button("Enviar", variant="primary")

            # Função de disparo
            submit_btn.click(
                fn=gerar_analise_completa,
                inputs=[input_nome, input_ambiente, input_estrutura, input_poder],
                outputs=[chat_box, out_imagem, out_biologia, out_config_visual]
            )
            # Também permite enviar com o Enter na caixa de texto
            user_input.submit(
                fn=gerar_analise_completa,
                inputs=[input_nome, input_ambiente, input_estrutura, input_poder],
                outputs=[chat_box, out_imagem, out_biologia, out_config_visual]
            )

if __name__ == "__main__":
    demo.launch()
            
