import streamlit as st

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Orçamento Loja Elisa",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 🖼️ ÁREA DA LOGO (SUBSTITUA ABAIXO)
# ==============================================================================
# Cole o código gigante que você enviou dentro das aspas abaixo:
SUA_LOGO_AQUI = "COLE_O_CODIGO_GIGANTE_AQUI" 
# ==============================================================================

# --- FUNÇÕES ÚTEIS ---
def format_brl(val):
    if val is None: return "R$ 0,00"
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- CSS PROFISSIONAL ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    
    /* Estilo dos Cards */
    div.block-container { padding-top: 2rem; }
    .css-1r6slb0, .stVerticalBlock { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 15px; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    
    /* Títulos */
    h1, h2, h3 { color: #1e3a8a; font-family: sans-serif; }
    
    /* Botões */
    button[kind="primary"] {
        background-color: #1e3a8a;
        border: none;
        transition: 0.3s;
    }
    button[kind="primary"]:hover {
        background-color: #152c6b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Inputs */
    .stTextInput input, .stNumberInput input {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # --- CABEÇALHO PERSONALIZADO ---
    # Verifica se a logo foi colada, senão usa um texto padrão
    if len(SUA_LOGO_AQUI) > 100:
        logo_html = f"""
        <div style="display: flex; align-items: center; margin-bottom: 30px; border-bottom: 2px solid #eee; padding-bottom: 20px;">
            <img src="{SUA_LOGO_AQUI}" style="max-height: 100px; margin-right: 25px; border-radius: 8px;">
            <div>
                <h1 style="margin: 0; font-size: 2.5rem; color: #1e3a8a;">Loja Elisa</h1>
                <p style="margin: 0; color: #666; font-size: 1.1rem;">Sistema de Orçamentos</p>
            </div>
        </div>
        """
    else:
        logo_html = """
        <div style="padding: 20px; background-color: #fee; border-radius: 10px; margin-bottom: 20px; color: red;">
            ⚠️ <b>Atenção:</b> Você precisa colar o código da imagem na variável <code>SUA_LOGO_AQUI</code> dentro do arquivo Python.
        </div>
        <h1>Loja Elisa</h1>
        """
    
    st.markdown(logo_html, unsafe_allow_html=True)

    # --- CARD 1: INSERÇÃO ---
    with st.container():
        st.markdown("### 👤 Novo Pedido")
        col_cli, col_vazio = st.columns([3, 1])
        nome_cliente = col_cli.text_input("Nome do Cliente", placeholder="Ex: Dona Maria")
        
        st.write("---")
        
        # Estado da lista
        if 'itens' not in st.session_state: st.session_state.itens = []

        # Inputs de Produto
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        item = c1.text_input("Produto", key="input_item", placeholder="Ex: Cobre Leito King")
        qtd = c2.number_input("Qtd", 1, 100, 1, key="input_qtd")
        preco = c3.number_input("Preço (R$)", 0.0, step=5.0, format="%.2f", key="input_preco")
        
        c4.write("")
        c4.write("")
        if c4.button("➕ Adicionar", type="primary", use_container_width=True):
            if item and preco > 0:
                st.session_state.itens.append({"Item": item, "Qtd": qtd, "Preço": preco})
                st.toast("Adicionado!", icon="✅")
            else:
                st.toast("Preencha nome e preço", icon="⚠️")

    # --- CARD 2: LISTA E CÁLCULOS ---
    if st.session_state.itens:
        st.write("")
        with st.container():
            st.markdown("### 🛒 Resumo do Pedido")
            
            total_geral = 0
            # Montagem do texto do WhatsApp
            saudacao = f"Olá, {nome_cliente}! " if nome_cliente else "Olá! "
            texto_zap = f"*{saudacao}Segue seu orçamento na Loja Elisa:*\n\n"

            # Tabela Visual
            for i, p in enumerate(st.session_state.itens):
                total_item = p['Qtd'] * p['Preço']
                total_geral += total_item
                
                # Layout da linha
                cl1, cl2, cl3 = st.columns([4, 2, 1])
                cl1.markdown(f"**{p['Qtd']}x** {p['Item']}")
                cl2.text(f"{format_brl(total_item)}")
                if cl3.button("🗑️", key=f"del_{i}"):
                    st.session_state.itens.pop(i)
                    st.rerun()
                
                st.markdown("<hr style='margin: 5px 0; border-color: #f0f0f0;'>", unsafe_allow_html=True)
                texto_zap += f"▪️ {p['Qtd']}x {p['Item']} ({format_brl(p['Preço'])})\n"

            # Cálculos de Desconto/Parcelas
            total_pix = total_geral * 0.90
            
            parcelas = 1
            if total_geral < 60: parcelas = 1
            elif total_geral >= 300: parcelas = 10
            else:
                # Lógica da escada de 30 em 30
                if total_geral < 90: parcelas = 2
                elif total_geral < 120: parcelas = 3
                elif total_geral < 150: parcelas = 4
                elif total_geral < 180: parcelas = 5
                elif total_geral < 210: parcelas = 6
                elif total_geral < 240: parcelas = 7
                elif total_geral < 270: parcelas = 8
                elif total_geral < 300: parcelas = 9
            
            valor_parcela = total_geral / parcelas

            # Rodapé do WhatsApp
            texto_zap += f"\n*💰 TOTAL: {format_brl(total_geral)}*"
            texto_zap += "\n\n--------------------------------"
            texto_zap += "\n*CONDIÇÕES ESPECIAIS:*"
            texto_zap += f"\n\n✅ *À VISTA (Pix/Dinheiro):*"
            texto_zap += f"\n➡️ *{format_brl(total_pix)}* (10% de Desconto)"
            texto_zap += f"\n\n💳 *CARTÃO DE CRÉDITO:*"
            if parcelas > 1:
                texto_zap += f"\n➡️ Até *{parcelas}x de {format_brl(valor_parcela)}* sem juros"
            else:
                texto_zap += f"\n➡️ 1x de {format_brl(total_geral)}"
            texto_zap += "\n--------------------------------"
            texto_zap += "\n_Orçamento válido por 7 dias. Sujeito a disponibilidade de estoque._"

            # Exibição dos Totais
            st.markdown("#### Valores Finais")
            k1, k2, k3 = st.columns(3)
            k1.metric("Total", format_brl(total_geral))
            k2.metric("À Vista (-10%)", format_brl(total_pix), delta="Economia")
            k3.metric("Cartão", f"{parcelas}x {format_brl(valor_parcela)}")

            st.write("---")
            
            # Área de Cópia
            c_copia, c_limpa = st.columns([3, 1])
            with c_copia:
                st.text_area("📲 Copie para o WhatsApp:", value=texto_zap, height=250)
            with c_limpa:
                st.write("") 
                st.write("") 
                if st.button("🧹 Limpar", type="primary"):
                    st.session_state.itens = []
                    st.rerun()

    # Rodapé simples
    st.markdown("<div style='text-align: center; margin-top: 50px; color: #aaa; font-size: 0.8rem;'>Sistema Integrado Loja Elisa</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
