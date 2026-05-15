import React from 'react';
import { CollapsibleSection } from './CollapsibleSection';

interface NarrativeInsight {
  id: string;
  type: string;
  severity: 'high' | 'medium' | 'low';
  title: string;
  description: string;
  related_modules: string[];
  recommended_actions: string[];
}

interface NarrativeInsightsProps {
  insights: NarrativeInsight[];
}

export const NarrativeInsights: React.FC<NarrativeInsightsProps> = ({ insights }) => {
  const getSeverityColor = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'medium':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'low':
        return 'bg-blue-100 text-blue-800 border-blue-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity.toLowerCase()) {
      case 'high':
        return '🔴';
      case 'medium':
        return '🟡';
      case 'low':
        return '🔵';
      default:
        return '⚪';
    }
  };

  if (!insights || insights.length === 0) {
    return (
      <CollapsibleSection
        title="Insights Narrativos"
        icon="💡"
        defaultExpanded={false}
      >
        <div className="text-center py-8 text-gray-500">
          <p className="text-lg">✅ Nenhum insight crítico detectado</p>
          <p className="text-sm mt-2">A estrutura narrativa está alinhada com o storytelling pattern.</p>
        </div>
      </CollapsibleSection>
    );
  }

  return (
    <CollapsibleSection
      title="Insights Narrativos"
      icon="💡"
      badge={insights.length}
      defaultExpanded={false}
    >
      <div className="space-y-4">
        {insights.map((insight) => (
          <div
            key={insight.id}
            className="border-2 border-gray-200 rounded-xl p-5 hover:shadow-lg transition-all hover:border-blue-300"
          >
            {/* Header with severity */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-start gap-3 flex-1">
                <span className="text-2xl">{getSeverityIcon(insight.severity)}</span>
                <h4 className="font-semibold text-gray-900 text-lg">{insight.title}</h4>
              </div>
              <span
                className={`px-3 py-1 rounded-full text-xs font-bold border-2 ${getSeverityColor(
                  insight.severity
                )}`}
              >
                {insight.severity.toUpperCase()}
              </span>
            </div>

            {/* Description */}
            <div className="text-sm text-gray-700 mb-4 ml-11">
              {insight.description}
            </div>

            {/* Related Modules */}
            {insight.related_modules && insight.related_modules.length > 0 && (
              <div className="mb-3 ml-11">
                <span className="text-xs font-bold text-gray-500 uppercase">Módulos Relacionados:</span>
                <div className="flex flex-wrap gap-2 mt-2">
                  {insight.related_modules.map((module, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-blue-50 text-blue-700 rounded-lg text-xs font-medium border border-blue-200"
                    >
                      {module}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {/* Recommended Actions */}
            {insight.recommended_actions && insight.recommended_actions.length > 0 && (
              <div className="ml-11">
                <span className="text-xs font-bold text-gray-500 uppercase">Ações Recomendadas:</span>
                <ul className="mt-2 space-y-1">
                  {insight.recommended_actions.map((action, idx) => (
                    <li key={idx} className="text-sm text-gray-700 flex items-start gap-2">
                      <span className="text-green-600 font-bold">→</span>
                      <span>{action}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ))}
      </div>
    </CollapsibleSection>
  );
};

// Made with Bob