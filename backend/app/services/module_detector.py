"""
Module detector service for identifying page modules using heuristic analysis.
"""
from typing import Dict, List, Any
import re


def detect_modules(
    normalized_page: Dict[str, Any],
    modules_catalog: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Detect modules in a normalized page using heuristic analysis.
    
    Args:
        normalized_page: Normalized page data with metadata,
                        headings, links, etc.
        modules_catalog: List of module definitions from catalog
    
    Returns:
        List of detected modules with metadata
    """
    detected_modules = []
    
    # Extract page data
    headings = normalized_page.get("headings", [])
    links = normalized_page.get("links", [])
    images = normalized_page.get("images", [])
    main_text = normalized_page.get("main_text", "").lower()
    
    # Create catalog lookup by name for easy matching
    catalog_by_name = {m["name"]: m for m in modules_catalog}
    
    # Detect Hero / Main Banner
    hero_module = _detect_hero(
        headings, main_text, images, catalog_by_name
    )
    if hero_module:
        detected_modules.append(hero_module)
    
    # Detect Breadcrumb
    breadcrumb_module = _detect_breadcrumb(
        links, headings, catalog_by_name
    )
    if breadcrumb_module:
        detected_modules.append(breadcrumb_module)
    
    # Detect FAQ / Accordion
    faq_modules = _detect_faq(
        headings, main_text, catalog_by_name
    )
    detected_modules.extend(faq_modules)
    
    # Detect CTA / Call to Action
    cta_modules = _detect_cta(
        headings, links, main_text, catalog_by_name
    )
    detected_modules.extend(cta_modules)
    
    # Detect Benefits (Card with icon / Image Icon)
    benefit_modules = _detect_benefits(
        headings, main_text, images, catalog_by_name
    )
    detected_modules.extend(benefit_modules)
    
    # Detect Richtext
    richtext_modules = _detect_richtext(
        headings, main_text, catalog_by_name
    )
    detected_modules.extend(richtext_modules)
    
    # Assign positions based on detection order
    for idx, module in enumerate(detected_modules):
        module["position"] = idx
    
    return detected_modules


def _detect_hero(
    headings: List[Dict],
    main_text: str,
    images: List[Dict],
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Hero / Main Banner module."""
    if not headings:
        return None
    
    # Hero typically has H1 at the beginning
    first_heading = headings[0]
    if first_heading.get("level") != "1":
        return None
    
    h1_text = first_heading.get("text", "")
    
    # Check for hero indicators
    hero_keywords = [
        "bem-vindo", "welcome", "descubra", "discover",
        "conheca", "meet", "solucao", "solution"
    ]
    
    has_hero_keyword = any(kw in main_text for kw in hero_keywords)
    has_images = len(images) > 0
    
    confidence = 0.6
    if has_hero_keyword:
        confidence += 0.2
    if has_images:
        confidence += 0.2
    
    evidence = ["H1 found at beginning"]
    if has_hero_keyword:
        evidence.append("Hero keywords detected")
    if has_images:
        evidence.append("Images present")
    
    catalog_entry = catalog.get("Main Banner", {})
    
    return {
        "id": "detected_hero_0",
        "type": "Hero",
        "matched_catalog_id": catalog_entry.get("id", "module_09"),
        "matched_catalog_name": "Main Banner",
        "title": h1_text,
        "text": h1_text[:200],
        "position": 0,
        "confidence": round(confidence, 2),
        "evidence": evidence
    }


def _detect_breadcrumb(
    links: List[Dict],
    headings: List[Dict],
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Breadcrumb module."""
    if not links:
        return None
    
    # Look for breadcrumb indicators in first few links
    breadcrumb_keywords = [
        "home", "inicio", "para voce", "empresas",
        "produtos", "servicos"
    ]
    
    # Check first 5 links for breadcrumb pattern
    early_links = links[:5]
    breadcrumb_links = []
    
    for link in early_links:
        link_text = link.get("text", "").lower()
        if any(kw in link_text for kw in breadcrumb_keywords):
            breadcrumb_links.append(link)
    
    if len(breadcrumb_links) < 2:
        return None
    
    confidence = 0.7 if len(breadcrumb_links) >= 3 else 0.5
    
    catalog_entry = catalog.get("Breadcrumb Header", {})
    
    return {
        "id": "detected_breadcrumb_0",
        "type": "Navigation",
        "matched_catalog_id": catalog_entry.get("id", "module_01"),
        "matched_catalog_name": "Breadcrumb Header",
        "title": "Breadcrumb navigation",
        "text": " > ".join(
            [link.get("text", "") for link in breadcrumb_links[:3]]
        ),
        "position": 0,
        "confidence": round(confidence, 2),
        "evidence": [
            f"Found {len(breadcrumb_links)} breadcrumb-like links",
            "Links contain navigation keywords"
        ]
    }


def _detect_faq(
    headings: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Detect FAQ / Accordion modules."""
    faq_modules = []
    
    # Look for FAQ indicators
    faq_keywords = [
        "perguntas frequentes", "faq", "duvidas",
        "como funciona", "o que e", "posso", "quando"
    ]
    
    has_faq_keyword = any(kw in main_text for kw in faq_keywords)
    
    # Count question-like headings
    question_headings = []
    for heading in headings:
        text = heading.get("text", "").lower()
        question_starters = [
            "como", "o que", "qual", "quando", "posso", "por que"
        ]
        if any(text.startswith(q) for q in question_starters):
            question_headings.append(heading)
    
    if has_faq_keyword or len(question_headings) >= 3:
        confidence = 0.8 if len(question_headings) >= 3 else 0.6
        
        catalog_entry = catalog.get("Accordion", {})
        
        faq_modules.append({
            "id": "detected_faq_0",
            "type": "Expandable Content",
            "matched_catalog_id": catalog_entry.get("id", "module_04"),
            "matched_catalog_name": "Accordion",
            "title": "FAQ section",
            "text": (
                f"Detected {len(question_headings)} "
                "question-like headings"
            ),
            "position": 0,
            "confidence": round(confidence, 2),
            "evidence": [
                f"Found {len(question_headings)} question headings",
                (
                    "FAQ keywords present" if has_faq_keyword
                    else "Question patterns detected"
                )
            ]
        })
    
    return faq_modules


def _detect_cta(
    headings: List[Dict],
    links: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Detect CTA / Call to Action modules."""
    cta_modules = []
    
    # CTA action verbs
    cta_verbs = [
        "contrate", "simule", "abra", "fale", "conheca",
        "baixe", "solicite", "comece", "experimente",
        "cadastre", "assine", "garanta"
    ]
    
    # Check links for CTA patterns
    cta_links = []
    for link in links:
        link_text = link.get("text", "").lower()
        if any(verb in link_text for verb in cta_verbs):
            cta_links.append(link)
    
    # Check main text for CTA keywords
    cta_count = sum(1 for verb in cta_verbs if verb in main_text)
    
    if cta_links or cta_count >= 2:
        confidence = 0.7 if cta_links else 0.5
        
        catalog_entry = catalog.get("Call to Action", {})
        
        if cta_links:
            cta_text = cta_links[0].get("text", "CTA detected")
        else:
            cta_text = "CTA section"
        
        cta_modules.append({
            "id": "detected_cta_0",
            "type": "CTA",
            "matched_catalog_id": catalog_entry.get("id", "module_19"),
            "matched_catalog_name": "Call to Action",
            "title": cta_text,
            "text": cta_text[:200],
            "position": 0,
            "confidence": round(confidence, 2),
            "evidence": [
                (
                    f"Found {len(cta_links)} CTA links" if cta_links
                    else f"Found {cta_count} CTA verbs"
                ),
                "Action verbs detected"
            ]
        })
    
    return cta_modules


def _detect_benefits(
    headings: List[Dict],
    main_text: str,
    images: List[Dict],
    catalog: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Detect Benefits modules (Card with icon / Image Icon)."""
    benefit_modules = []
    
    # Benefit keywords
    benefit_keywords = [
        "beneficio", "vantagem", "diferencial",
        "recurso", "funcionalidade", "caracteristica"
    ]
    
    has_benefit_keyword = any(kw in main_text for kw in benefit_keywords)
    
    # Look for list-like patterns in headings (H3, H4)
    list_headings = [h for h in headings if h.get("level") in ["3", "4"]]
    
    # If we have multiple similar-level headings and benefit keywords
    if len(list_headings) >= 3 and (has_benefit_keyword or len(images) >= 3):
        confidence = 0.7 if has_benefit_keyword else 0.5
        
        # Prefer "Card with icon" if we have images
        if len(images) >= 3:
            catalog_entry = catalog.get("Card with icon", {})
            module_name = "Card with icon"
            module_id = "module_08"
        else:
            catalog_entry = catalog.get("Image Icon", {})
            module_name = "Image Icon"
            module_id = "module_06"
        
        benefit_modules.append({
            "id": "detected_benefits_0",
            "type": "Icon Feature List",
            "matched_catalog_id": catalog_entry.get("id", module_id),
            "matched_catalog_name": module_name,
            "title": "Benefits section",
            "text": f"Detected {len(list_headings)} benefit items",
            "position": 0,
            "confidence": round(confidence, 2),
            "evidence": [
                f"Found {len(list_headings)} list-style headings",
                (
                    f"Images present: {len(images)}" if images
                    else "Benefit keywords detected"
                )
            ]
        })
    
    return benefit_modules


def _detect_richtext(
    headings: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Detect Richtext modules."""
    richtext_modules = []
    
    # Richtext is common, so we detect it if there's substantial text
    # and it doesn't match other specific patterns
    
    if len(main_text) > 500:
        # Count paragraphs (approximate by sentence count)
        sentence_count = len(re.findall(r'[.!?]+', main_text))
        
        if sentence_count >= 5:
            confidence = 0.6
            
            catalog_entry = catalog.get("Richtext", {})
            
            richtext_modules.append({
                "id": "detected_richtext_0",
                "type": "Text Content",
                "matched_catalog_id": catalog_entry.get("id", "module_02"),
                "matched_catalog_name": "Richtext",
                "title": "Text content section",
                "text": main_text[:200],
                "position": 0,
                "confidence": round(confidence, 2),
                "evidence": [
                    f"Substantial text content ({len(main_text)} chars)",
                    (
                        f"Multiple paragraphs detected "
                        f"({sentence_count} sentences)"
                    )
                ]
            })
    
    return richtext_modules


# Made with Bob