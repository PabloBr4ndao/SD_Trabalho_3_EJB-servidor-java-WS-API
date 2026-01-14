import streamlit as st
import requests
import pandas as pd
import time

# Configuração da Página
st.set_page_config(page_title="SD Food", page_icon="🍽️", layout="wide")

BASE_URL = "http://localhost:8080"

st.title("🍽️ Sistema de Restaurante - SD Food")
st.markdown("### Cliente Web (Python + Streamlit) consumindo API Java")

# Sidebar para Status do Servidor
st.sidebar.header("Status do Sistema")
try:
    # Teste simples de conexão (tentando pegar cardápio)
    requests.get(f"{BASE_URL}/cardapio/comidas", timeout=2)
    st.sidebar.success("🟢 Servidor Java Conectado")
except:
    st.sidebar.error("🔴 Servidor Java Offline")
    st.sidebar.warning("Certifique-se que o Java está rodando na porta 8080")
    st.stop()

# --- COLUNA 1: CARDÁPIO ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📋 Cardápio Disponível")
    
    tipo_cardapio = st.radio("Selecione o tipo:", ["Comidas", "Bebidas"])
    
    endpoint = "comidas" if tipo_cardapio == "Comidas" else "bebidas"
    
    if st.button("Atualizar Cardápio"):
        try:
            resp = requests.get(f"{BASE_URL}/cardapio/{endpoint}")
            itens = resp.json()
            
            # Transformar JSON em Tabela Bonita
            df = pd.DataFrame(itens)
            st.dataframe(df, use_container_width=True)
            
            # Guardar itens na sessão para usar no formulário de pedido
            st.session_state['itens_atuais'] = itens
        except Exception as e:
            st.error(f"Erro ao buscar cardápio: {e}")

# --- COLUNA 2: FAZER PEDIDO ---
with col2:
    st.subheader("👨‍🍳 Realizar Pedido")
    
    with st.form("form_pedido"):
        nome_cliente = st.text_input("Seu Nome", "Cliente Web")
        
        # Seleção do prato 
        id_item = st.number_input("ID do Item (Veja na tabela ao lado)", min_value=0, step=1)
        obs = st.text_input("Observações", "Capricha!")
        
        enviar = st.form_submit_button("Enviar Pedido")
        
        if enviar:
            # Tenta definir a rota. Se for bebida, vamos tentar, mas sabemos que pode falhar
            tipo_rota = "comida" if tipo_cardapio == "Comidas" else "bebida"
            
            # URL completa para debug
            url_completa = f"{BASE_URL}/pedir/{tipo_rota}"
            params = {'cliente': nome_cliente, 'id': id_item, 'obs': obs}
            
            try:
                # Fazendo o POST para o Java
                res = requests.post(url_completa, params=params)
                
                # --- CORREÇÃO AQUI: Só tenta ler JSON se deu certo (200) ---
                if res.status_code == 200:
                    try:
                        dados_pedido = res.json()
                        st.success(f"Pedido #{dados_pedido['idPedido']} realizado com sucesso!")
                        st.session_state['ultimo_pedido'] = dados_pedido['idPedido']
                    except:
                        # Se deu 200 mas não veio JSON
                        st.warning("Pedido enviado, mas o servidor não retornou confirmação em JSON.")
                else:
                    # Se deu erro 404, 500, etc.
                    st.error(f"Erro do Servidor: {res.status_code}")
                    st.write(f"O servidor não encontrou a rota: {url_completa}")
                    st.info("Dica: Se você pediu BEBIDA e deu erro 404, é porque o servidor Java não programou a rota de bebidas.")

            except Exception as e:
                st.error(f"Erro de conexão grave: {e}")

# --- ÁREA DE RASTREAMENTO (EM BAIXO) ---
st.divider()
st.subheader("🚚 Rastreamento em Tempo Real")

if 'ultimo_pedido' in st.session_state:
    id_rastreio = st.session_state['ultimo_pedido']
    st.info(f"Monitorando Pedido #{id_rastreio}")
    
    col_status1, col_status2 = st.columns(2)
    placeholder_rest = col_status1.empty()
    placeholder_log = col_status2.empty()
    
    # Botão para atualizar status manualmente
    if st.button("🔄 Atualizar Status Agora"):
        try:
            r = requests.get(f"{BASE_URL}/pedido/{id_rastreio}/status")
            status = r.json()
            
            placeholder_rest.metric("Cozinha", status.get('restaurante', 'RU UFC'))
            placeholder_log.metric("Logística", status.get('logistica', 'Motoboy Delivery'))
            
            # Barra de progresso visual baseada no texto
            progresso = 0
            s_log = status.get('logistica', '')
            if "preparação" in s_log: progresso = 20
            elif "Saiu" in s_log: progresso = 60
            elif "Entregue" in s_log: progresso = 100
            st.progress(progresso)
            
        except:
            st.error("Não foi possível buscar o status.")
else:
    st.info("Faça um pedido acima para iniciar o rastreamento.")