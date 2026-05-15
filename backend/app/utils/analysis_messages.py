"""
Centralized Portuguese messages for analysis evidence and user-facing text.
All user-visible strings should be defined here to maintain consistency.
"""

# Module detection evidence messages
MODULE_EVIDENCE = {
    # Breadcrumb
    "breadcrumb_links_found": "Encontrados {count} links de navegação breadcrumb",
    "breadcrumb_keywords": "Links contêm palavras-chave de navegação",
    
    # Hero / Main Banner
    "hero_h1_found": "H1 encontrado no início",
    "hero_keywords": "Palavras-chave de hero detectadas",
    "hero_images": "Imagens presentes",
    "hero_cta": "CTA detectado",
    
    # Richtext
    "richtext_content": "Conteúdo textual substancial ({chars} caracteres)",
    "richtext_paragraphs": "Múltiplos parágrafos detectados ({count} sentenças)",
    
    # Image with text
    "image_text_images": "Imagens presentes: {count}",
    "image_text_benefits": "Palavras-chave de benefícios detectadas",
    "image_text_combination": "Combinação de texto e imagem",
    
    # Accordion / FAQ
    "accordion_questions": "Encontradas {count} perguntas",
    "accordion_faq_keywords": "Palavras-chave de FAQ presentes",
    "accordion_question_patterns": "Padrões de pergunta detectados",
    
    # Carousel
    "carousel_images": "Múltiplas imagens presentes: {count}",
    "carousel_keywords": "Palavras-chave de carrossel detectadas",
    
    # Image Icon
    "image_icon_headings": "Encontrados {count} títulos em formato de lista",
    "image_icon_images": "Imagens presentes: {count}",
    "image_icon_benefits": "Palavras-chave de benefícios detectadas",
    
    # Contracts
    "contracts_pdf_links": "Encontrados {count} links PDF",
    "contracts_keywords": "Palavras-chave de contrato/tarifa detectadas",
    
    # Card with icon
    "card_icon_headings": "Encontrados {count} títulos em formato de card",
    "card_icon_keywords": "Palavras-chave de card detectadas",
    "card_icon_images": "Imagens presentes: {count}",
    
    # Media with steps
    "media_steps_keywords": "Palavras-chave de passo detectadas",
    "media_steps_numbered": "Encontrados {count} itens numerados",
    "media_steps_media": "Mídia presente",
    
    # WhatsApp
    "whatsapp_links": "Encontrados {count} links do WhatsApp",
    "whatsapp_keywords": "Palavras-chave do WhatsApp detectadas",
    
    # QR Code
    "qr_images": "Encontradas {count} imagens de QR code",
    "qr_keywords": "Palavras-chave de QR code detectadas",
}

# Module titles (for display)
MODULE_TITLES = {
    "breadcrumb": "Navegação breadcrumb",
    "hero": "Banner principal",
    "richtext": "Seção de conteúdo textual",
    "image_text": "Seção de imagem com texto",
    "accordion": "Seção de FAQ",
    "carousel": "Seção de carrossel",
    "image_icon": "Seção de lista com ícones",
    "contracts": "Contratos e documentos",
    "card_icon": "Cards com ícones",
    "media_steps": "Guia passo a passo",
    "whatsapp": "Contato WhatsApp",
    "qr": "QR Code",
}

# Module text descriptions
MODULE_TEXT = {
    "breadcrumb": "Navegação breadcrumb detectada",
    "accordion": "Detectadas {count} perguntas",
    "carousel": "Detectadas {count} imagens",
    "image_icon": "Detectados {count} itens",
    "contracts": "Detectados {count} documentos",
    "card_icon": "Detectados {count} cards",
    "media_steps": "Processo com etapas sequenciais",
    "whatsapp": "Botão WhatsApp detectado",
    "qr": "QR code detectado",
}

# Agent names (for trace)
AGENT_NAMES = {
    "orchestrator": "Agente Orquestrador",
    "seo": "Agente SEO",
    "module_strategy": "Agente de Estratégia de Módulos",
    "storytelling": "Agente de Storytelling",
    "brand_safety": "Agente de Segurança de Marca",
    "recommendation": "Agente de Recomendações",
}

# Agent summaries
AGENT_SUMMARIES = {
    "orchestrator_briefing": "Analisou estrutura do briefing e coordenou fluxo de agentes",
    "orchestrator_url": "Analisou estrutura da URL e coordenou fluxo de trabalho",
    "seo_briefing": "Avaliou potencial de SEO e oportunidades de palavras-chave",
    "seo_url": "Avaliou potencial de SEO da URL e metadados",
    "module_strategy_briefing": "Recomendou composição de módulos baseada nos objetivos da página",
    "module_strategy_url": "Analisou módulos e estrutura da página",
    "storytelling_briefing": "Analisou fluxo narrativo e estrutura de storytelling",
    "storytelling_url": "Avaliou fluxo narrativo a partir do contexto da URL",
    "brand_safety": "Verificou conformidade com diretrizes da marca",
    "brand_safety_url": "Verificou conformidade com a marca",
    "recommendation": "Sintetizou insights e priorizou recomendações",
    "recommendation_url": "Gerou recomendações acionáveis",
}

# Recommendation messages
RECOMMENDATION_MESSAGES = {
    "narrative_title": "Aplicar sequência narrativa recomendada",
    "narrative_why": "O pattern detectado define uma progressão narrativa mais aderente ao objetivo da página.",
    "narrative_suggestion": "Organize a página na sequência: {sequence}",
    
    "cta_title": "Usar CTAs aderentes ao pattern detectado",
    "cta_why": "Chamadas para ação alinhadas ao storytelling reduzem fricção e tornam a conversão mais clara.",
    "cta_suggestion": "Teste CTAs como: {examples}",
    
    "brand_safety_title": "Ajustar copy para compliance e segurança de marca",
    "brand_safety_why": "O pattern inclui regras específicas de linguagem e conformidade para este contexto.",
    "brand_safety_compliance": "Siga estas diretrizes: {guidelines}",
    "brand_safety_avoid": "Evite expressões como: {avoid}",
    
    "avoid_module_title": "Evitar módulo {module} neste contexto",
    "avoid_module_suggestion": "Reavalie o uso de {module} e priorize os módulos recomendados pelo pattern.",
    
    "expand_content_title": "Expandir contexto textual da página",
    "expand_content_why": "Pouco conteúdo textual pode limitar clareza da proposta e cobertura orgânica.",
    "expand_content_suggestion": "Detalhe melhor a proposta de valor, a jornada e o CTA sem fugir da estrutura do pattern.",
    
    "validate_constraints_title": "Validar restrições do briefing na implementação",
    "validate_constraints_why": "Restrições explícitas podem afetar a ordem narrativa e a composição de módulos.",
    "validate_constraints_suggestion": "Confirme que os módulos e a copy final respeitam: {constraints}",
}

# Narrative insight messages
NARRATIVE_INSIGHT_MESSAGES = {
    "missing_step_title": "Ausência de etapa narrativa: {step_name}",
    "missing_step_description": "A página não possui módulos que suportem a etapa '{step_name}' do storytelling pattern detectado.",
    
    "compliance_risk_title": "Risco de compliance detectado",
    "compliance_risk_description": "Possível violação de diretrizes de marca ou compliance: {issue}",
    
    "weak_cta_progression_title": "Progressão de CTA inadequada",
    "weak_cta_progression_description": "A página solicita conversão antes de estabelecer confiança ou explicar condições.",
    
    "module_gap_title": "Lacuna na arquitetura de módulos",
    "module_gap_description": "Módulo obrigatório ausente: {module_name}",
    
    "narrative_break_title": "Quebra na sequência narrativa",
    "narrative_break_description": "A ordem dos módulos não segue a progressão recomendada pelo storytelling pattern.",
    
    "excessive_conversion_pressure_title": "Pressão de conversão excessiva",
    "excessive_conversion_pressure_description": "Múltiplos CTAs antes de estabelecer valor e segurança podem gerar fricção.",
    
    "poor_module_order_title": "Ordem de módulos não otimizada",
    "poor_module_order_description": "A sequência atual não segue a jornada emocional recomendada: {journey}",
    
    "missing_objection_handling_title": "Ausência de tratamento de objeções",
    "missing_objection_handling_description": "Página não possui FAQ ou seção de segurança para reduzir incertezas.",
    
    "weak_value_proposition_title": "Proposta de valor pouco clara",
    "weak_value_proposition_description": "Benefícios práticos não estão destacados de forma escaneável.",
}

# Narrative insight types
NARRATIVE_INSIGHT_TYPES = {
    "missing_step": "missing_step",
    "compliance_risk": "compliance_risk",
    "weak_cta_progression": "weak_cta_progression",
    "module_gap": "module_gap",
    "narrative_break": "narrative_break",
    "excessive_conversion_pressure": "excessive_conversion_pressure",
    "poor_module_order": "poor_module_order",
    "missing_objection_handling": "missing_objection_handling",
    "weak_value_proposition": "weak_value_proposition",
}

# Severity levels
SEVERITY_LEVELS = {
    "high": "high",
    "medium": "medium",
    "low": "low",
}

# Module plan messages
MODULE_PLAN_MESSAGES = {
    "reorder_reason": "Módulo recomendado pelo storytelling pattern detectado.",
    "add_required_reason": "Módulo obrigatório no pattern detectado para sustentar a narrativa.",
    "add_optional_reason": "Módulo opcional recomendado pelo pattern detectado.",
    "add_no_modules_reason": "Módulo obrigatório sugerido porque nenhum módulo foi detectado na página.",
}

# Page summary messages
PAGE_SUMMARY_MESSAGES = {
    "main_topic_briefing": "Tópico extraído da análise do briefing",
    "main_topic_url": "Tópico identificado da URL: {url}",
}

# Status messages
STATUS_MESSAGES = {
    "completed": "concluído",
    "in_progress": "em andamento",
    "pending": "pendente",
}

# Priority levels
PRIORITY_LEVELS = {
    "high": "alta",
    "medium": "média",
    "low": "baixa",
}

# Impact levels
IMPACT_LEVELS = {
    "high": "alto",
    "medium": "médio",
    "low": "baixo",
}

# Effort levels
EFFORT_LEVELS = {
    "high": "alto",
    "medium": "médio",
    "low": "baixo",
}

# Area names
AREA_NAMES = {
    "storytelling": "storytelling",
    "conversion": "conversão",
    "brand_safety": "brand_safety",
    "modules": "módulos",
    "seo": "seo",
    "execution": "execução",
}


def format_message(template: str, **kwargs) -> str:
    """
    Format a message template with provided arguments.
    
    Args:
        template: Message template with {placeholders}
        **kwargs: Values to replace in template
    
    Returns:
        Formatted message string
    """
    return template.format(**kwargs)


# Made with Bob