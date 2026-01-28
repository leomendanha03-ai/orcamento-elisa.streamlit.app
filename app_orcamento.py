import streamlit as st
import base64

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Orçamento Loja Elisa",
    page_icon="🛍️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 🖼️ ÁREA DA LOGO
# ==============================================================================
# Cole o código gigante que você enviou dentro das aspas abaixo:
SUA_LOGO_AQUI = "COLE_O_CODIGO_GIGANTE_AQUI" 
# ==============================================================================

# --- FUNÇÕES ÚTEIS ---
def format_brl(val):
    if val is None: return "R$ 0,00"
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- CSS PROFISSIONAL CORRIGIDO ---
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    
    /* Container Branco (Cards) */
    div.block-container { padding-top: 1rem; }
    .css-1r6slb0, .stVerticalBlock { 
        background-color: #ffffff; 
        padding: 15px; 
        border-radius: 12px; 
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    /* CORREÇÃO DOS NÚMEROS (Métricas) */
    div[data-testid="stMetricValue"] {
        font-size: 1.2rem !important; /* Diminui um pouco a fonte */
        font-weight: 700;
        color: #1e3a8a;
        word-wrap: break-word; /* Quebra linha se precisar */
        white-space: normal;   /* Permite ver o número todo */
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
    }
    
    /* Botões Padronizados */
    button[kind="primary"] {
        background-color: #1e3a8a;
        border: none;
        transition: 0.3s;
        width: 100%; /* Botão ocupa largura total da coluna */
        height: 46px; /* Altura fixa para alinhar com inputs */
        margin-top: 0px;
    }
    button[kind="primary"]:hover {
        background-color: #152c6b;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Botão de Lixeira (Secondary) */
    button[kind="secondary"] {
        border: 1px solid #ddd;
        color: #e53e3e;
        height: 46px; /* Mesma altura do input */
    }

    /* Inputs */
    .stTextInput input, .stNumberInput input {
        border-radius: 8px;
        height: 46px; /* Altura padronizada */
    }
    
    hr { margin: 1em 0; border-color: #eee; }
</style>
""", unsafe_allow_html=True)

def main():
    # --- CABEÇALHO ---
    if len(SUA_LOGO_AQUI) > 100:
        st.markdown(f"""
        <div style="display: flex; align-items: center; margin-bottom: 20px; border-bottom: 2px solid #eee; padding-bottom: 15px;">
            <img src="{SUA_LOGO_AQUI}" style="max-height: 80px; margin-right: 20px; border-radius: 8px;">
            <div>
                <h2 style="margin: 0; color: #1e3a8a;">Loja Elisa</h2>
                <p style="margin: 0; color: #666; font-size: 0.9rem;">Orçamento Rápido</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Cole o código da Logo no arquivo Python.")

    # --- CARD 1: INSERÇÃO ---
    with st.container():
        col_cli, col_vazio = st.columns([3, 1])
        nome_cliente = col_cli.text_input("Nome do Cliente", placeholder="Ex: Dona Maria")
        
        st.markdown("#### Adicionar Produto")
        
        # Estado da lista
        if 'itens' not in st.session_state: st.session_state.itens = []

        # --- CORREÇÃO DE ALINHAMENTO E TAMANHO ---
        # Ajustei as proporções: [4, 1.5, 2, 1.5] para dar espaço certo
        c1, c2, c3, c4 = st.columns([4, 1.5, 2, 1.5])
        
        with c1:
            item = st.text_input("Descrição", key="input_item", placeholder="Ex: Lençol Casal")
        with c2:
            qtd = st.number_input("Qtd", 1, 100, 1, key="input_qtd")
        with c3:
            preco = st.number_input("Preço (R$)", 0.0, step=5.0, format="%.2f", key="input_preco")
        
        with c4:
            # Esse espaço vazio empurra o botão para baixo, alinhando com as caixas de texto
            st.write("") 
            st.write("") 
            if st.button("➕ Add", type="primary", use_container_width=True):
                if item and preco > 0:
                    st.session_state.itens.append({"Item": item, "Qtd": qtd, "Preço": preco})
                    st.toast("Adicionado!", icon="✅")
                else:
                    st.toast("Preencha o valor", icon="⚠️")

    # --- CARD 2: LISTA E CÁLCULOS ---
    if st.session_state.itens:
        st.write("")
        with st.container():
            st.markdown("### 🛒 Itens")
            
            total_geral = 0
            saudacao = f"Olá, {nome_cliente}! " if nome_cliente else "Olá! "
            texto_zap = f"*{saudacao}Segue seu orçamento na Loja Elisa:*\n\n"

            for i, p in enumerate(st.session_state.itens):
                total_item = p['Qtd'] * p['Preço']
                total_geral += total_item
                
                # Proporção ajustada para o número não cortar
                cl1, cl2, cl3 = st.columns([5, 2.5, 1]) 
                
                with cl1:
                    st.markdown(f"**{p['Qtd']}x** {p['Item']}")
                with cl2:
                    # Exibe o valor alinhado e formatado
                    st.markdown(f"**{format_brl(total_item)}**")
                with cl3:
                    if st.button("🗑️", key=f"del_{i}", use_container_width=True):
                        st.session_state.itens.pop(i)
                        st.rerun()
                
                st.markdown("<hr style='margin: 5px 0; border-color: #f0f0f0;'>", unsafe_allow_html=True)
                texto_zap += f"▪️ {p['Qtd']}x {p['Item']} ({format_brl(p['Preço'])})\n"

            # Cálculos
            total_pix = total_geral * 0.90
            
            # Lógica de Parcelas
            parcelas = 1
            if total_geral < 60: parcelas = 1
            elif total_geral >= 300: parcelas = 10
            else:
                if total_geral < 90: parcelas = 2
                elif total_geral < 120: parcelas = 3
                elif total_geral < 150: parcelas = 4
                elif total_geral < 180: parcelas = 5
                elif total_geral < 210: parcelas = 6
                elif total_geral < 240: parcelas = 7
                elif total_geral < 270: parcelas = 8
                elif total_geral < 300: parcelas = 9
            
            valor_parcela = total_geral / parcelas

            # Rodapé WhatsApp
            texto_zap += f"\n*💰 TOTAL: {format_brl(total_geral)}*"
            texto_zap += "\n\n--------------------------------"
            texto_zap += f"\n\n✅ *À VISTA (Pix/Dinheiro):*"
            texto_zap += f"\n➡️ *{format_brl(total_pix)}* (10% OFF)"
            texto_zap += f"\n\n💳 *CARTÃO DE CRÉDITO:*"
            if parcelas > 1:
                texto_zap += f"\n➡️ Até *{parcelas}x de {format_brl(valor_parcela)}* sem juros"
            else:
                texto_zap += f"\n➡️ 1x de {format_brl(total_geral)}"
            texto_zap += "\n--------------------------------"
            texto_zap += "\n_Orçamento válido por 7 dias._"

            # Exibição dos Totais (Métricas lado a lado)
            st.markdown("#### Valores Finais")
            k1, k2, k3 = st.columns(3)
            k1.metric("Total", format_brl(total_geral))
            k2.metric("À Vista (-10%)", format_brl(total_pix))
            k3.metric(f"Cartão ({parcelas}x)", format_brl(valor_parcela))

            st.write("---")
            
            # Área de Cópia
            c_copia, c_limpa = st.columns([3, 1])
            with c_copia:
                st.text_area("📲 Copie para o WhatsApp:", value=texto_zap, height=150)
            with c_limpa:
                st.write("") 
                st.write("") 
                if st.button("🧹 Limpar", type="primary", use_container_width=True):
                    st.session_state.itens = []
                    st.rerun()

    st.markdown("<div style='text-align: center; margin-top: 30px; color: #aaa; font-size: 0.8rem;'>Sistema Loja Elisa</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
