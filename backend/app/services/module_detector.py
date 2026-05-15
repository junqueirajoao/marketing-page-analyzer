"""
Module detector service for identifying page modules using heuristic analysis.
Maps detected blocks to official catalog modules.
"""
from typing import Dict, List, Any
import re

from app.utils.analysis_messages import (
    MODULE_EVIDENCE,
    MODULE_TITLES,
    MODULE_TEXT,
    format_message
)


def detect_modules(
    normalized_page: Dict[str, Any],
    modules_catalog: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Detect modules in a normalized page using catalog-based heuristics.
    
    Args:
        normalized_page: Normalized page data with metadata,
                        headings, links, etc.
        modules_catalog: List of module definitions from catalog
    
    Returns:
        List of detected modules matching catalog structure
    """
    detected_modules = []
    
    # Extract page data
    headings = normalized_page.get("headings", [])
    links = normalized_page.get("links", [])
    images = normalized_page.get("images", [])
    main_text = normalized_page.get("main_text", "").lower()
    
    # Create catalog lookup by name for easy matching
    catalog_by_name = {m["name"]: m for m in modules_catalog}
    
    # Detect modules using catalog-based matching
    # Each detector returns a match with the catalog entry
    
    # 1. Detect Breadcrumb Header (module_01)
    breadcrumb = _detect_breadcrumb(links, headings, catalog_by_name)
    if breadcrumb:
        detected_modules.append(breadcrumb)
    
    # 2. Detect Main Banner / Hero (module_09)
    hero = _detect_hero(headings, main_text, images, links, catalog_by_name)
    if hero:
        detected_modules.append(hero)
    
    # 3. Detect Richtext (module_02)
    richtext = _detect_richtext(headings, main_text, catalog_by_name)
    if richtext:
        detected_modules.append(richtext)
    
    # 4. Detect Image with text (module_03)
    image_text = _detect_image_with_text(
        headings, images, main_text, catalog_by_name
    )
    if image_text:
        detected_modules.append(image_text)
    
    # 5. Detect Accordion / FAQ (module_04)
    accordion = _detect_accordion(headings, main_text, catalog_by_name)
    if accordion:
        detected_modules.append(accordion)
    
    # 6. Detect Carrossel (module_05)
    carousel = _detect_carousel(images, links, main_text, catalog_by_name)
    if carousel:
        detected_modules.append(carousel)
    
    # 7. Detect Image Icon (module_06)
    image_icon = _detect_image_icon(
        headings, images, main_text, catalog_by_name
    )
    if image_icon:
        detected_modules.append(image_icon)
    
    # 8. Detect Contract and tariffs (module_07)
    contracts = _detect_contracts(links, main_text, catalog_by_name)
    if contracts:
        detected_modules.append(contracts)
    
    # 9. Detect Card with icon (module_08)
    card_icon = _detect_card_with_icon(
        headings, images, main_text, catalog_by_name
    )
    if card_icon:
        detected_modules.append(card_icon)
    
    # 10. Detect Media with steps (module_10)
    media_steps = _detect_media_with_steps(
        headings, main_text, images, catalog_by_name
    )
    if media_steps:
        detected_modules.append(media_steps)
    
    # 11. Detect WhatsApp button (module_11)
    whatsapp = _detect_whatsapp(links, main_text, catalog_by_name)
    if whatsapp:
        detected_modules.append(whatsapp)
    
    # 12. Detect QR Code modules (module_13, module_14)
    qr_codes = _detect_qr_codes(images, main_text, catalog_by_name)
    detected_modules.extend(qr_codes)
    
    # Assign positions based on detection order (starting from 1)
    for idx, module in enumerate(detected_modules, start=1):
        module["position"] = idx
    
    return detected_modules


def _create_detected_module(
    module_id: str,
    catalog_entry: Dict[str, Any],
    title: str,
    text: str,
    confidence: float,
    evidence: List[str]
) -> Dict[str, Any]:
    """Helper to create a standardized detected module."""
    return {
        "id": module_id,
        "type": catalog_entry.get("generic_type", "Unknown"),
        "matched_catalog_id": catalog_entry.get("id", ""),
        "matched_catalog_name": catalog_entry.get("name", ""),
        "display_name": catalog_entry.get("display_name", ""),
        "title": title,
        "text": text[:200] if text else "",
        "position": 0,  # Will be set later
        "confidence": round(confidence, 2),
        "evidence": evidence
    }


def _detect_breadcrumb(
    links: List[Dict],
    headings: List[Dict],
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Breadcrumb Header module (module_01)."""
    if not links:
        return None
    
    catalog_entry = catalog.get("Breadcrumb Header", {})
    
    # Look for breadcrumb indicators in first few links
    breadcrumb_keywords = [
        "home", "inicio", "início", "para voce", "para você",
        "empresas", "produtos", "servicos", "serviços"
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
    
    evidence = [
        format_message(
            MODULE_EVIDENCE["breadcrumb_links_found"],
            count=len(breadcrumb_links)
        ),
        MODULE_EVIDENCE["breadcrumb_keywords"]
    ]
    
    breadcrumb_text = " > ".join(
        [link.get("text", "") for link in breadcrumb_links[:3]]
    )
    
    return _create_detected_module(
        module_id="detected_breadcrumb_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["breadcrumb"],
        text=breadcrumb_text,
        confidence=confidence,
        evidence=evidence
    )


def _detect_hero(
    headings: List[Dict],
    main_text: str,
    images: List[Dict],
    links: List[Dict],
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Main Banner / Hero module (module_09)."""
    if not headings:
        return None
    
    catalog_entry = catalog.get("Main Banner", {})
    
    # Hero typically has H1 at the beginning
    first_heading = headings[0]
    if first_heading.get("level") != "1":
        return None
    
    h1_text = first_heading.get("text", "")
    
    # Check for hero indicators from catalog detection_hints
    hero_keywords = [
        "bem-vindo", "welcome", "descubra", "discover",
        "conheca", "conheça", "meet", "solucao", "solução", "solution"
    ]
    
    has_hero_keyword = any(kw in main_text for kw in hero_keywords)
    has_images = len(images) > 0
    
    # Check for CTA (common in hero)
    cta_verbs = [
        "contrate", "simule", "abra", "fale", "conheca", "conheça",
        "baixe", "solicite", "comece", "experimente"
    ]
    has_cta = any(verb in main_text for verb in cta_verbs)
    
    confidence = 0.6
    if has_hero_keyword:
        confidence += 0.15
    if has_images:
        confidence += 0.15
    if has_cta:
        confidence += 0.1
    
    evidence = [MODULE_EVIDENCE["hero_h1_found"]]
    if has_hero_keyword:
        evidence.append(MODULE_EVIDENCE["hero_keywords"])
    if has_images:
        evidence.append(MODULE_EVIDENCE["hero_images"])
    if has_cta:
        evidence.append(MODULE_EVIDENCE["hero_cta"])
    
    return _create_detected_module(
        module_id="detected_hero_0",
        catalog_entry=catalog_entry,
        title=h1_text,
        text=h1_text,
        confidence=confidence,
        evidence=evidence
    )


def _detect_richtext(
    headings: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Richtext module (module_02)."""
    catalog_entry = catalog.get("Richtext", {})
    
    # Richtext is common, detect if there's substantial text
    if len(main_text) < 500:
        return None
    
    # Count paragraphs (approximate by sentence count)
    sentence_count = len(re.findall(r'[.!?]+', main_text))
    
    if sentence_count < 5:
        return None
    
    confidence = 0.6
    
    evidence = [
        format_message(
            MODULE_EVIDENCE["richtext_content"],
            chars=len(main_text)
        ),
        format_message(
            MODULE_EVIDENCE["richtext_paragraphs"],
            count=sentence_count
        )
    ]
    
    return _create_detected_module(
        module_id="detected_richtext_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["richtext"],
        text=main_text[:200],
        confidence=confidence,
        evidence=evidence
    )


def _detect_image_with_text(
    headings: List[Dict],
    images: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Image with text module (module_03)."""
    catalog_entry = catalog.get("Image with text", {})
    
    # Needs both images and substantial text
    if len(images) < 1 or len(main_text) < 200:
        return None
    
    # Check for benefit/feature keywords
    benefit_keywords = [
        "beneficio", "benefício", "vantagem", "diferencial",
        "recurso", "funcionalidade"
    ]
    
    has_benefit = any(kw in main_text for kw in benefit_keywords)
    
    if not has_benefit:
        return None
    
    confidence = 0.65
    
    evidence = [
        format_message(
            MODULE_EVIDENCE["image_text_images"],
            count=len(images)
        ),
        MODULE_EVIDENCE["image_text_benefits"],
        MODULE_EVIDENCE["image_text_combination"]
    ]
    
    return _create_detected_module(
        module_id="detected_image_text_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["image_text"],
        text=main_text[:200],
        confidence=confidence,
        evidence=evidence
    )


def _detect_accordion(
    headings: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Accordion / FAQ module (module_04)."""
    catalog_entry = catalog.get("Accordion", {})
    
    # Look for FAQ indicators from catalog
    faq_keywords = [
        "perguntas frequentes", "faq", "duvidas", "dúvidas",
        "como funciona", "o que e", "o que é", "posso", "quando"
    ]
    
    has_faq_keyword = any(kw in main_text for kw in faq_keywords)
    
    # Count question-like headings
    question_headings = []
    for heading in headings:
        text = heading.get("text", "").lower()
        question_starters = [
            "como", "o que", "qual", "quando", "posso", "por que", "onde"
        ]
        if any(text.startswith(q) for q in question_starters):
            question_headings.append(heading)
    
    if not has_faq_keyword and len(question_headings) < 3:
        return None
    
    confidence = 0.8 if len(question_headings) >= 3 else 0.6
    
    evidence = [
        format_message(
            MODULE_EVIDENCE["accordion_questions"],
            count=len(question_headings)
        )
    ]
    if has_faq_keyword:
        evidence.append(MODULE_EVIDENCE["accordion_faq_keywords"])
    else:
        evidence.append(MODULE_EVIDENCE["accordion_question_patterns"])
    
    return _create_detected_module(
        module_id="detected_accordion_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["accordion"],
        text=format_message(
            MODULE_TEXT["accordion"],
            count=len(question_headings)
        ),
        confidence=confidence,
        evidence=evidence
    )


def _detect_carousel(
    images: List[Dict],
    links: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Carrossel module (module_05)."""
    catalog_entry = catalog.get("Carrossel", {})
    
    # Carousel indicators
    carousel_keywords = [
        "slider", "carrossel", "carousel", "anterior", "próximo",
        "proximo", "swipe"
    ]
    
    has_carousel_keyword = any(kw in main_text for kw in carousel_keywords)
    
    # Multiple images suggest carousel possibility
    if len(images) < 3 and not has_carousel_keyword:
        return None
    
    confidence = 0.7 if has_carousel_keyword else 0.5
    
    evidence = [
        format_message(
            MODULE_EVIDENCE["carousel_images"],
            count=len(images)
        )
    ]
    if has_carousel_keyword:
        evidence.append(MODULE_EVIDENCE["carousel_keywords"])
    
    return _create_detected_module(
        module_id="detected_carousel_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["carousel"],
        text=format_message(MODULE_TEXT["carousel"], count=len(images)),
        confidence=confidence,
        evidence=evidence
    )


def _detect_image_icon(
    headings: List[Dict],
    images: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Image Icon module (module_06)."""
    catalog_entry = catalog.get("Image Icon", {})
    
    # Look for icon-like patterns
    # Multiple small headings + images suggest icon list
    list_headings = [h for h in headings if h.get("level") in ["3", "4"]]
    
    if len(list_headings) < 3 or len(images) < 3:
        return None
    
    # Benefit keywords
    benefit_keywords = [
        "beneficio", "benefício", "vantagem", "diferencial"
    ]
    
    has_benefit = any(kw in main_text for kw in benefit_keywords)
    
    confidence = 0.65 if has_benefit else 0.5
    
    evidence = [
        format_message(
            MODULE_EVIDENCE["image_icon_headings"],
            count=len(list_headings)
        ),
        format_message(
            MODULE_EVIDENCE["image_icon_images"],
            count=len(images)
        )
    ]
    if has_benefit:
        evidence.append(MODULE_EVIDENCE["image_icon_benefits"])
    
    return _create_detected_module(
        module_id="detected_image_icon_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["image_icon"],
        text=format_message(
            MODULE_TEXT["image_icon"],
            count=len(list_headings)
        ),
        confidence=confidence,
        evidence=evidence
    )


def _detect_contracts(
    links: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Contract and tariffs module (module_07)."""
    catalog_entry = catalog.get("Contract and tariffs", {})
    
    # Look for PDF links or contract keywords
    pdf_links = [
        link for link in links
        if ".pdf" in link.get("href", "").lower()
    ]
    
    contract_keywords = [
        "contrato", "tarifa", "regulamento", "condicoes", "condições",
        "termos", "documento", "download"
    ]
    
    has_contract_keyword = any(kw in main_text for kw in contract_keywords)
    
    if len(pdf_links) < 1 and not has_contract_keyword:
        return None
    
    confidence = 0.8 if len(pdf_links) > 0 else 0.6
    
    evidence = []
    if pdf_links:
        evidence.append(
            format_message(
                MODULE_EVIDENCE["contracts_pdf_links"],
                count=len(pdf_links)
            )
        )
    if has_contract_keyword:
        evidence.append(MODULE_EVIDENCE["contracts_keywords"])
    
    return _create_detected_module(
        module_id="detected_contracts_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["contracts"],
        text=format_message(
            MODULE_TEXT["contracts"],
            count=len(pdf_links)
        ),
        confidence=confidence,
        evidence=evidence
    )


def _detect_card_with_icon(
    headings: List[Dict],
    images: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Card with icon module (module_08)."""
    catalog_entry = catalog.get("Card with icon", {})
    
    # Similar to image icon but with card structure
    list_headings = [h for h in headings if h.get("level") in ["3", "4"]]
    
    if len(list_headings) < 2:
        return None
    
    # Card keywords
    card_keywords = [
        "beneficio", "benefício", "vantagem", "diferencial",
        "funcionalidade", "caracteristica", "característica"
    ]
    
    has_card_keyword = any(kw in main_text for kw in card_keywords)
    
    if not has_card_keyword and len(images) < 2:
        return None
    
    confidence = 0.7 if has_card_keyword and len(images) >= 2 else 0.55
    
    evidence = [
        format_message(
            MODULE_EVIDENCE["card_icon_headings"],
            count=len(list_headings)
        )
    ]
    if has_card_keyword:
        evidence.append(MODULE_EVIDENCE["card_icon_keywords"])
    if images:
        evidence.append(
            format_message(
                MODULE_EVIDENCE["card_icon_images"],
                count=len(images)
            )
        )
    
    return _create_detected_module(
        module_id="detected_card_icon_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["card_icon"],
        text=format_message(MODULE_TEXT["card_icon"], count=len(list_headings)),
        confidence=confidence,
        evidence=evidence
    )


def _detect_media_with_steps(
    headings: List[Dict],
    main_text: str,
    images: List[Dict],
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Media with steps module (module_10)."""
    catalog_entry = catalog.get("Media with steps", {})
    
    # Look for step indicators
    step_keywords = [
        "passo", "etapa", "primeiro", "segundo", "terceiro",
        "depois", "por fim", "finalmente", "como fazer"
    ]
    
    has_step_keyword = any(kw in main_text for kw in step_keywords)
    
    # Look for numbered patterns
    numbered_pattern = re.findall(r'\b[1-9]\.\s|\b[1-9]\)\s', main_text)
    
    if not has_step_keyword and len(numbered_pattern) < 2:
        return None
    
    confidence = 0.75 if has_step_keyword and numbered_pattern else 0.6
    
    evidence = []
    if has_step_keyword:
        evidence.append(MODULE_EVIDENCE["media_steps_keywords"])
    if numbered_pattern:
        evidence.append(
            format_message(
                MODULE_EVIDENCE["media_steps_numbered"],
                count=len(numbered_pattern)
            )
        )
    if images:
        evidence.append(MODULE_EVIDENCE["media_steps_media"])
    
    return _create_detected_module(
        module_id="detected_media_steps_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["media_steps"],
        text=MODULE_TEXT["media_steps"],
        confidence=confidence,
        evidence=evidence
    )


def _detect_whatsapp(
    links: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> Dict[str, Any] | None:
    """Detect Button Help WhatsApp module (module_11)."""
    catalog_entry = catalog.get("Button Help WhatsApp", {})
    
    # Look for WhatsApp indicators
    whatsapp_keywords = [
        "whatsapp", "whats app", "wpp", "wa.me"
    ]
    
    has_whatsapp = any(kw in main_text for kw in whatsapp_keywords)
    
    # Check links for WhatsApp
    whatsapp_links = [
        link for link in links
        if any(kw in link.get("href", "").lower() for kw in whatsapp_keywords)
    ]
    
    if not has_whatsapp and not whatsapp_links:
        return None
    
    confidence = 0.9 if whatsapp_links else 0.7
    
    evidence = []
    if whatsapp_links:
        evidence.append(
            format_message(
                MODULE_EVIDENCE["whatsapp_links"],
                count=len(whatsapp_links)
            )
        )
    if has_whatsapp:
        evidence.append(MODULE_EVIDENCE["whatsapp_keywords"])
    
    return _create_detected_module(
        module_id="detected_whatsapp_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["whatsapp"],
        text=MODULE_TEXT["whatsapp"],
        confidence=confidence,
        evidence=evidence
    )


def _detect_qr_codes(
    images: List[Dict],
    main_text: str,
    catalog: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """Detect QR Code modules (module_13, module_14)."""
    qr_modules = []
    
    # Look for QR code indicators
    qr_keywords = [
        "qr code", "qrcode", "qr", "codigo qr", "código qr",
        "escaneie", "escanear", "scanner"
    ]
    
    has_qr = any(kw in main_text for kw in qr_keywords)
    
    # Check image alt texts for QR
    qr_images = [
        img for img in images
        if any(kw in img.get("alt", "").lower() for kw in qr_keywords)
    ]
    
    if not has_qr and not qr_images:
        return qr_modules
    
    # Determine which QR module
    catalog_entry = catalog.get("QR Code Nativo", {})
    
    confidence = 0.85 if qr_images else 0.65
    
    evidence = []
    if qr_images:
        evidence.append(
            format_message(
                MODULE_EVIDENCE["qr_images"],
                count=len(qr_images)
            )
        )
    if has_qr:
        evidence.append(MODULE_EVIDENCE["qr_keywords"])
    
    qr_module = _create_detected_module(
        module_id="detected_qr_0",
        catalog_entry=catalog_entry,
        title=MODULE_TITLES["qr"],
        text=MODULE_TEXT["qr"],
        confidence=confidence,
        evidence=evidence
    )
    
    qr_modules.append(qr_module)
    
    return qr_modules


# Made with Bob