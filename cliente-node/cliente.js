const http = require('http');

// Configuração
const BASE_URL = 'http://localhost:8080';

// Função para fazer requisições
function request(method, path, params = null) {
    return new Promise((resolve, reject) => {
        
        // Monta os parâmetros na URL (Query String) igual ao Python
        if (params) {
            const query = new URLSearchParams(params).toString();
            path += '?' + query;
        }

        const options = {
            method: method,
            headers: { 'Content-Type': 'application/json' }
        };

        // Faz a chamada para a URL completa
        const req = http.request(BASE_URL + path, options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                try {
                    const json = JSON.parse(data);
                    resolve(json);
                } catch (e) {
                    // Se der erro (HTML ou 404), mostra o código
                    if (res.statusCode >= 400) {
                        console.error(`ERRO HTTP ${res.statusCode} na url: ${path}`);
                        resolve({ erro: true, code: res.statusCode });
                    } else {
                        resolve(data);
                    }
                }
            });
        });

        req.on('error', (e) => reject(e));
        req.end();
    });
}

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function run() {
    console.log("--- CLIENTE NODE.JS (INTEROPERABILIDADE) ---");
    
    try {
        // 1. Vamos usar a rota de COMIDA que sabemos que funciona no Python
        console.log("1. Buscando cardápio...");
        const menu = await request('GET', '/cardapio/comidas');
        console.log("CARDÁPIO RECEBIDO COM SUCESSO.");

        // 2. Fazer o Pedido
        console.log("\n2. Pedindo Lasanha (ID 3) via Node.js...");
        
        // Usamos '/pedir/comida' pois sabemos que ela existe
        const params = { 
            cliente: 'Cliente Node.js', 
            id: 3, 
            obs: 'Sem queijo extra' 
        };
        
        const pedido = await request('POST', '/pedir/comida', params);
        
        if (pedido.erro) {
            console.log("Erro no pedido. O servidor recusou a conexão.");
            return;
        }

        console.log("PEDIDO REALIZADO:", pedido);

        // 3. Rastrear
        if(pedido.idPedido) {
            console.log(`\n3. Rastreando Pedido #${pedido.idPedido}...`);
            
            // Loop de atualização
            for(let i=0; i<5; i++) {
                await sleep(3000); // Espera 3 segundos
                const st = await request('GET', `/pedido/${pedido.idPedido}/status`);
                
                console.log(`STATUS ATUAL: ${st.statusRestaurante} | ${st.statusLogistica}`);
                
                if (st.statusLogistica === 'Entregue') break;
            }
        }
    } catch (error) {
        console.log("Erro fatal na execução:", error);
    }
}

run();