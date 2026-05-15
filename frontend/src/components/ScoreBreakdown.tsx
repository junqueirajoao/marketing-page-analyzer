import React from 'react';
import { ScoreBreakdown as ScoreBreakdownType, ScoreBreakdownItem } from '../lib/api';
import { CollapsibleSection } from './CollapsibleSection';

interface ScoreBreakdownProps {
  breakdown: ScoreBreakdownType;
}

export const ScoreBreakdown: React.FC<ScoreBreakdownProps> = ({ breakdown }) => {
  const getImpactColor = (impact: number) => {
    if (impact > 0) return 'text-green-600';
    if (impact <= -15) return 'text-red-600';
    if (impact <= -8) return 'text-orange-600';
    return 'text-yellow-600';
  };

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'seo':
        return '🔍';
      case 'storytelling':
        return '📖';
      case 'modules':
        return '🧩';
      case 'brand_safety':
        return '🛡️';
      default:
        return '📊';
    }
  };

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'seo':
        return 'SEO';
      case 'storytelling':
        return 'Storytelling';
      case 'modules':
        return 'Módulos';
      case 'brand_safety':
        return 'Segurança de Marca';
      default:
        return category;
    }
  };

  const categories = Object.entries(breakdown).filter(
    ([_, items]) => items && items.length > 0
  );

  if (categories.length === 0) {
    return null;
  }

  return (
    <CollapsibleSection
      title="Detalhamento de Pontuação"
      icon="📊"
      defaultExpanded={false}
    >
      <div className="space-y-6">
        {categories.map(([category, items]) => (
          <div key={category} className="border-l-4 border-blue-500 pl-4">
            <h4 className="font-semibold text-gray-900 mb-3 flex items-center gap-2">
              <span className="text-xl">{getCategoryIcon(category)}</span>
              {getCategoryLabel(category)}
            </h4>
            <div className="space-y-2">
              {items.map((item: ScoreBreakdownItem, idx: number) => (
                <div
                  key={idx}
                  className="bg-gray-50 rounded-lg p-3 hover:bg-gray-100 transition-colors"
                >
                  <div className="flex items-start justify-between gap-3">
                    <div className="flex-1">
                      <div className="text-sm text-gray-700">{item.reason}</div>
                      <div className="text-xs text-gray-500 mt-1">
                        Critério: {item.criterion}
                      </div>
                    </div>
                    <div
                      className={`font-bold text-lg ${getImpactColor(item.impact)}`}
                    >
                      {item.impact > 0 ? '+' : ''}
                      {item.impact}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </CollapsibleSection>
  );
};

// Made with Bob