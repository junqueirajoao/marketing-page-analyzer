from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from app.services.storytelling_pattern_service import (
    build_storytelling_analysis,
    find_best_storytelling_pattern,
    get_storytelling_patterns,
)


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
        
        storytelling_pattern = self._select_storytelling_pattern(
            catalogs=catalogs,
            page_type=None,
            business_goal=business_goal,
            target_audience=target_audience,
            text_context=briefing,
        )
        storytelling_analysis = build_storytelling_analysis(
            storytelling_pattern
        )

        agent_trace = self._build_agent_trace(briefing, business_goal)
        analysis_id = self._generate_analysis_id()
        scores = self._calculate_scores(briefing, constraints)
        page_summary = self._build_page_summary(
            briefing, business_goal, target_audience
        )
        recommendations = self._generate_recommendations(
            business_goal=business_goal,
            constraints=constraints,
            pattern=storytelling_pattern,
            text_context=briefing,
        )
        module_plan = self._build_module_plan(
            catalogs=catalogs,
            pattern=storytelling_pattern,
            detected_modules=[],
        )
        copy_suggestions = self._generate_copy_suggestions(
            pattern=storytelling_pattern
        )
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
            "storytelling_analysis": storytelling_analysis,
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
        
        text_context = self._build_url_context(
            url=url,
            business_goal=business_goal,
            normalized_page=normalized_page,
        )
        storytelling_pattern = self._select_storytelling_pattern(
            catalogs=catalogs,
            page_type=page_type_hint,
            business_goal=business_goal,
            target_audience=target_audience,
            text_context=text_context,
        )
        storytelling_analysis = build_storytelling_analysis(
            storytelling_pattern
        )

        page_diagnostics = self._build_page_diagnostics(normalized_page)
        agent_trace = self._build_url_agent_trace(url)
        analysis_id = self._generate_analysis_id()
        scores = self._calculate_url_scores(url)
        page_summary = self._build_url_page_summary(
            url, business_goal, target_audience, page_type_hint
        )
        recommendations = self._generate_recommendations(
            business_goal=business_goal,
            constraints=[],
            pattern=storytelling_pattern,
            text_context=text_context,
        )
        module_plan = self._build_module_plan(
            catalogs=catalogs,
            pattern=storytelling_pattern,
            detected_modules=normalized_page.get("modules", []),
        )
        copy_suggestions = self._generate_copy_suggestions(
            pattern=storytelling_pattern
        )
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
            "page_diagnostics": page_diagnostics,
            "storytelling_analysis": storytelling_analysis,
            "detected_modules": normalized_page.get("modules", []),
        }
    
    def _generate_analysis_id(self) -> str:
        """Generate a unique analysis ID."""
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
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
        self,
        business_goal: str,
        constraints: List[str],
        pattern: Optional[Dict[str, Any]],
        text_context: str,
    ) -> List[Dict[str, Any]]:
        """Generate pattern-based recommendations."""
        recommendations: List[Dict[str, Any]] = []

        narrative_steps = []
        if pattern:
            narrative_steps = [
                str(step.get("name"))
                for step in pattern.get("narrative_steps", [])
                if isinstance(step, dict) and step.get("name")
            ]

        if narrative_steps:
            recommendations.append({
                "priority": "alta",
                "area": "storytelling",
                "title": "Aplicar sequência narrativa recomendada",
                "why": (
                    "O pattern detectado define uma progressão narrativa "
                    "mais aderente ao objetivo da página."
                ),
                "suggestion": (
                    "Organize a página na sequência: "
                    + " → ".join(narrative_steps)
                ),
                "impact": "alto",
                "effort": "médio"
            })

        cta_examples = []
        if pattern:
            cta_examples = list(pattern.get("cta_examples") or [])
        if cta_examples:
            recommendations.append({
                "priority": "alta",
                "area": "conversão",
                "title": "Usar CTAs aderentes ao pattern detectado",
                "why": (
                    "Chamadas para ação alinhadas ao storytelling reduzem "
                    "fricção e tornam a conversão mais clara."
                ),
                "suggestion": (
                    "Teste CTAs como: " + "; ".join(cta_examples[:3])
                ),
                "impact": "alto",
                "effort": "baixo"
            })

        compliance_guidelines = []
        avoid_copy = []
        if pattern:
            compliance_guidelines = list(
                pattern.get("compliance_guidelines") or []
            )
            avoid_copy = list(pattern.get("avoid_copy") or [])
        if compliance_guidelines or avoid_copy:
            safety_parts = []
            if compliance_guidelines:
                safety_parts.append(
                    "Siga estas diretrizes: "
                    + "; ".join(compliance_guidelines[:3])
                )
            if avoid_copy:
                safety_parts.append(
                    "Evite expressões como: "
                    + "; ".join(avoid_copy[:3])
                )
            recommendations.append({
                "priority": "alta",
                "area": "brand_safety",
                "title": "Ajustar copy para compliance e segurança de marca",
                "why": (
                    "O pattern inclui regras específicas de linguagem e "
                    "conformidade para este contexto."
                ),
                "suggestion": " ".join(safety_parts),
                "impact": "alto",
                "effort": "baixo"
            })

        avoid_modules_when = []
        if pattern:
            avoid_modules_when = list(pattern.get("avoid_modules_when") or [])
        for avoid_rule in avoid_modules_when:
            if not isinstance(avoid_rule, dict):
                continue
            module_name = str(avoid_rule.get("module") or "").strip()
            reason = str(avoid_rule.get("reason") or "").strip()
            if module_name and reason:
                recommendations.append({
                    "priority": "média",
                    "area": "módulos",
                    "title": f"Evitar módulo {module_name} neste contexto",
                    "why": reason,
                    "suggestion": (
                        f"Reavalie o uso de {module_name} e priorize os "
                        "módulos recomendados pelo pattern."
                    ),
                    "impact": "médio",
                    "effort": "baixo"
                })

        if len(text_context) < 200:
            recommendations.append({
                "priority": "média",
                "area": "seo",
                "title": "Expandir contexto textual da página",
                "why": (
                    "Pouco conteúdo textual pode limitar clareza da proposta "
                    "e cobertura orgânica."
                ),
                "suggestion": (
                    "Detalhe melhor a proposta de valor, a jornada e o CTA "
                    "sem fugir da estrutura do pattern."
                ),
                "impact": "médio",
                "effort": "médio"
            })

        if constraints:
            recommendations.append({
                "priority": "baixa",
                "area": "execução",
                "title": "Validar restrições do briefing na implementação",
                "why": (
                    "Restrições explícitas podem afetar a ordem narrativa e "
                    "a composição de módulos."
                ),
                "suggestion": (
                    "Confirme que os módulos e a copy final respeitam: "
                    + "; ".join(constraints[:3])
                ),
                "impact": "médio",
                "effort": "baixo"
            })

        return recommendations

    def _build_module_plan(
        self,
        catalogs: Dict[str, Any],
        pattern: Optional[Dict[str, Any]],
        detected_modules: List[Dict[str, Any]],
    ) -> Dict[str, List[Any]]:
        """Build module plan using the detected storytelling pattern."""
        detected_names = [
            str(module.get("matched_catalog_name") or "").strip()
            for module in detected_modules
            if isinstance(module, dict)
        ]
        detected_name_set = {name for name in detected_names if name}

        required_modules = []
        optional_modules = []
        recommended_order = []
        avoid_modules_when = []
        if pattern:
            required_modules = list(pattern.get("required_modules") or [])
            optional_modules = list(pattern.get("optional_modules") or [])
            recommended_order = list(
                pattern.get("recommended_module_order") or []
            )
            avoid_modules_when = list(
                pattern.get("avoid_modules_when") or []
            )

        keep = []
        for module_name in detected_names:
            if (
                module_name in recommended_order
                or module_name in required_modules
            ):
                keep.append(module_name)

        reorder = []
        for index, module_name in enumerate(recommended_order, start=1):
            if module_name in detected_name_set:
                reorder.append({
                    "module_type": module_name,
                    "suggested_position": index,
                    "reason": (
                        "Módulo recomendado pelo storytelling pattern "
                        "detectado."
                    )
                })

        add = []
        for module_name in required_modules:
            if module_name not in detected_name_set:
                add.append({
                    "module_type": module_name,
                    "reason": (
                        "Módulo obrigatório no pattern detectado para "
                        "sustentar a narrativa."
                    )
                })

        for module_name in optional_modules:
            if (
                module_name not in detected_name_set
                and module_name in recommended_order
            ):
                add.append({
                    "module_type": module_name,
                    "reason": (
                        "Módulo opcional recomendado pelo pattern detectado."
                    )
                })

        remove = []
        for avoid_rule in avoid_modules_when:
            if not isinstance(avoid_rule, dict):
                continue
            module_name = str(avoid_rule.get("module") or "").strip()
            reason = str(avoid_rule.get("reason") or "").strip()
            if module_name and module_name in detected_name_set:
                remove.append({
                    "module_type": module_name,
                    "reason": reason
                })

        if not detected_name_set:
            for module_name in required_modules:
                if not any(
                    item.get("module_type") == module_name for item in add
                ):
                    add.append({
                        "module_type": module_name,
                        "reason": (
                            "Módulo obrigatório sugerido porque nenhum módulo "
                            "foi detectado na página."
                        )
                    })

        return {
            "keep": keep,
            "remove": remove,
            "reorder": reorder,
            "add": add
        }

    def _generate_copy_suggestions(
        self, pattern: Optional[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Generate copy improvement suggestions.
        
        Returns:
            List of copy suggestion dictionaries.
        """
        suggestions = []

        headlines = []
        ctas = []
        tones = []
        if pattern:
            headlines = list(pattern.get("headline_examples") or [])
            ctas = list(pattern.get("cta_examples") or [])
            tones = list(pattern.get("tone_guidelines") or [])

        if headlines:
            suggestions.append({
                "section": "título",
                "current": "Título atual",
                "suggested": headlines[0],
                "reason": "Exemplo de headline recomendado pelo pattern"
            })

        if ctas:
            suggestions.append({
                "section": "cta",
                "current": "CTA atual",
                "suggested": ctas[0],
                "reason": "CTA alinhado ao storytelling detectado"
            })

        if tones:
            suggestions.append({
                "section": "tom",
                "current": "Tom atual",
                "suggested": ", ".join(tones[:3]),
                "reason": "Diretriz de tom definida no storytelling pattern"
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
    
    def _select_storytelling_pattern(
        self,
        catalogs: Dict[str, Any],
        page_type: Optional[str],
        business_goal: Optional[str],
        target_audience: Optional[str],
        text_context: Optional[str],
    ) -> Optional[Dict[str, Any]]:
        patterns = get_storytelling_patterns(catalogs)
        return find_best_storytelling_pattern(
            patterns=patterns,
            page_type=page_type,
            business_goal=business_goal,
            target_audience=target_audience,
            text_context=text_context,
        )

    def _build_url_context(
        self,
        url: str,
        business_goal: Optional[str],
        normalized_page: Dict[str, Any],
    ) -> str:
        main_text = str(normalized_page.get("main_text") or "")
        goal = str(business_goal or "")
        return " ".join(part for part in [url, goal, main_text] if part)
    
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