import streamlit as st
import math

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Orçamento Loja Elisa", page_icon="🛍️", layout="centered")

# --- FUNÇÕES ÚTEIS (Embutidas para não precisar de arquivos extras) ---
def format_brl(val):
    if val is None: return "R$ 0,00"
    return f"R$ {val:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# --- CSS PARA DEIXAR BONITO ---
st.markdown("""
<style>
    .stApp { background-color: #f0f2f6; }
    div[data-testid="stMetricValue"] { font-size: 1.8rem; color: #0068c9; }
    button[kind="primary"] { background-color: #0068c9; border: none; }
</style>
""", unsafe_allow_html=True)

# --- INÍCIO DO PROGRAMA ---
def main():
    st.title("🛍️ Loja Elisa | Orçamentos")
    st.markdown("---")

    # 1. Dados do Cliente
    col_cli, col_zap = st.columns([3, 1])
    nome_cliente = col_cli.text_input("Nome do Cliente", placeholder="Ex: Dona Maria")
    
    # 2. Estado da Memória
    if 'itens' not in st.session_state: st.session_state.itens = []

    # 3. Adicionar Produtos (Com enter funcionando)
    with st.container():
        st.markdown("### Adicionar Produto")
        c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
        item = c1.text_input("Descrição", key="txt_item")
        qtd = c2.number_input("Qtd", 1, 100, 1, key="num_qtd")
        preco = c3.number_input("Preço Unit.", 0.0, step=1.0, key="num_preco")
        
        c4.write("")
        c4.write("")
        if c4.button("➕ Incluir", type="primary"):
            if item and preco > 0:
                st.session_state.itens.append({"Item": item, "Qtd": qtd, "Preço": preco})
            else:
                st.toast("Preencha nome e preço!", icon="⚠️")

    # 4. Lista e Cálculos
    if st.session_state.itens:
        st.write("---")
        total_geral = 0
        texto_zap = f"*Olá{' ' + nome_cliente if nome_cliente else ''}! Aqui está seu orçamento da Loja Elisa:*\n\n"

        # Tabela Visual
        for i, p in enumerate(st.session_state.itens):
            total_item = p['Qtd'] * p['Preço']
            total_geral += total_item
            
            # Linha do item
            cl1, cl2, cl3 = st.columns([4, 2, 1])
            cl1.text(f"{p['Qtd']}x {p['Item']}")
            cl2.text(f"{format_brl(total_item)}")
            if cl3.button("❌", key=f"del_{i}"):
                st.session_state.itens.pop(i)
                st.rerun()
            
            texto_zap += f"▪️ {p['Qtd']}x {p['Item']} ({format_brl(p['Preço'])})\n"

        # --- CÁLCULO INTELIGENTE ---
        # 10% Desconto à vista
        total_pix = total_geral * 0.90
        
        # Parcelamento Escalonado
        parcelas = 1
        if total_geral < 60: parcelas = 1
        elif total_geral >= 300: parcelas = 10
        else:
            # Regra da Escada (de 30 em 30 reais)
            if total_geral < 90: parcelas = 2
            elif total_geral < 120: parcelas = 3
            elif total_geral < 150: parcelas = 4
            elif total_geral < 180: parcelas = 5
            elif total_geral < 210: parcelas = 6
            elif total_geral < 240: parcelas = 7
            elif total_geral < 270: parcelas = 8
            elif total_geral < 300: parcelas = 9
            
        valor_parcela = total_geral / parcelas

        # Texto Final Zap
        texto_zap += f"\n*💰 TOTAL: {format_brl(total_geral)}*"
        texto_zap += "\n\n--------------------------------"
        texto_zap += "\n*CONDIÇÕES DE PAGAMENTO:*"
        texto_zap += f"\n\n✅ *À VISTA (Pix/Dinheiro):*"
        texto_zap += f"\n➡️ *{format_brl(total_pix)}* (10% OFF)"
        texto_zap += f"\n\n💳 *CARTÃO DE CRÉDITO:*"
        if parcelas > 1:
            texto_zap += f"\n➡️ Até *{parcelas}x de {format_brl(valor_parcela)}* sem juros"
        else:
            texto_zap += f"\n➡️ 1x de {format_brl(total_geral)}"
        texto_zap += "\n--------------------------------"

        st.markdown("### 💰 Resumo")
        k1, k2, k3 = st.columns(3)
        k1.metric("Total", format_brl(total_geral))
        k2.metric("Pix (-10%)", format_brl(total_pix))
        k3.metric("Cartão", f"{parcelas}x {format_brl(valor_parcela)}")

        st.markdown("---")
        c_copy, c_clean = st.columns([3, 1])
        with c_copy:
            st.text_area("📲 Copie para o WhatsApp:", value=texto_zap, height=300)
        with c_clean:
            st.write("")
            st.write("")
            if st.button("🗑️ Limpar", type="primary"):
                st.session_state.itens = []
                st.rerun()

if __name__ == "__main__":
    main()