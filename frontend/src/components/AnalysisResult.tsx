import { AnalysisResponse } from '../lib/api';
import { CollapsibleSection } from './CollapsibleSection';
import { ModuleMap } from './ModuleMap';
import { NarrativeInsights } from './NarrativeInsights';
import { ScoreBreakdown } from './ScoreBreakdown';

interface AnalysisResultProps {
  data: AnalysisResponse;
}

export const AnalysisResult: React.FC<AnalysisResultProps> = ({ data }) => {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600 bg-green-50 border-green-200';
    if (score >= 60) return 'text-orange-600 bg-orange-50 border-orange-200';
    return 'text-red-600 bg-red-50 border-red-200';
  };

  const getPriorityColor = (priority: string) => {
    switch (priority.toLowerCase()) {
      case 'high':
      case 'alta':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'medium':
      case 'média':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      case 'low':
      case 'baixa':
        return 'bg-gray-100 text-gray-800 border-gray-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  return (
    <div className="mt-8 space-y-6">
      {/* Header with Overall Score - Dashboard executivo */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-xl shadow-lg p-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2">Análise Concluída</h2>
            <p className="text-blue-100">ID: {data.analysis_id}</p>
          </div>
          <div className="text-center">
            <div className="text-5xl font-bold">{data.score.overall}</div>
            <div className="text-sm text-blue-100 mt-1">Pontuação Geral</div>
          </div>
        </div>
      </div>

      {/* Score Breakdown - Cards de SEO, storytelling, módulos e segurança de marca */}
      <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <span className="text-2xl">📊</span>
          Detalhamento de Pontuação
        </h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {Object.entries(data.score).map(([key, value]) => {
            if (key === 'overall') return null;
            const icons: Record<string, string> = {
              seo: '🔍',
              storytelling: '📖',
              modules: '🧩',
              brand_safety: '🛡️'
            };
            const labels: Record<string, string> = {
              seo: 'SEO',
              storytelling: 'Storytelling',
              modules: 'Módulos',
              brand_safety: 'Segurança de Marca'
            };
            return (
              <div key={key} className={`border-2 rounded-xl p-4 transition-all hover:shadow-lg ${getScoreColor(value)}`}>
                <div className="text-3xl mb-2">{icons[key] || '📈'}</div>
                <div className="text-2xl font-bold">{value}</div>
                <div className="text-sm font-medium mt-1">
                  {labels[key] || key}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Score Breakdown - Detalhamento de pontuação - COLLAPSED BY DEFAULT */}
      {data.score_breakdown && <ScoreBreakdown breakdown={data.score_breakdown} />}

      {/* Recommendations - Top prioridades - COLLAPSED BY DEFAULT */}
      {data.recommendations && data.recommendations.length > 0 && (
        <CollapsibleSection
          title="Principais Prioridades"
          icon="⭐"
          badge={data.recommendations.length}
          defaultExpanded={false}
        >
          <div className="space-y-4">
            {data.recommendations.map((rec, index) => (
              <div key={index} className="border-2 border-gray-200 rounded-xl p-5 hover:shadow-lg transition-all hover:border-blue-300">
                <div className="flex items-start justify-between mb-3">
                  <h4 className="font-semibold text-gray-900 flex-1 text-lg">{rec.title}</h4>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold border-2 ${getPriorityColor(rec.priority)}`}>
                    {rec.priority}
                  </span>
                </div>
                <div className="text-sm text-gray-600 mb-2">
                  <span className="font-medium">Área:</span> {rec.area}
                </div>
                <div className="text-sm text-gray-700 mb-2">
                  <span className="font-medium">Por quê:</span> {rec.why}
                </div>
                <div className="text-sm text-gray-700 mb-2">
                  <span className="font-medium">Sugestão:</span> {rec.suggestion}
                </div>
                <div className="flex gap-4 text-xs text-gray-600 mt-3">
                  <span><span className="font-medium">Impacto:</span> {rec.impact}</span>
                  <span><span className="font-medium">Esforço:</span> {rec.effort}</span>
                </div>
              </div>
            ))}
          </div>
        </CollapsibleSection>
      )}

      {/* Module Map - Mapa de módulos detectados com recomendações */}
      <ModuleMap
        detectedModules={data.detected_modules}
        modulePlan={data.module_plan}
      />

      {/* Narrative Insights - Insights estruturais e narrativos */}
      <NarrativeInsights insights={data.narrative_insights} />

      {/* Page Diagnostics - Checklist final - COLLAPSED BY DEFAULT */}
      {data.page_diagnostics && (
        <CollapsibleSection
          title="Checklist Final"
          icon="✔️"
          defaultExpanded={false}
        >
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            <div className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${data.page_diagnostics.has_title ? 'bg-green-500' : 'bg-red-500'}`}></span>
              <span className="text-sm text-gray-700">Tag de Título</span>
            </div>
            <div className="flex items-center gap-2">
              <span className={`w-3 h-3 rounded-full ${data.page_diagnostics.has_meta_description ? 'bg-green-500' : 'bg-red-500'}`}></span>
              <span className="text-sm text-gray-700">Meta Descrição</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-700">Cabeçalhos: {data.page_diagnostics.headings_count}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-700">Links: {data.page_diagnostics.links_count}</span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-700">Imagens: {data.page_diagnostics.images_count}</span>
            </div>
            {data.page_diagnostics.modules_detected_count !== undefined && (
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-700">Módulos: {data.page_diagnostics.modules_detected_count}</span>
              </div>
            )}
          </div>
        </CollapsibleSection>
      )}

      {/* Catalog Context - COLLAPSED BY DEFAULT */}
      <CollapsibleSection
        title="Contexto do Catálogo"
        icon="📚"
        defaultExpanded={false}
      >
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-4 bg-blue-50 rounded-xl border-2 border-blue-200">
            <div className="text-4xl font-bold text-blue-600">{data.catalog_context.modules_available_count}</div>
            <div className="text-sm text-gray-700 mt-2 font-medium">Módulos Disponíveis</div>
          </div>
          <div className="text-center p-4 bg-orange-50 rounded-xl border-2 border-orange-200">
            <div className="text-4xl font-bold text-orange-600">{data.catalog_context.storytelling_patterns_count}</div>
            <div className="text-sm text-gray-700 mt-2 font-medium">Padrões de Storytelling</div>
          </div>
          <div className="text-center p-4 bg-blue-50 rounded-xl border-2 border-blue-200">
            <div className="text-4xl font-bold text-blue-600">{data.catalog_context.brand_rules_count}</div>
            <div className="text-sm text-gray-700 mt-2 font-medium">Regras de Marca</div>
          </div>
        </div>
      </CollapsibleSection>

      {/* Agent Trace - COLLAPSED BY DEFAULT */}
      {data.agent_trace && data.agent_trace.length > 0 && (
        <CollapsibleSection
          title="Rastreamento de Agentes"
          icon="🤖"
          badge={data.agent_trace.length}
          defaultExpanded={false}
        >
          <div className="space-y-2">
            {data.agent_trace.map((trace, index) => (
              <div key={index} className="flex items-start gap-3 text-sm">
                <span className={`px-2 py-1 rounded text-xs font-medium ${
                  trace.status === 'success' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {trace.status}
                </span>
                <div className="flex-1">
                  <span className="font-medium text-gray-900">{trace.agent}:</span>
                  <span className="text-gray-700 ml-2">{trace.summary}</span>
                </div>
              </div>
            ))}
          </div>
        </CollapsibleSection>
      )}
    </div>
  );
};

// Made with Bob