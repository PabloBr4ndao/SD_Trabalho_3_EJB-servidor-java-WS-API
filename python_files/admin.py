import streamlit as st
import requests
import pandas as pd
import time

st.set_page_config(page_title="Monitor do Servidor", page_icon="🖥️", layout="wide")

BASE_URL = "http://localhost:8080"

st.title("🖥️ Painel de Controle do Servidor (Admin)")
st.markdown("Monitoramento em tempo real de todos os pedidos do SD Food.")

# Container para atualização automática
placeholder = st.empty()

while True:
    try:
        # Busca TODOS os pedidos do servidor (nova rota)
        response = requests.get(f"{BASE_URL}/admin/pedidos")
        
        with placeholder.container():
            if response.status_code == 200:
                dados = response.json()
                
                # Métricas do Topo
                total = len(dados)
                pendentes = sum(1 for p in dados if "Entregue" not in p.get('status', ''))
                faturamento = sum(p.get('preco', 0) for p in dados)
                
                kpi1, kpi2, kpi3 = st.columns(3)
                kpi1.metric("Total de Pedidos", total)
                kpi2.metric("Pedidos em Andamento", pendentes)
                kpi3.metric("Faturamento Total", f"R$ {faturamento:.2f}")
                
                st.divider()
                
                if total > 0:
                    # Cria tabela visual
                    df = pd.DataFrame(dados)
                    
                    # Seleciona e renomeia colunas para ficar bonito
                    cols_to_show = ['idPedido', 'nomeCliente', 'status', 'preco']
                    # Adiciona colunas específicas se existirem (para tratar comidas/bebidas juntos)
                    if 'nomePrato' in df.columns: cols_to_show.append('nomePrato')
                    if 'nomeBebida' in df.columns: cols_to_show.append('nomeBebida')
                    
                    # Mostra a tabela colorida
                    st.subheader("📋 Lista Geral de Pedidos")
                    st.dataframe(
                        df, 
                        column_config={
                            "status": st.column_config.TextColumn("Status", help="Status atual na cozinha/logística"),
                            "preco": st.column_config.NumberColumn("Valor", format="R$ %.2f")
                        },
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("Nenhum pedido registrado no servidor até o momento.")
            else:
                st.error("Erro ao conectar na rota /admin/pedidos. Você atualizou o Java?")
                
        # Atualiza a cada 2 segundos (Simulação de Real-Time)
        time.sleep(2)
        
    except Exception as e:
        with placeholder.container():
            st.error("🔴 Servidor Offline")
            st.warning("Certifique-se que o ApiServer.java está rodando.")
        time.sleep(5)