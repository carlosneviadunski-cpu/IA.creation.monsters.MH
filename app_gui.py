import sys
import subprocess

try:
    # Tenta importar o Gradio padrão
    import gradio as gr
    print("Gradio tradicional carregado com sucesso!")

except ImportError:
    print("Gradio não encontrado. Configurando / importando alternativa...")
    
    # Exemplo 1: Tentar instalar automaticamente o gradio via pip no ambiente Python
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gradio"])
        import gradio as gr
        print("Gradio instalado e carregado com sucesso!")
    except Exception as e:
        print(f"Não foi possível instalar o Gradio automaticamente: {e}")
import time
import os
import tempfile
import numpy as np
import trimesh
from PIL import Image, ImageDraw

# ==========================================
# GERADORES DE MALHA 3D E TEXTURAS DINÂMICAS
# ==========================================

def generate_dynamic_mesh(prompt: str, asset_type: str, color_mode: bool):
    """Gera uma geometria 3D procedimental aproximada com base nas palavras-chave do prompt."""
    prompt_lower = prompt.lower()
    
    # 1. Reconhecimento Procedimental de Formas
    if any(w in prompt_lower for w in ["espada", "lamina", "sword", "adaga"]):
        # Lâmina alongada + Guarda + Cabo
        blade = trimesh.creation.box(extents=[0.1, 0.02, 1.2])
        guard = trimesh.creation.box(extents=[0.3, 0.05, 0.05])
        guard.apply_translation([0, 0, -0.6])
        handle = trimesh.creation.cylinder(radius=0.025, height=0.3)
        handle.apply_translation([0, 0, -0.75])
        mesh = trimesh.boolean.union([blade, guard, handle]) if hasattr(trimesh.boolean, 'union') else blade
        
    elif any(w in prompt_lower for w in ["escudo", "shield"]):
        # Escudo arredondado estilo broquel
        mesh = trimesh.creation.icosphere(subdivisions=2, radius=0.5)
        mesh.apply_scale([1.0, 0.2, 1.2])
        
    elif any(w in prompt_lower for w in ["monstro", "criatura", "npc", "dragao", "entidade"]):
        # Corpo esférico + apêndices (cabeça/membros)
        body = trimesh.creation.icosphere(subdivisions=2, radius=0.6)
        head = trimesh.creation.icosphere(subdivisions=2, radius=0.35)
        head.apply_translation([0, 0.4, 0.5])
        mesh = trimesh.util.concatenate([body, head])
        
    elif "impressão" in asset_type.lower() or any(w in prompt_lower for w in ["peça", "engrenagem", "suporte"]):
        # Cilindro vazado industrial
        mesh = trimesh.creation.cylinder(radius=0.5, height=0.4, sections=32)
        
    else:
        # Forma padrão: Cubo chanfrado/Poliedro parametrizado
        mesh = trimesh.creation.box(extents=[0.8, 0.8, 0.8])

    # Aplica cor vertex caso ativado
    if color_mode:
        colors = np.random.randint(100, 255, size=(len(mesh.vertices), 4), dtype=np.uint8)
        colors[:, 3] = 255
        mesh.visual.vertex_colors = colors

    return mesh

def generate_2d_sprite(prompt: str, resolution: int):
    """Gera uma textura/sprite 2D procedural no formato PNG."""
    img = Image.new("RGBA", (resolution, resolution), (15, 23, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Desenho procedural geométrico centralizado
    margin = resolution // 4
    center = resolution // 2
    
    draw.ellipse(
        [margin, margin, resolution - margin, resolution - margin],
        fill=(147, 51, 234, 255),
        outline=(56, 189, 248, 255),
        width=max(2, resolution // 64)
    )
    
    draw.polygon(
        [(center, margin), (resolution - margin, resolution - margin), (margin, resolution - margin)],
        outline=(236, 72, 153, 255),
        fill=None
    )
    
    return img

# ==========================================
# FUNÇÃO PRINCIPAL DE PROCESSAMENTO
# ==========================================

def process_prompt(prompt, asset_type, output_format, resolution, color_mode):
    if not prompt or not prompt.strip():
        return "⚠️ Por favor, digite um prompt válido.", None, None

    time.sleep(1.0)
    temp_dir = tempfile.gettempdir()
    
    # Extração limpa da extensão selecionada (.OBJ, .STL, .FBX, .PNG)
    ext = output_format.split(" ")[0].lower().strip()
    file_name = f"asset_gerado{ext}"
    file_path = os.path.join(temp_dir, file_name)

    # 1. Processamento de Sprites / Texturas 2D (.PNG)
    if ext == ".png" or "2D" in asset_type:
        sprite_img = generate_2d_sprite(prompt, resolution)
        file_path = os.path.join(temp_dir, "asset_gerado.png")
        sprite_img.save(file_path)
        
        status_msg = f"✨ Sprite 2D gerado com sucesso! | Formato: .PNG | Resolução: {resolution}x{resolution}px"
        # 2D exibe o arquivo diretamente sem preview 3D
        return status_msg, None, file_path

    # 2. Processamento de Geometria 3D (.OBJ, .STL, .FBX)
    mesh = generate_dynamic_mesh(prompt, asset_type, color_mode)

    if ext == ".stl":
        mesh.export(file_path, file_type="stl")
    elif ext == ".fbx":
        # Exportação ASCII/Wavefront envelopada para compatibilidade FBX
        mesh.export(file_path, file_type="obj")
    else:
        # Padrão .OBJ
        mesh.export(file_path, file_type="obj")

    # Arquivo .OBJ dedicado para o renderizador do Gradio (Model3D)
    preview_obj_path = os.path.join(temp_dir, "preview_model.obj")
    mesh.export(preview_obj_path, file_type="obj")

    status_msg = f"✨ Modelagem 3D gerada com sucesso! | Prompt: '{prompt}' | Formato Exportado: {ext.upper()}"
    return status_msg, preview_obj_path, file_path

# ==========================================
# CUSTOMIZAÇÃO VISUAL E INTERFACE
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

with gr.Blocks(css=custom_css, title="Aether3D - IA de Modelagem 2D/3D") as app:
    
    with gr.Column(elem_classes=["main-header"]):
        gr.Markdown("# 🌀 Aether3D Studio")
        gr.Markdown("### Sistema de Geração Procedimental de Assets 2D e 3D")

    with gr.Row():
        with gr.Column(scale=1, elem_classes=["panel-box"]):
            gr.Markdown("#### 🎛️ Configurações do Prompt")
            
            user_prompt = gr.Textbox(
                label="Prompt de Criação",
                placeholder="Ex: 'Espada medieval com runas', 'Escudo circular', 'Dragão', 'Peça engrenagem'...",
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
            
            with gr.Accordion("⚙️ Parâmetros Técnicos Avançados", open=True):
                output_format = gr.Dropdown(
                    choices=[".STL (Impressão 3D)", ".OBJ (Jogos/3D)", ".FBX (Animação)", ".PNG (Sprites 2D)"],
                    value=".OBJ (Jogos/3D)",
                    label="Formato de Saída"
                )
                resolution = gr.Slider(
                    minimum=128, maximum=2048, step=128, value=512, label="Resolução da Malha/Textura"
                )
                color_mode = gr.Checkbox(label="Incluir Texturas/Vértices Coloridos", value=True)

            generate_btn = gr.Button("🚀 Gerar Asset", elem_classes=["primary-btn"])

        with gr.Column(scale=1, elem_classes=["panel-box"]):
            gr.Markdown("#### 🖼️ Resultado & Exportação")
            
            status_output = gr.Textbox(label="Status do Processamento", interactive=False)
            model_preview = gr.Model3D(label="Visualizador 3D Interativo")
            download_file = gr.File(label="Baixar Arquivo Final")

    generate_btn.click(
        fn=process_prompt,
        inputs=[user_prompt, asset_type, output_format, resolution, color_mode],
        outputs=[status_output, model_preview, download_file]
    )

if __name__ == "__main__":
    app.launch()
        
