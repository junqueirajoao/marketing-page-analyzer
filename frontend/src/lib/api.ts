import axios from 'axios';

const API_BASE_URL = 'http://localhost:8001';

export interface AnalyzeUrlPayload {
  url: string;
  business_goal?: string;
  target_audience?: string;
  page_type_hint?: string;
}

export interface AnalyzeBriefingPayload {
  briefing: string;
  business_goal?: string;
  target_audience?: string;
  constraints?: string[];
}

export interface DetectedModule {
  id: string;
  type: string;
  matched_catalog_id: string;
  matched_catalog_name: string;
  display_name: string;
  title: string;
  text: string;
  position: number;
  confidence: number;
  evidence: string[];
}

export interface AnalysisResponse {
  analysis_id: string;
  score: {
    overall: number;
    seo: number;
    storytelling: number;
    modules: number;
    brand_safety: number;
  };
  page_summary: {
    detected_type: string;
    primary_goal: string;
    main_topic: string;
  };
  recommendations: Array<{
    priority: string;
    area: string;
    title: string;
    why: string;
    suggestion: string;
    impact: string;
    effort: string;
  }>;
  module_plan: {
    keep: any[];
    remove: any[];
    reorder: any[];
    add: any[];
  };
  copy_suggestions: Array<{
    section: string;
    current: string;
    suggested: string;
    reason: string;
  }>;
  catalog_context: {
    modules_available_count: number;
    storytelling_patterns_count: number;
    brand_rules_count: number;
  };
  agent_trace: Array<{
    agent: string;
    status: string;
    summary: string;
  }>;
  page_diagnostics?: {
    has_title: boolean;
    has_meta_description: boolean;
    headings_count: number;
    links_count: number;
    images_count: number;
    has_error: boolean;
    modules_detected_count?: number;
  };
  detected_modules?: DetectedModule[];
}

export async function analyzeUrl(payload: AnalyzeUrlPayload): Promise<AnalysisResponse> {
  const response = await axios.post(`${API_BASE_URL}/analyze/url`, payload);
  return response.data;
}

export async function analyzeBriefing(payload: AnalyzeBriefingPayload): Promise<AnalysisResponse> {
  const response = await axios.post(`${API_BASE_URL}/analyze/briefing`, payload);
  return response.data;
}

// Made with Bob
