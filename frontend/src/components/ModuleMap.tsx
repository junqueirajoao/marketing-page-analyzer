import { DetectedModule } from '../lib/api';

interface ModuleMapProps {
  detectedModules?: DetectedModule[];
  modulePlan?: {
    keep: any[];
    remove: any[];
    reorder: any[];
    add: any[];
  };
}

export const ModuleMap: React.FC<ModuleMapProps> = ({ detectedModules, modulePlan }) => {
  // If no modules detected, show empty state
  if (!detectedModules || detectedModules.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
        <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
          <span className="text-2xl">🗺️</span>
          Mapa de Módulos Detectados
        </h3>
        <div className="text-center py-8">
          <div className="text-6xl mb-4">📭</div>
          <p className="text-gray-600 mb-2 font-medium">
            Nenhum módulo foi detectado nesta análise.
          </p>
          <p className="text-sm text-gray-500">
            Verifique se a URL retornou HTML válido ou se a página depende de JavaScript.
          </p>
        </div>
      </div>
    );
  }

  // Get module status from module_plan
  const getModuleStatus = (moduleName: string) => {
    if (!modulePlan) return 'detected';
    
    if (modulePlan.keep?.some((item: any) => 
      typeof item === 'string' ? item === moduleName : item.name === moduleName
    )) {
      return 'keep';
    }
    
    if (modulePlan.remove?.some((item: any) => 
      typeof item === 'string' ? item === moduleName : item.module_type === moduleName
    )) {
      return 'remove';
    }
    
    if (modulePlan.reorder?.some((item: any) => 
      typeof item === 'string' ? item === moduleName : item.module_type === moduleName
    )) {
      return 'reorder';
    }
    
    return 'detected';
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'keep':
        return 'border-green-300 bg-green-50';
      case 'remove':
        return 'border-red-300 bg-red-50';
      case 'reorder':
        return 'border-orange-300 bg-orange-50';
      default:
        return 'border-blue-300 bg-blue-50';
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'keep':
        return <span className="px-2 py-1 bg-green-200 text-green-800 text-xs font-bold rounded">✅ Manter</span>;
      case 'remove':
        return <span className="px-2 py-1 bg-red-200 text-red-800 text-xs font-bold rounded">❌ Remover</span>;
      case 'reorder':
        return <span className="px-2 py-1 bg-orange-200 text-orange-800 text-xs font-bold rounded">🔄 Reordenar</span>;
      default:
        return <span className="px-2 py-1 bg-blue-200 text-blue-800 text-xs font-bold rounded">🔍 Detectado</span>;
    }
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return 'text-green-600';
    if (confidence >= 0.6) return 'text-orange-600';
    return 'text-red-600';
  };

  // Sort modules by position
  const sortedModules = [...detectedModules].sort((a, b) => a.position - b.position);

  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
      <h3 className="text-xl font-bold text-gray-900 mb-4 flex items-center gap-2">
        <span className="text-2xl">🗺️</span>
        Mapa de Módulos Detectados ({detectedModules.length})
      </h3>
      
      <div className="space-y-4">
        {sortedModules.map((module) => {
          const status = getModuleStatus(module.matched_catalog_name);
          
          return (
            <div 
              key={module.id} 
              className={`border-2 rounded-xl p-5 transition-all hover:shadow-lg ${getStatusColor(status)}`}
            >
              {/* Header */}
              <div className="flex items-start justify-between mb-3">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-bold text-gray-500">#{module.position}</span>
                    <h4 className="font-bold text-gray-900 text-lg">
                      {module.display_name}
                    </h4>
                  </div>
                  <div className="text-sm text-gray-600">
                    <span className="font-medium">Catálogo:</span> {module.matched_catalog_name}
                  </div>
                  <div className="text-sm text-gray-600">
                    <span className="font-medium">ID:</span> {module.matched_catalog_id}
                  </div>
                </div>
                <div className="flex flex-col items-end gap-2">
                  {getStatusBadge(status)}
                  <div className={`text-sm font-bold ${getConfidenceColor(module.confidence)}`}>
                    {Math.round(module.confidence * 100)}% confiança
                  </div>
                </div>
              </div>

              {/* Content */}
              {module.title && (
                <div className="mb-2">
                  <span className="text-xs font-bold text-gray-500 uppercase">Título:</span>
                  <div className="text-sm text-gray-700 mt-1">{module.title}</div>
                </div>
              )}

              {module.text && module.text !== module.title && (
                <div className="mb-2">
                  <span className="text-xs font-bold text-gray-500 uppercase">Conteúdo:</span>
                  <div className="text-sm text-gray-700 mt-1">{module.text}</div>
                </div>
              )}

              {/* Evidence */}
              {module.evidence && module.evidence.length > 0 && (
                <div className="mt-3 pt-3 border-t border-gray-300">
                  <span className="text-xs font-bold text-gray-500 uppercase">Evidências:</span>
                  <ul className="mt-2 space-y-1">
                    {module.evidence.map((evidence, idx) => (
                      <li key={idx} className="text-xs text-gray-600 flex items-start gap-2">
                        <span className="text-blue-500">•</span>
                        <span>{evidence}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Recommendations from module_plan */}
      {modulePlan && (modulePlan.add?.length > 0 || modulePlan.remove?.length > 0) && (
        <div className="mt-6 pt-6 border-t-2 border-gray-200">
          <h4 className="font-bold text-gray-900 mb-3 flex items-center gap-2">
            <span>💡</span>
            Recomendações de Módulos
          </h4>
          
          <div className="grid md:grid-cols-2 gap-4">
            {modulePlan.add && modulePlan.add.length > 0 && (
              <div className="border-2 border-blue-300 rounded-xl p-4 bg-blue-50">
                <h5 className="font-semibold text-blue-900 mb-2 flex items-center gap-2">
                  <span>➕</span> Adicionar ({modulePlan.add.length})
                </h5>
                <ul className="text-sm text-blue-800 space-y-2">
                  {modulePlan.add.map((item: any, idx: number) => (
                    <li key={idx} className="flex flex-col gap-1">
                      <span className="font-medium">
                        • {typeof item === 'string' ? item : item.module_type || JSON.stringify(item)}
                      </span>
                      {typeof item === 'object' && item.reason && (
                        <span className="text-xs text-blue-700 ml-3">{item.reason}</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {modulePlan.remove && modulePlan.remove.length > 0 && (
              <div className="border-2 border-red-300 rounded-xl p-4 bg-red-50">
                <h5 className="font-semibold text-red-900 mb-2 flex items-center gap-2">
                  <span>❌</span> Remover ({modulePlan.remove.length})
                </h5>
                <ul className="text-sm text-red-800 space-y-2">
                  {modulePlan.remove.map((item: any, idx: number) => (
                    <li key={idx} className="flex flex-col gap-1">
                      <span className="font-medium">
                        • {typeof item === 'string' ? item : item.module_type || JSON.stringify(item)}
                      </span>
                      {typeof item === 'object' && item.reason && (
                        <span className="text-xs text-red-700 ml-3">{item.reason}</span>
                      )}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

// Made with Bob