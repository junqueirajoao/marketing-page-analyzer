# Como Executar o Backend

## Problema Resolvido

O erro "Network Error" / "Connection Refused" ocorria porque:
1. O frontend estava configurado para conectar na porta 8001
2. O backend não estava rodando nessa porta ou o CORS não permitia a origem do frontend

## Solução Implementada

### 1. CORS Atualizado
O backend agora aceita requisições de:
- `http://localhost:3000` (porta configurada no Vite)
- `http://127.0.0.1:3000`
- `http://localhost:5173` (porta padrão do Vite)
- `http://127.0.0.1:5173`

### 2. Scripts de Inicialização
Criados scripts para rodar o backend na porta 8001:

#### Windows (PowerShell):
```powershell
cd backend
.\run_server.ps1
```

#### Linux/Mac:
```bash
cd backend
chmod +x run_server.sh
./run_server.sh
```

#### Manualmente:
```bash
cd backend
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\Activate.ps1  # Windows

uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Verificação

1. **Backend rodando**: Acesse http://localhost:8001/docs
2. **Frontend rodando**: Execute `npm run dev` na pasta frontend
3. **Teste a conexão**: Tente analisar uma URL pelo frontend

## Portas Utilizadas

- **Backend**: 8001
- **Frontend**: 3000 (configurado no vite.config.ts)

## Troubleshooting

### Porta 8001 já em uso
```powershell
# Windows - encontrar processo na porta 8001
netstat -ano | findstr :8001
# Matar processo (substitua PID)
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8001 | xargs kill -9
```

### Virtual environment não encontrado
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate    # Linux/Mac
pip install -r requirements.txt
```

### Erro de CORS ainda persiste
Verifique se o frontend está rodando em uma das portas permitidas (3000 ou 5173).