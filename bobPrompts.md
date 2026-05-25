# Guia de Prompts - Marketing Page Analyzer

> Coleção organizada de prompts para desenvolvimento do projeto Bob-a-thon

---

## Fase 1: Estrutura Inicial do Backend

### Prompt 1: Criação da Base do Backend FastAPI

Seguindo o guia técnico em docs/guia-tecnico-hackathon.md, crie a base do backend FastAPI.

Objetivo desta etapa:
- Criar estrutura inicial do backend.
- Implementar GET /health.
- Implementar POST /analyze/briefing com fallback local mockado.
- Criar schemas Pydantic básicos.
- Manter o código simples e preparado para evoluir para scraping e IBM Consulting Advantage depois.

Não implemente frontend ainda.
Não implemente scraping ainda.
Não conecte IBM Consulting Advantage ainda.

---

### Prompt 2: Implementação dos Catálogos JSON

Seguindo o guia tecnico em docs/guia-tecnico-hackathon.md, implemente a proxima etapa do backend.

Contexto:
- O projeto ja tem backend FastAPI.
- O endpoint GET /health esta funcionando.
- O endpoint POST /analyze/briefing esta funcionando.
- A rota analyze.py chama app.services.report_builder.build_briefing_analysis_report.
- Quero manter tudo compativel com Windows e evitar acentos nos textos mockados por enquanto.

Objetivo desta etapa:
1. Criar os arquivos JSON em backend/app/data:
   - modules_catalog.json
   - storytelling_patterns.json
   - brand_rules.json

2. Criar um service:
   - backend/app/services/catalog_loader.py

3. O catalog_loader.py deve ter funcoes para carregar:
   - load_modules_catalog()
   - load_storytelling_patterns()
   - load_brand_rules()
   - load_all_catalogs()

4. As funcoes devem ler os arquivos JSON usando pathlib, considerando que o codigo roda a partir da pasta backend.

5. Atualizar report_builder.py para chamar load_all_catalogs() e usar os catalogos no retorno mockado, pelo menos incluindo um campo "catalog_context" com:
   - modules_available_count
   - storytelling_patterns_count
   - brand_rules_count

6. Nao conectar IBM Consulting Advantage ainda.
7. Nao implementar scraping ainda.
8. Nao implementar frontend ainda.
9. Manter o codigo simples, legivel e testavel.
10. Evitar textos com acentos por enquanto para nao gerar problema de encoding no PowerShell.

Depois da implementacao, explique quais arquivos foram criados ou alterados.

---

### Prompt 3: Implementação dos Catálogos JSON (Versão Atualizada)

Seguindo o guia tecnico local em docs/guia-tecnico-hackathon.md, implemente a proxima etapa do backend.

Contexto:
- O projeto ja tem backend FastAPI.
- O endpoint GET /health esta funcionando.
- O endpoint POST /analyze/briefing esta funcionando.
- A rota analyze.py chama app.services.report_builder.build_briefing_analysis_report.
- Quero manter tudo compativel com Windows e evitar acentos nos textos mockados por enquanto.
- O arquivo docs/guia-tecnico-hackathon.md existe localmente, mas esta no .gitignore e nao deve ser alterado nem preparado para commit.

Objetivo desta etapa:
1. Criar os arquivos JSON em backend/app/data:
   - modules_catalog.json
   - storytelling_patterns.json
   - brand_rules.json

2. Criar um service:
   - backend/app/services/catalog_loader.py

3. O catalog_loader.py deve ter funcoes para carregar:
   - load_modules_catalog()
   - load_storytelling_patterns()
   - load_brand_rules()
   - load_all_catalogs()

4. As funcoes devem ler os arquivos JSON usando pathlib, considerando que o codigo roda a partir da pasta backend.

5. Atualizar report_builder.py para chamar load_all_catalogs() e usar os catalogos no retorno mockado, pelo menos incluindo um campo "catalog_context" com:
   - modules_available_count
   - storytelling_patterns_count
   - brand_rules_count

6. Nao conectar IBM Consulting Advantage ainda.
7. Nao implementar scraping ainda.
8. Nao implementar frontend ainda.
9. Manter o codigo simples, legivel e testavel.
10. Evitar textos com acentos por enquanto para nao gerar problema de encoding no PowerShell.
11. Nao editar docs/guia-tecnico-hackathon.md.

Depois da implementacao, explique quais arquivos foram criados ou alterados.

---

## Fase 2: Correções e Padronizações

### Prompt 4: Correção de Chaves do Catálogo

A funcao load_all_catalogs() em backend/app/services/catalog_loader.py esta retornando chaves diferentes do contrato esperado.

**Erro ao testar:**
```
KeyError: 'modules_catalog'
```

**Padronize o retorno de load_all_catalogs() para usar exatamente estas chaves:**
```python
{
  "modules_catalog": [...],
  "storytelling_patterns": [...],
  "brand_rules": [...]
}
```

Tambem ajuste qualquer uso em report_builder.py para ler essas mesmas chaves.

Nao altere docs/guia-tecnico-hackathon.md.
Nao implemente novas features.
Apenas corrija a padronizacao das chaves e mantenha o endpoint /analyze/briefing funcionando.

---

### Prompt 5: Padronização de Chaves do Catálogo

A funcao load_all_catalogs() em backend/app/services/catalog_loader.py esta funcionando, mas o contrato precisa seguir o guia tecnico.

Hoje ela retorna:
- modules
- storytelling_patterns
- brand_rules

Altere para retornar exatamente:
- modules_catalog
- storytelling_patterns
- brand_rules

Tambem ajuste qualquer uso em backend/app/services/report_builder.py para usar catalogs["modules_catalog"] em vez de catalogs["modules"].

Nao altere docs/guia-tecnico-hackathon.md.
Nao implemente novas features.
Nao altere os arquivos JSON.
Apenas padronize a chave do catalogo de modulos.

---

## Fase 3: Análise de URLs

### Prompt 6: Implementação do Endpoint de Análise de URL

Seguindo o guia tecnico local em docs/guia-tecnico-hackathon.md, implemente a proxima etapa do backend.

Contexto:
- O backend FastAPI esta funcionando.
- GET /health funciona.
- POST /analyze/briefing funciona.
- report_builder.py usa LocalAgentFallback.
- LocalAgentFallback retorna agent_trace corretamente.
- load_all_catalogs() retorna:
  - modules_catalog
  - storytelling_patterns
  - brand_rules
- Quero manter tudo compativel com Windows.
- Evitar acentos nos textos mockados por enquanto.
- Nao alterar docs/guia-tecnico-hackathon.md.

Objetivo desta etapa:
1. Atualizar backend/app/schemas/input.py para adicionar um schema AnalyzeUrlRequest com:
   - url: HttpUrl
   - business_goal: Optional[str] = None
   - target_audience: Optional[str] = None
   - page_type_hint: Optional[str] = None

2. Atualizar backend/app/routes/analyze.py para adicionar:
   - POST /analyze/url

3. Criar em backend/app/services/report_builder.py uma funcao:
   - build_url_analysis_report(payload: AnalyzeUrlRequest) -> dict

4. Por enquanto, build_url_analysis_report deve usar LocalAgentFallback tambem, sem scraping real ainda.

5. O agent_payload para URL deve conter:
   - input_type: "url"
   - url: str(payload.url)
   - business_goal
   - target_audience
   - page_type_hint
   - catalogs

6. Como LocalAgentFallback hoje tem analyze_briefing(payload), ajuste advantage_client.py para tambem suportar:
   - analyze_url(payload: dict) -> dict

7. analyze_url pode reaproveitar a logica de analyze_briefing, mas deve retornar page_summary com:
   - detected_type: payload.page_type_hint or "unknown"
   - primary_goal: payload.business_goal or "nao_informado"
   - main_topic: "tema identificado a partir da url"

8. A resposta de /analyze/url deve manter o mesmo contrato:
   - analysis_id
   - score
   - page_summary
   - recommendations
   - module_plan
   - copy_suggestions
   - catalog_context
   - agent_trace

9. Nao implementar scraper.py ainda.
10. Nao implementar frontend ainda.
11. Nao conectar IBM Consulting Advantage real ainda.

Depois da implementacao, explique quais arquivos foram criados ou alterados.

---

## Fase 4: Correções do Agent Trace

### Prompt 7: Correção do Agent Trace no Endpoint de Briefing

O arquivo backend/app/services/advantage_client.py ja tem a classe LocalAgentFallback e ela retorna agent_trace corretamente.

Porem o endpoint POST /analyze/briefing ainda nao esta retornando agent_trace.

Corrija backend/app/services/report_builder.py para:
- importar load_all_catalogs de app.services.catalog_loader
- importar LocalAgentFallback de app.services.advantage_client
- montar um agent_payload com:
  - input_type: "briefing"
  - briefing
  - business_goal
  - target_audience
  - constraints
  - catalogs
- chamar LocalAgentFallback().analyze_briefing(agent_payload)
- retornar exatamente a resposta do fallback

Nao altere docs/guia-tecnico-hackathon.md.
Nao implemente novas features.
Nao altere os arquivos JSON.
Nao altere rotas se nao for necessario.

---

### Prompt 8: Correção do Agent Trace (Segunda Tentativa)

O teste direto de LocalAgentFallback funcionou e retornou agent_trace.

Comando testado:
from app.services.advantage_client import LocalAgentFallback; r=LocalAgentFallback().analyze_briefing(...); print(r.keys())

Resultado:
dict_keys(['analysis_id', 'score', 'page_summary', 'recommendations', 'module_plan', 'copy_suggestions', 'catalog_context', 'agent_trace'])

Mas o endpoint POST /analyze/briefing ainda nao retorna agent_trace.

Corrija backend/app/services/report_builder.py para usar LocalAgentFallback.

Requisitos:
- Importar load_all_catalogs de app.services.catalog_loader.
- Importar LocalAgentFallback de app.services.advantage_client.
- Em build_briefing_analysis_report(payload), carregar catalogs = load_all_catalogs().
- Montar agent_payload com:
  - input_type: "briefing"
  - briefing: payload.briefing
  - business_goal: payload.business_goal
  - target_audience: payload.target_audience
  - constraints: payload.constraints
  - catalogs: catalogs
- Instanciar LocalAgentFallback().
- Retornar LocalAgentFallback().analyze_briefing(agent_payload).
- Remover o mock antigo diretamente de report_builder.py.

Nao altere docs/guia-tecnico-hackathon.md.
Nao altere os JSONs.
Nao altere advantage_client.py.
Nao implemente novas features.

---

### Prompt 09: Substituição Completa do Report Builder

O endpoint POST /analyze/briefing ainda nao retorna agent_trace.

O teste direto de LocalAgentFallback funciona, entao o problema esta em report_builder.py.

Substitua completamente backend/app/services/report_builder.py por uma versao simples com este comportamento:

- importar AnalyzeBriefingRequest de app.schemas.input
- importar load_all_catalogs de app.services.catalog_loader
- importar LocalAgentFallback de app.services.advantage_client
- definir build_briefing_analysis_report(payload: AnalyzeBriefingRequest) -> dict
- dentro da funcao:
  - catalogs = load_all_catalogs()
  - agent_payload = {
      "input_type": "briefing",
      "briefing": payload.briefing,
      "business_goal": payload.business_goal,
      "target_audience": payload.target_audience,
      "constraints": payload.constraints,
      "catalogs": catalogs
    }
  - agent_client = LocalAgentFallback()
  - return agent_client.analyze_briefing(agent_payload)

Remova todo mock antigo de report_builder.py.
Nao altere docs/guia-tecnico-hackathon.md.
Nao altere advantage_client.py.
Nao altere os JSONs.

---

## Fase 5: Scraping e Normalização

### Prompt 10: Implementação de Scraping e Normalização

Seguindo o guia tecnico local em docs/guia-tecnico-hackathon.md, implemente a proxima etapa do backend: scraping e normalizacao simples para /analyze/url.

Contexto:
- O backend FastAPI esta funcionando.
- POST /analyze/briefing funciona.
- POST /analyze/url funciona com LocalAgentFallback.
- report_builder.py monta agent_payload para briefing e URL.
- LocalAgentFallback retorna agent_trace.
- load_all_catalogs() retorna modules_catalog, storytelling_patterns e brand_rules.
- Quero manter tudo compativel com Windows.
- Evitar acentos nos textos mockados por enquanto.
- Nao alterar docs/guia-tecnico-hackathon.md.

Objetivo desta etapa:
1. Criar ou atualizar backend/app/services/scraper.py.

2. Implementar uma funcao:
   - fetch_page(url: str) -> dict

3. fetch_page deve:
   - usar httpx
   - baixar o HTML da URL
   - usar timeout de 20 segundos
   - definir um User-Agent simples
   - retornar um dict com:
     - url
     - status_code
     - html
   - tratar erros retornando:
     - url
     - status_code: None
     - html: ""
     - error: mensagem do erro

4. Criar ou atualizar backend/app/services/page_normalizer.py.

5. Implementar uma funcao:
   - normalize_page(raw_page: dict) -> dict

6. normalize_page deve usar BeautifulSoup para extrair:
   - url
   - metadata:
     - title
     - meta_description
     - canonical
   - headings:
     - level
     - text
   - links:
     - text
     - href
   - images:
     - alt
     - src
   - main_text
   - modules: lista vazia por enquanto
   - error, se existir no raw_page

7. Atualizar build_url_analysis_report em report_builder.py para:
   - chamar fetch_page(str(payload.url))
   - chamar normalize_page(raw_page)
   - incluir normalized_page dentro do agent_payload enviado ao LocalAgentFallback

8. Atualizar LocalAgentFallback.analyze_url para:
   - ler normalized_page do payload
   - incluir no retorno um campo "page_diagnostics" com:
     - has_title
     - has_meta_description
     - headings_count
     - links_count
     - images_count
     - has_error

9. A resposta de /analyze/url deve manter:
   - analysis_id
   - score
   - page_summary
   - recommendations
   - module_plan
   - copy_suggestions
   - catalog_context
   - agent_trace
   - page_diagnostics

10. Nao conectar IBM Consulting Advantage real ainda.
11. Nao implementar frontend ainda.
12. Nao implementar deteccao real de modulos ainda.

Depois da implementacao, explique quais arquivos foram criados ou alterados.

---

### Prompt 11: Enriquecimento do Catálogo de Módulos

Seguindo o guia tecnico local em docs/guia-tecnico-hackathon.md, atualize o catalogo de modulos do backend.

Contexto:
- O projeto ja possui backend FastAPI funcionando.
- O endpoint POST /analyze/url funciona com LocalAgentFallback.
- O endpoint POST /analyze/briefing funciona com LocalAgentFallback.
- O catalog_loader.py carrega modules_catalog, storytelling_patterns e brand_rules.
- A task atual e P0: enriquecer o catalogo de modulos para melhorar as recomendacoes do Module Strategy Agent.
- Quero manter tudo compativel com Windows.
- Evitar acentos nos textos por enquanto para evitar problemas de encoding.
- Nao alterar docs/guia-tecnico-hackathon.md.

Objetivo:
1. Atualizar backend/app/data/modules_catalog.json para um catalogo mais rico.

2. Cada item do catalogo deve conter:
   - id
   - name
   - component_type
   - best_for
   - purpose
   - typical_position
   - content_slots
   - good_when
   - bad_when
   - recommendation_rules
   - avoid_when
   - storytelling_role
   - seo_notes

3. Criar pelo menos estes modulos:
   - Hero com CTA
   - Beneficios
   - Como funciona
   - FAQ
   - Prova social
   - Comparativo
   - Simulador
   - CTA final
   - Conteudo educativo
   - Cross-sell
   - Bloco regulatorio
   - Cards de produto

4. Manter o JSON valido.

5. Nao alterar o contrato de load_all_catalogs().
   Ele deve continuar retornando:
   - modules_catalog
   - storytelling_patterns
   - brand_rules

6. Se necessario, ajustar LocalAgentFallback apenas para continuar funcionando com o novo formato do catalogo.

7. Nao implementar deteccao real de modulos ainda.
8. Nao implementar scraping ainda.
9. Nao implementar frontend ainda.
10. Nao conectar IBM Consulting Advantage real ainda.

Depois da implementacao, explique quais arquivos foram alterados.

---

### Prompt 12: Implementação de Scraping (Versão Simplificada)

Seguindo o guia tecnico local em docs/guia-tecnico-hackathon.md, implemente a proxima task P0: Implementar scraping de paginas.

Contexto:
- O backend FastAPI esta funcionando.
- POST /analyze/briefing funciona.
- POST /analyze/url funciona com LocalAgentFallback.
- report_builder.py monta agent_payload para briefing e URL.
- LocalAgentFallback retorna agent_trace.
- load_all_catalogs() retorna modules_catalog, storytelling_patterns e brand_rules.
- modules_catalog foi enriquecido e agora possui 31 modulos.
- Quero manter tudo compativel com Windows.
- Evitar acentos nos textos mockados por enquanto.
- Nao alterar docs/guia-tecnico-hackathon.md.

Objetivo desta task:
1. Criar ou atualizar backend/app/services/scraper.py.

2. Implementar uma funcao:
   - fetch_page(url: str) -> dict

3. fetch_page deve:
   - usar httpx
   - baixar o HTML da URL
   - usar timeout de 20 segundos
   - definir um User-Agent simples
   - retornar um dict com:
     - url
     - status_code
     - html
     - error

4. Em caso de sucesso:
   - error deve ser None
   - html deve conter o HTML retornado
   - status_code deve conter o codigo HTTP

5. Em caso de erro:
   - url deve ser preservada
   - status_code deve ser None, se nao houver resposta
   - html deve ser string vazia
   - error deve conter mensagem curta do erro

6. Nao integrar ainda ao /analyze/url nesta task.
7. Nao criar page_normalizer.py ainda.
8. Nao alterar LocalAgentFallback.
9. Nao alterar report_builder.py.
10. Nao implementar frontend.
11. Nao conectar IBM Consulting Advantage real.

Depois da implementacao, explique quais arquivos foram criados ou alterados.

---

### Prompt 13: Implementação de Normalização (Versão Simplificada)

Seguindo o guia tecnico local em docs/guia-tecnico-hackathon.md, implemente a proxima task P0: Implementar normalizacao de paginas.

Contexto:
- O backend FastAPI esta funcionando.
- POST /analyze/url funciona com LocalAgentFallback.
- POST /analyze/briefing funciona com LocalAgentFallback.
- scraper.py ja existe e possui fetch_page como funcao async.
- fetch_page foi validado com URL valida e invalida.
- modules_catalog possui 31 modulos.
- Quero manter tudo compativel com Windows.
- Evitar acentos nos textos mockados por enquanto.
- Nao alterar docs/guia-tecnico-hackathon.md.

Objetivo desta task:
1. Criar ou atualizar backend/app/services/page_normalizer.py.

2. Implementar uma funcao:
   - normalize_page(raw_page: dict) -> dict

3. normalize_page deve usar BeautifulSoup para extrair:
   - url
   - metadata:
     - title
     - meta_description
     - canonical
   - headings:
     - level
     - text
   - links:
     - text
     - href
   - images:
     - alt
     - src
   - main_text
   - modules: lista vazia por enquanto
   - error, se existir no raw_page

4. Regras:
   - Se raw_page tiver error, preservar esse erro no resultado.
   - Se html estiver vazio, retornar campos vazios sem quebrar.
   - Limpar textos com strip.
   - Ignorar links sem href.
   - Ignorar imagens sem src.
   - Limitar main_text a no maximo 10000 caracteres para evitar payload gigante.
   - Nao implementar deteccao real de modulos ainda.
   - Nao integrar ao /analyze/url ainda.
   - Nao alterar LocalAgentFallback.
   - Nao alterar report_builder.py.
   - Nao implementar frontend.
   - Nao conectar IBM Consulting Advantage real.

Depois da implementacao, explique quais arquivos foram criados ou alterados.

---

### Prompt 14: Integração de Scraping ao Endpoint

Seguindo o guia tecnico local em docs/guia-tecnico-hackathon.md, implemente a proxima task P0: Integrar scraping ao /analyze/url.

Contexto:
- O backend FastAPI esta funcionando.
- POST /analyze/url funciona com LocalAgentFallback.
- scraper.py ja existe e possui fetch_page como funcao async.
- page_normalizer.py ja existe e possui normalize_page(raw_page).
- fetch_page foi validado com URL valida e invalida.
- normalize_page foi validado com URL valida e invalida.
- load_all_catalogs() retorna modules_catalog, storytelling_patterns e brand_rules.
- modules_catalog possui 31 modulos.
- Quero manter tudo compativel com Windows.
- Evitar acentos nos textos mockados por enquanto.
- Nao alterar docs/guia-tecnico-hackathon.md.

Objetivo desta task:
1. Atualizar backend/app/services/report_builder.py.

2. Alterar build_url_analysis_report para ser async se necessario.

3. Em build_url_analysis_report:
   - carregar catalogs com load_all_catalogs()
   - chamar raw_page = await fetch_page(str(payload.url))
   - chamar normalized_page = normalize_page(raw_page)
   - montar agent_payload contendo:
     - input_type: "url"
     - url: str(payload.url)
     - business_goal: payload.business_goal
     - target_audience: payload.target_audience
     - page_type_hint: payload.page_type_hint
     - catalogs: catalogs
     - normalized_page: normalized_page

4. Chamar LocalAgentFallback().analyze_url(agent_payload).

5. Atualizar backend/app/routes/analyze.py:
   - endpoint POST /analyze/url deve ser async se build_url_analysis_report for async
   - deve usar await build_url_analysis_report(payload)

6. Atualizar LocalAgentFallback.analyze_url em advantage_client.py para:
   - ler normalized_page do payload
   - continuar retornando o contrato atual
   - incluir um novo campo page_diagnostics

7. page_diagnostics deve conter:
   - has_title: true/false
   - has_meta_description: true/false
   - headings_count: numero de headings
   - links_count: numero de links
   - images_count: numero de imagens
   - has_error: true/false

8. A resposta de /analyze/url deve continuar retornando:
   - analysis_id
   - score
   - page_summary
   - recommendations
   - module_plan
   - copy_suggestions
   - catalog_context
   - agent_trace

9. E agora tambem deve retornar:
   - page_diagnostics

10. Nao implementar deteccao real de modulos ainda.
11. Nao implementar frontend ainda.
12. Nao conectar IBM Consulting Advantage real ainda.
13. Nao alterar o comportamento de /analyze/briefing.

Depois da implementacao, explique quais arquivos foram criados ou alterados.

---

### Prompt 15: Detecção Simples de Módulos

Seguindo o guia tecnico local em docs/guia-tecnico-hackathon.md, implemente a proxima task P0: Criar deteccao simples de modulos.

Contexto:
- O backend FastAPI esta funcionando.
- POST /analyze/url funciona.
- scraper.py possui fetch_page async e ja foi validado.
- page_normalizer.py possui normalize_page(raw_page) e ja foi validado.
- /analyze/url ja integra scraping e normalizacao.
- A resposta de /analyze/url ja retorna page_diagnostics.
- modules_catalog possui 31 modulos enriquecidos.
- Quero manter tudo compativel com Windows.
- Evitar acentos nos textos mockados por enquanto.
- Nao alterar docs/guia-tecnico-hackathon.md.

Objetivo desta task:
1. Criar ou atualizar backend/app/services/module_detector.py.

2. Implementar uma funcao:
   - detect_modules(normalized_page: dict, modules_catalog: list) -> list

3. A deteccao deve ser heuristica e simples, sem IA ainda.

4. Detectar pelo menos:
   - Hero / Main Banner
   - FAQ / Accordion
   - Benefits / Card with icon / Image Icon
   - CTA / Call to Action
   - Breadcrumb
   - Richtext

5. Usar sinais como:
   - headings
   - main_text
   - links
   - palavras-chave comuns
   - posicao aproximada
   - nomes/sinonimos/detection_hints do modules_catalog quando util

6. Cada modulo detectado deve retornar dict com:
   - id
   - type
   - matched_catalog_id
   - matched_catalog_name
   - title
   - text
   - position
   - confidence
   - evidence

7. Atualizar page_normalizer.py para:
   - manter modules como lista vazia por padrao
   - nao chamar detect_modules diretamente, para evitar dependencia circular

8. Atualizar report_builder.py para:
   - depois de normalize_page(raw_page), chamar detect_modules(normalized_page, catalogs["modules_catalog"])
   - salvar o resultado em normalized_page["modules"]
   - enviar normalized_page com modules preenchido para LocalAgentFallback

9. Atualizar LocalAgentFallback.analyze_url, se necessario, para:
   - incluir em page_diagnostics um campo modules_detected_count
   - nao quebrar o contrato atual

10. A resposta de /analyze/url deve continuar retornando:
   - analysis_id
   - score
   - page_summary
   - recommendations
   - module_plan
   - copy_suggestions
   - catalog_context
   - agent_trace
   - page_diagnostics

11. Nao conectar IBM Consulting Advantage real ainda.
12. Nao implementar frontend ainda.
13. Nao usar bibliotecas novas.

Depois da implementacao, explique quais arquivos foram criados ou alterados.

---

## Fase 6: Frontend

### Prompt 16: Criação do Frontend Inicial

Vamos implementar a próxima task P0: Criar frontend inicial.

Contexto do projeto:
Estamos no projeto Marketing Page Analyzer do Bob-a-thon.
Use sempre como referência o arquivo docs/guia-tecnico-hackathon.md.
O backend FastAPI já está funcionando em:
http://localhost:8001

Endpoints existentes:
GET /health
POST /analyze/briefing
POST /analyze/url

Importante:
Esta task é só o frontend inicial com formulário. A tela visual completa de resultado será a próxima task. Nesta entrega, basta permitir enviar briefing ou URL para o backend e mostrar a resposta JSON de forma simples para validar integração.

Stack desejada conforme guia:
- React
- Vite
- TypeScript
- Tailwind CSS
- Axios ou fetch wrapper
- Estrutura simples e compatível com Windows

Requisitos da task:
1. Criar pasta frontend na raiz do projeto, se ainda não existir.
2. Criar app React com Vite e TypeScript.
3. Configurar Tailwind CSS.
4. Criar uma tela inicial com:
   - Título: Marketing Page Analyzer
   - Breve descrição do produto
   - Abas ou seletor para escolher entre:
     - Análise por URL
     - Análise por briefing
5. Formulário de URL com campos:
   - url
   - business_goal
   - target_audience
   - page_type_hint
   - botão "Analisar URL"
6. Formulário de briefing com campos:
   - briefing
   - business_goal
   - target_audience
   - constraints, pode ser texto simples separado por vírgula
   - botão "Analisar briefing"
7. Criar um arquivo de API, por exemplo:
   frontend/src/lib/api.ts
   com funções:
   - analyzeUrl(payload)
   - analyzeBriefing(payload)
8. O frontend deve chamar:
   - POST http://localhost:8001/analyze/url
   - POST http://localhost:8001/analyze/briefing
9. Mostrar estado de loading enquanto analisa.
10. Mostrar mensagem de erro amigável se a chamada falhar.
11. Mostrar a resposta da API em um bloco JSON formatado na tela.
12. Não implementar ainda dashboard final, cards de score ou visualização de módulos. Isso fica para a próxima task.
13. Manter código simples, legível e organizado.

**Estrutura sugerida:**
```
frontend/
├── package.json
├── vite.config.ts
├── index.html
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── index.css
    ├── lib/
    │   └── api.ts
    └── components/
        ├── UrlAnalyzerForm.tsx
        ├── BriefingAnalyzerForm.tsx
        └── JsonResult.tsx
```

Critério de aceite:
- O usuário consegue rodar o frontend localmente.
- O usuário consegue escolher análise por URL ou briefing.
- O usuário consegue enviar os dados para o backend.
- A resposta da API aparece na tela em JSON formatado.
- Loading e erro básico aparecem corretamente.
- Não quebrar o backend.

**Comandos esperados para rodar:**

Backend:
```bash
cd "C:\Users\014590631\Documents\Projetos Python\Bob-a-thon\marketing-page-analyzer\backend"
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload --port 8001
```

Frontend:
```bash
cd "C:\Users\014590631\Documents\Projetos Python\Bob-a-thon\marketing-page-analyzer\frontend"
npm install
npm run dev
```

Ao finalizar, me entregue:
1. Arquivos criados/modificados.
2. Como rodar.
3. Como testar análise por URL.
4. Como testar análise por briefing.
5. Observações importantes.

---

## Fase 7: Configurações Finais

### Prompt 17: Correção de CORS

Corrigir CORS do backend FastAPI para permitir chamadas do frontend React.

**Contexto:**
- Frontend roda em `http://localhost:3000`
- Backend roda em `http://localhost:8001`
- Ao chamar POST /analyze/url pelo frontend, o navegador retorna CORS error e o preflight OPTIONS recebe 405

Tarefa:
No arquivo backend/app/main.py, adicionar ou corrigir CORSMiddleware do FastAPI.

**Configuração esperada:**

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(...)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Depois incluir as rotas...
```

**Manter as rotas existentes sem quebrar:**
- GET /health
- POST /analyze/briefing
- POST /analyze/url

**Critério de aceite:**
- O frontend consegue chamar /analyze/url sem CORS error
- O preflight OPTIONS não retorna 405
- O formulário de URL exibe o JSON de resposta na tela
- O formulário de briefing também funciona

