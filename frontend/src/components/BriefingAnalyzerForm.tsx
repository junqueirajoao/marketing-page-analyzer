import { useState } from 'react';
import { analyzeBriefing, AnalyzeBriefingPayload, AnalysisResponse } from '../lib/api';

interface BriefingAnalyzerFormProps {
  onResult: (result: AnalysisResponse) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export const BriefingAnalyzerForm: React.FC<BriefingAnalyzerFormProps> = ({ onResult, onError, onLoading }) => {
  const [formData, setFormData] = useState({
    briefing: '',
    constraints: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.briefing) {
      onError('Briefing é obrigatório');
      return;
    }

    try {
      onLoading(true);
      onError('');
      
      const payload: AnalyzeBriefingPayload = {
        briefing: formData.briefing,
        ...(formData.constraints && {
          constraints: formData.constraints.split(',').map(c => c.trim()).filter(c => c)
        }),
      };
      
      const result = await analyzeBriefing(payload);
      onResult(result);
    } catch (err: any) {
      onError(err.response?.data?.detail || err.message || 'Falha ao analisar briefing');
    } finally {
      onLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="briefing" className="block text-sm font-medium text-gray-700 mb-2">
          Briefing da Página *
        </label>
        <textarea
          id="briefing"
          required
          value={formData.briefing}
          onChange={(e) => setFormData({ ...formData, briefing: e.target.value })}
          placeholder="Descreva os requisitos da sua página de marketing. Exemplo: Preciso de uma landing page para promover nosso novo produto de investimentos..."
          rows={8}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-base"
        />
        <p className="mt-2 text-sm text-gray-500">
          Descreva o que você precisa. O sistema irá automaticamente identificar o tipo de página, objetivo e público-alvo ideal.
        </p>
      </div>

      <div>
        <label htmlFor="constraints" className="block text-sm font-medium text-gray-700 mb-2">
          Restrições (opcional)
        </label>
        <input
          type="text"
          id="constraints"
          value={formData.constraints}
          onChange={(e) => setFormData({ ...formData, constraints: e.target.value })}
          placeholder="ex: mobile-first, sem vídeo, limite de orçamento"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-base"
        />
        <p className="mt-2 text-sm text-gray-500">
          Separe múltiplas restrições por vírgula.
        </p>
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors font-medium text-base"
      >
        🚀 Analisar Briefing
      </button>
    </form>
  );
};

// Made with Bob
