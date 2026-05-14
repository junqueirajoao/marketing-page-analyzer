from typing import Dict, Any, List, Optional
from datetime import datetime


class LocalAgentFallback:
    """
    Local fallback implementation simulating IBM Consulting Advantage agents.
    This class provides mock responses that follow the expected agent payload
    structure and response contract.
    """
    
    def __init__(self):
        """Initialize the local agent fallback."""
        self.agent_names = [
            "Orchestrator Agent",
            "SEO Agent",
            "Module Strategy Agent",
            "Storytelling Agent",
            "Brand Safety Agent",
            "Recommendation Agent"
        ]
    
    def analyze_briefing(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a briefing using simulated agent logic.
        
        Args:
            payload: Dictionary containing:
                - input_type: Type of input (e.g., "briefing")
                - briefing: The briefing text
                - business_goal: Optional business goal
                - target_audience: Optional target audience
                - constraints: List of constraints
                - catalogs: Dictionary with modules_catalog,
                           storytelling_patterns, brand_rules
        
        Returns:
            Dictionary with analysis results including:
                - analysis_id
                - score
                - page_summary
                - recommendations
                - module_plan
                - copy_suggestions
                - catalog_context
                - agent_trace
        """
        # Extract payload data
        briefing = payload.get("briefing", "")
        business_goal = payload.get("business_goal", "nao_informado")
        target_audience = payload.get("target_audience", "nao_informado")
        constraints = payload.get("constraints", [])
        catalogs = payload.get("catalogs", {})
        
        # Simulate agent trace
        agent_trace = self._build_agent_trace(briefing, business_goal)
        
        # Build analysis response
        analysis_id = self._generate_analysis_id()
        
        # Simulate scoring from different agents
        scores = self._calculate_scores(briefing, constraints)
        
        # Build page summary
        page_summary = self._build_page_summary(
            briefing, business_goal, target_audience
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            briefing, business_goal, constraints
        )
        
        # Build module plan
        module_plan = self._build_module_plan(briefing, catalogs)
        
        # Generate copy suggestions
        copy_suggestions = self._generate_copy_suggestions(briefing)
        
        # Build catalog context
        catalog_context = self._build_catalog_context(catalogs)
        
        return {
            "analysis_id": analysis_id,
            "score": scores,
            "page_summary": page_summary,
            "recommendations": recommendations,
            "module_plan": module_plan,
            "copy_suggestions": copy_suggestions,
            "catalog_context": catalog_context,
            "agent_trace": agent_trace
        }
    
    def analyze_url(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a URL using simulated agent logic.
        
        Args:
            payload: Dictionary containing:
                - input_type: Type of input (e.g., "url")
                - url: The URL to analyze
                - business_goal: Optional business goal
                - target_audience: Optional target audience
                - page_type_hint: Optional page type hint
                - catalogs: Dictionary with modules_catalog,
                           storytelling_patterns, brand_rules
                - normalized_page: Normalized page data from scraper
        
        Returns:
            Dictionary with analysis results including:
                - analysis_id
                - score
                - page_summary
                - recommendations
                - module_plan
                - copy_suggestions
                - catalog_context
                - agent_trace
                - page_diagnostics
        """
        # Extract payload data
        url = payload.get("url", "")
        business_goal = payload.get("business_goal", "nao_informado")
        target_audience = payload.get("target_audience", "nao_informado")
        page_type_hint = payload.get("page_type_hint")
        catalogs = payload.get("catalogs", {})
        normalized_page = payload.get("normalized_page", {})
        
        # Build page diagnostics from normalized page
        page_diagnostics = self._build_page_diagnostics(normalized_page)
        
        # Simulate agent trace for URL analysis
        agent_trace = self._build_url_agent_trace(url)
        
        # Build analysis response
        analysis_id = self._generate_analysis_id()
        
        # Simulate scoring (slightly different from briefing)
        scores = self._calculate_url_scores(url)
        
        # Build page summary for URL
        page_summary = self._build_url_page_summary(
            url, business_goal, target_audience, page_type_hint
        )
        
        # Generate recommendations for URL
        recommendations = self._generate_url_recommendations(
            url, business_goal
        )
        
        # Build module plan
        module_plan = self._build_module_plan(url, catalogs)
        
        # Generate copy suggestions
        copy_suggestions = self._generate_url_copy_suggestions(url)
        
        # Build catalog context
        catalog_context = self._build_catalog_context(catalogs)
        
        return {
            "analysis_id": analysis_id,
            "score": scores,
            "page_summary": page_summary,
            "recommendations": recommendations,
            "module_plan": module_plan,
            "copy_suggestions": copy_suggestions,
            "catalog_context": catalog_context,
            "agent_trace": agent_trace,
            "page_diagnostics": page_diagnostics
        }
    
    def _generate_analysis_id(self) -> str:
        """Generate a unique analysis ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        return f"analysis_{timestamp}"
    
    def _build_agent_trace(
        self, briefing: str, business_goal: str
    ) -> List[Dict[str, Any]]:
        """
        Build the agent trace showing simulated agent execution.
        
        Returns:
            List of agent execution steps with name, status, and summary.
        """
        trace = []
        
        # Orchestrator Agent
        trace.append({
            "agent": "Agente Orquestrador",
            "status": "concluído",
            "summary": (
                "Analisou estrutura do briefing e coordenou fluxo de agentes"
            )
        })
        
        # SEO Agent
        trace.append({
            "agent": "Agente SEO",
            "status": "concluído",
            "summary": (
                "Avaliou potencial de SEO e "
                "oportunidades de palavras-chave"
            )
        })
        
        # Module Strategy Agent
        trace.append({
            "agent": "Agente de Estratégia de Módulos",
            "status": "concluído",
            "summary": (
                "Recomendou composição de módulos "
                "baseada nos objetivos da página"
            )
        })
        
        # Storytelling Agent
        trace.append({
            "agent": "Agente de Storytelling",
            "status": "concluído",
            "summary": "Analisou fluxo narrativo e estrutura de storytelling"
        })
        
        # Brand Safety Agent
        trace.append({
            "agent": "Agente de Segurança de Marca",
            "status": "concluído",
            "summary": "Verificou conformidade com diretrizes da marca"
        })
        
        # Recommendation Agent
        trace.append({
            "agent": "Agente de Recomendações",
            "status": "concluído",
            "summary": "Sintetizou insights e priorizou recomendações"
        })
        
        return trace
    
    def _calculate_scores(
        self, briefing: str, constraints: List[str]
    ) -> Dict[str, int]:
        """
        Calculate simulated scores for different aspects.
        
        Returns:
            Dictionary with overall, seo, storytelling, modules,
            brand_safety scores.
        """
        # Simple heuristic: longer briefings get slightly better scores
        base_score = 70
        length_bonus = min(len(briefing) // 100, 15)
        constraint_penalty = len(constraints) * 2
        
        seo_score = max(
            60, min(95, base_score + length_bonus - constraint_penalty)
        )
        storytelling_score = max(65, min(95, base_score + length_bonus + 5))
        modules_score = max(60, min(95, base_score + length_bonus))
        brand_safety_score = max(75, min(95, base_score + 15))
        
        overall_score = (
            seo_score + storytelling_score + modules_score + brand_safety_score
        ) // 4
        
        return {
            "overall": overall_score,
            "seo": seo_score,
            "storytelling": storytelling_score,
            "modules": modules_score,
            "brand_safety": brand_safety_score
        }
    
    def _build_page_summary(
        self, briefing: str, business_goal: str, target_audience: str
    ) -> Dict[str, str]:
        """
        Build page summary based on briefing analysis.
        
        Returns:
            Dictionary with detected_type, primary_goal, main_topic.
        """
        # Simple heuristic to detect page type
        briefing_lower = briefing.lower()
        
        if "produto" in briefing_lower or "product" in briefing_lower:
            detected_type = "produto"
        elif "servico" in briefing_lower or "service" in briefing_lower:
            detected_type = "servico"
        elif "evento" in briefing_lower or "event" in briefing_lower:
            detected_type = "evento"
        else:
            detected_type = "institucional"
        
        return {
            "detected_type": detected_type,
            "primary_goal": business_goal,
            "main_topic": "Tópico extraído da análise do briefing"
        }
    
    def _generate_recommendations(
        self, briefing: str, business_goal: str, constraints: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations based on briefing analysis.
        
        Returns:
            List of recommendation dictionaries.
        """
        recommendations = []
        
        # Storytelling recommendation
        recommendations.append({
            "priority": "alta",
            "area": "storytelling",
            "title": "Organizar estrutura narrativa da página",
            "why": (
                "O briefing precisa de um fluxo "
                "problema-solução-ação mais claro "
                "para guiar os usuários efetivamente."
            ),
            "suggestion": (
                "Estruture a página com: declaração do problema, "
                "visão geral da solução, principais benefícios, "
                "prova social e CTA claro."
            ),
            "impact": "alto",
            "effort": "médio"
        })
        
        # SEO recommendation
        if len(briefing) < 200:
            recommendations.append({
                "priority": "média",
                "area": "seo",
                "title": "Expandir conteúdo para melhor cobertura de SEO",
                "why": (
                    "Conteúdo breve pode limitar oportunidades "
                    "de palavras-chave e visibilidade em buscas."
                ),
                "suggestion": (
                    "Adicione seções detalhadas cobrindo "
                    "perguntas dos usuários, casos de uso e benefícios."
                ),
                "impact": "médio",
                "effort": "alto"
            })
        
        # Module recommendation
        recommendations.append({
            "priority": "média",
            "area": "módulos",
            "title": "Adicionar módulo de FAQ para reduzir objeções",
            "why": (
                "Responder perguntas comuns constrói confiança e reduz "
                "fricção."
            ),
            "suggestion": (
                "Inclua módulo de FAQ com 5-7 perguntas cobrindo preços, "
                "implementação e suporte."
            ),
            "impact": "médio",
            "effort": "baixo"
        })
        
        return recommendations
    
    def _build_module_plan(
        self, briefing: str, catalogs: Dict[str, Any]
    ) -> Dict[str, List[Any]]:
        """
        Build module plan with keep, remove, reorder, add suggestions.
        
        Returns:
            Dictionary with keep, remove, reorder, add lists.
        """
        modules_catalog = catalogs.get("modules_catalog", [])
        
        # Suggest adding FAQ and testimonials for most pages
        add_suggestions = []
        
        # Find FAQ module
        for module in modules_catalog:
            if module.get("name") == "FAQ":
                add_suggestions.append({
                    "module_type": "FAQ",
                    "reason": "Ajuda a reduzir objeções antes da conversão."
                })
                break
        
        # Find testimonials module
        for module in modules_catalog:
            if module.get("name") == "Testimonials":
                add_suggestions.append({
                    "module_type": "Depoimentos",
                    "reason": "Prova social aumenta confiança e credibilidade."
                })
                break
        
        return {
            "keep": [],
            "remove": [],
            "reorder": [],
            "add": add_suggestions
        }
    
    def _generate_copy_suggestions(
        self, briefing: str
    ) -> List[Dict[str, str]]:
        """
        Generate copy improvement suggestions.
        
        Returns:
            List of copy suggestion dictionaries.
        """
        suggestions = []
        
        # Generic copy suggestions
        suggestions.append({
            "section": "título",
            "current": "Título genérico",
            "suggested": (
                "Título focado em benefícios que aborda "
                "o ponto de dor do usuário"
            ),
            "reason": "Proposta de valor clara melhora o engajamento"
        })
        
        suggestions.append({
            "section": "cta",
            "current": "Clique aqui",
            "suggested": "Comece seu teste grátis hoje",
            "reason": "CTAs orientados a ação com valor aumentam conversões"
        })
        
        return suggestions
    
    def _build_catalog_context(
        self, catalogs: Dict[str, Any]
    ) -> Dict[str, int]:
        """
        Build catalog context showing available resources.
        
        Returns:
            Dictionary with counts of available catalog items.
        """
        return {
            "modules_available_count": len(
                catalogs.get("modules_catalog", [])
            ),
            "storytelling_patterns_count": len(
                catalogs.get("storytelling_patterns", [])
            ),
            "brand_rules_count": len(
                catalogs.get("brand_rules", [])
            )
        }
    
    def _build_url_agent_trace(self, url: str) -> List[Dict[str, Any]]:
        """
        Build agent trace for URL analysis.
        
        Returns:
            List of agent execution steps.
        """
        trace = []
        
        # Orchestrator Agent
        trace.append({
            "agent": "Agente Orquestrador",
            "status": "concluído",
            "summary": (
                "Analisou estrutura da URL e "
                "coordenou fluxo de trabalho"
            )
        })
        
        # SEO Agent
        trace.append({
            "agent": "Agente SEO",
            "status": "concluído",
            "summary": "Avaliou potencial de SEO da URL e metadados"
        })
        
        # Module Strategy Agent
        trace.append({
            "agent": "Agente de Estratégia de Módulos",
            "status": "concluído",
            "summary": "Analisou módulos e estrutura da página"
        })
        
        # Storytelling Agent
        trace.append({
            "agent": "Agente de Storytelling",
            "status": "concluído",
            "summary": "Avaliou fluxo narrativo a partir do contexto da URL"
        })
        
        # Brand Safety Agent
        trace.append({
            "agent": "Agente de Segurança de Marca",
            "status": "concluído",
            "summary": "Verificou conformidade com a marca"
        })
        
        # Recommendation Agent
        trace.append({
            "agent": "Agente de Recomendações",
            "status": "concluído",
            "summary": "Gerou recomendações acionáveis"
        })
        
        return trace
    
    def _calculate_url_scores(self, url: str) -> Dict[str, int]:
        """
        Calculate scores for URL analysis.
        
        Returns:
            Dictionary with scores.
        """
        # Simple heuristic based on URL characteristics
        base_score = 75
        
        # URLs with https get bonus
        https_bonus = 5 if url.startswith("https://") else 0
        
        seo_score = max(65, min(95, base_score + https_bonus))
        storytelling_score = max(70, min(95, base_score))
        modules_score = max(65, min(95, base_score))
        brand_safety_score = max(80, min(95, base_score + 10))
        
        overall_score = (
            seo_score + storytelling_score + modules_score + brand_safety_score
        ) // 4
        
        return {
            "overall": overall_score,
            "seo": seo_score,
            "storytelling": storytelling_score,
            "modules": modules_score,
            "brand_safety": brand_safety_score
        }
    
    def _build_url_page_summary(
        self,
        url: str,
        business_goal: str,
        target_audience: str,
        page_type_hint: Optional[str]
    ) -> Dict[str, str]:
        """
        Build page summary for URL analysis.
        
        Returns:
            Dictionary with page summary.
        """
        # Use page_type_hint if provided, otherwise detect from URL
        if page_type_hint:
            detected_type = page_type_hint
        else:
            url_lower = url.lower()
            if "product" in url_lower or "produto" in url_lower:
                detected_type = "produto"
            elif "service" in url_lower or "servico" in url_lower:
                detected_type = "servico"
            elif "event" in url_lower or "evento" in url_lower:
                detected_type = "evento"
            else:
                detected_type = "desconhecido"
        
        # Extract topic from URL
        main_topic = f"Tópico identificado da URL: {url}"
        
        return {
            "detected_type": detected_type,
            "primary_goal": business_goal,
            "main_topic": main_topic
        }
    
    def _generate_url_recommendations(
        self, url: str, business_goal: str
    ) -> List[Dict[str, Any]]:
        """
        Generate recommendations for URL analysis.
        
        Returns:
            List of recommendations.
        """
        recommendations = []
        
        # SEO recommendation
        recommendations.append({
            "priority": "alta",
            "area": "seo",
            "title": "Otimizar metadados e estrutura da página",
            "why": (
                "Metadados bem estruturados melhoram a visibilidade em buscas "
                "e taxas de cliques."
            ),
            "suggestion": (
                "Adicione tags de título descritivas, meta descrições "
                "e marcação de dados estruturados."
            ),
            "impact": "alto",
            "effort": "médio"
        })
        
        # Content recommendation
        recommendations.append({
            "priority": "média",
            "area": "storytelling",
            "title": "Melhorar fluxo narrativo do conteúdo",
            "why": "Storytelling claro guia usuários em direção à conversão.",
            "suggestion": (
                "Estruture o conteúdo com fluxo problema-solução-ação "
                "e propostas de valor claras."
            ),
            "impact": "alto",
            "effort": "médio"
        })
        
        # Module recommendation
        recommendations.append({
            "priority": "média",
            "area": "módulos",
            "title": "Adicionar elementos de prova social",
            "why": "Depoimentos e estudos de caso constroem credibilidade.",
            "suggestion": (
                "Inclua depoimentos de clientes, estudos de caso "
                "ou selos de confiança."
            ),
            "impact": "médio",
            "effort": "baixo"
        })
        
        return recommendations
    
    def _generate_url_copy_suggestions(
        self, url: str
    ) -> List[Dict[str, str]]:
        """
        Generate copy suggestions for URL analysis.
        
        Returns:
            List of copy suggestions.
        """
        suggestions = []
        
        suggestions.append({
            "section": "título",
            "current": "Título genérico da página",
            "suggested": (
                "Título claro focado em benefícios "
                "que atende necessidades do usuário"
            ),
            "reason": (
                "Títulos fortes capturam atenção "
                "e estabelecem expectativas"
            )
        })
        
        suggestions.append({
            "section": "subtítulo",
            "current": "Descrição básica",
            "suggested": (
                "Subtítulo convincente explicando "
                "a proposta de valor principal"
            ),
            "reason": (
                "Subtítulos fornecem contexto "
                "e reforçam a mensagem principal"
            )
        })
        
        suggestions.append({
            "section": "cta",
            "current": "Saiba mais",
            "suggested": "Comece com seu teste grátis",
            "reason": (
                "CTAs específicos com valor claro "
                "geram conversões mais altas"
            )
        })
        
        return suggestions
    
    def _build_page_diagnostics(
        self, normalized_page: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build page diagnostics from normalized page data.
        
        Args:
            normalized_page: Normalized page data containing metadata,
                           headings, links, images, etc.
        
        Returns:
            Dictionary with page diagnostics including:
                - has_title: Whether page has a title
                - has_meta_description: Whether page has meta description
                - headings_count: Number of headings
                - links_count: Number of links
                - images_count: Number of images
                - has_error: Whether there was an error fetching/parsing
                - modules_detected_count: Number of modules detected
        """
        metadata = normalized_page.get("metadata", {})
        headings = normalized_page.get("headings", [])
        links = normalized_page.get("links", [])
        images = normalized_page.get("images", [])
        modules = normalized_page.get("modules", [])
        error = normalized_page.get("error")
        
        return {
            "has_title": bool(metadata.get("title", "").strip()),
            "has_meta_description": bool(
                metadata.get("meta_description", "").strip()
            ),
            "headings_count": len(headings),
            "links_count": len(links),
            "images_count": len(images),
            "has_error": error is not None,
            "modules_detected_count": len(modules)
        }


# Made with Bob