import gradio as gr
import time
import os
import tempfile

# ==========================================
# FUNÇÃO DE PROCESSAMENTO CORRIGIDA
# ==========================================
def process_prompt(prompt, asset_type, output_format, resolution, color_mode):
    if not prompt or not prompt.strip():
        return "⚠️ Por favor, digite um prompt válido.", None, None

    # Simulação do tempo de inferência da IA
    time.sleep(1.5)
    
    # Criamos um arquivo temporário real para evitar erros no gr.Model3D e gr.File
    temp_dir = tempfile.gettempdir()
    
    # Exemplo simples de cubo em formato .OBJ (válido para o visualizador 3D)
    obj_content = """# Cubo 3D gerado pelo Aether3D
v -1.0 -1.0  1.0
v  1.0 -1.0  1.0
v  1.0  1.0  1.0
v -1.0  1.0  1.0
v -1.0 -1.0 -1.0
v  1.0 -1.0 -1.0
v  1.0  1.0 -1.0
v -1.0  1.0 -1.0
f 1 2 3 4
f 8 7 6 5
f 4 3 7 8
f 5 1 4 8
f 5 6 2 1
f 2 6 7 3
"""
    file_path = os.path.join(temp_dir, "asset_gerado.obj")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(obj_content)
    
    status_msg = f"✨ Asset gerado com sucesso! Prompt: '{prompt}' | Tipo: {asset_type} | Resolução: {resolution}px"
    
    # Retorna: Status (str), Preview 3D (caminho do arquivo), Arquivo de Download (caminho do arquivo)
    return status_msg, file_path, file_path

# ==========================================
# CUSTOMIZAÇÃO VISUAL: TEMA AZUL E LILÁS
# ==========================================
custom_css = """
body, .gradio-container {
    background: linear-gradient(135deg, #0d1b2a 0%, #1b1b3a 100%) !important;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}
.main-header {
    text-align: center;
    color: #a5b4fc;
    margin-bottom: 20px;
}
.main-header h1 {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #c084fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.primary-btn {
    background: linear-gradient(90deg, #2563eb, #9333ea) !important;
    border: none !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 8px !important;
}
.primary-btn:hover {
    background: linear-gradient(90deg, #1d4ed8, #7e22ce) !important;
}
.panel-box {
    background-color: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid #c084fc44 !important;
    border-radius: 12px !important;
    padding: 15px;
}
"""

# ==========================================
# INTERFACE DA INTELIGÊNCIA ARTIFICIAL
# ==========================================
with gr.Blocks(css=custom_css, title="Aether3D - IA de Modelagem 2D/3D") as app:
    
    with gr.Column(elem_classes=["main-header"]):
        gr.Markdown("# 🌀 Aether3D Studio")
        gr.Markdown("### Sistema de Geração de Modelos 2D/3D para Jogos e Impressão")

    with gr.Row():
        # PAINEL DE ENTRADA DO USUÁRIO
        with gr.Column(scale=1, elem_classes=["panel-box"]):
            gr.Markdown("#### 🎛️ Configurações do Prompt")
            
            user_prompt = gr.Textbox(
                label="Prompt de Criação",
                placeholder="Ex: 'Espada medieval com runas brilhantes' ou 'Monstro do pântano'...",
                lines=3
            )
            
            asset_type = gr.Radio(
                choices=[
                    "Peça Industrial / Impressão 3D",
                    "Entidade / Monstro / NPC (Jogo 3D)",
                    "Cenário / Asset Ambiental (Jogo 3D)",
                    "Sprite / Textura / UI (Jogo 2D)"
                ],
                value="Entidade / Monstro / NPC (Jogo 3D)",
                label="Tipo de Asset"
            )
            
            with gr.Accordion("⚙️ Parâmetros Técnicos Avançados", open=False):
                output_format = gr.Dropdown(
                    choices=[".STL (Impressão 3D)", ".OBJ (Jogos/3D)", ".FBX (Animação)", ".PNG (Sprites 2D)"],
                    value=".OBJ (Jogos/3D)",
                    label="Formato de Saída"
                )
                resolution = gr.Slider(
                    minimum=128, maximum=2048, step=128, value=512, label="Resolução da Malha/Textura"
                )
                color_mode = gr.Checkbox(label="Incluir Texturas/Materiais RGB", value=True)

            generate_btn = gr.Button("🚀 Gerar Modelagem", elem_classes=["primary-btn"])

        # PAINEL DE VISUALIZAÇÃO E DOWNLOAD
        with gr.Column(scale=1, elem_classes=["panel-box"]):
            gr.Markdown("#### 🖼️ Resultado & Exportação")
            
            status_output = gr.Textbox(label="Status do Processamento", interactive=False)
            
            # Model3D atualizado sem parâmetros legados
            model_preview = gr.Model3D(label="Visualizador 3D Interativo")
            
            download_file = gr.File(label="Baixar Arquivo Final")

    # Evento de clique corrigido (agora passa todos os inputs necessários)
    generate_btn.click(
        fn=process_prompt,
        inputs=[user_prompt, asset_type, output_format, resolution, color_mode],
        outputs=[status_output, model_preview, download_file]
    )

if __name__ == "__main__":
    app.launch()
    
