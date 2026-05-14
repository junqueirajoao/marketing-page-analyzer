import { useState } from 'react';
import { analyzeUrl, AnalyzeUrlPayload, AnalysisResponse } from '../lib/api';

interface UrlAnalyzerFormProps {
  onResult: (result: AnalysisResponse) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export const UrlAnalyzerForm: React.FC<UrlAnalyzerFormProps> = ({ onResult, onError, onLoading }) => {
  const [formData, setFormData] = useState<AnalyzeUrlPayload>({
    url: '',
    business_goal: '',
    target_audience: '',
    page_type_hint: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.url) {
      onError('URL é obrigatória');
      return;
    }

    try {
      onLoading(true);
      onError('');
      
      const payload: AnalyzeUrlPayload = {
        url: formData.url,
        ...(formData.business_goal && { business_goal: formData.business_goal }),
        ...(formData.target_audience && { target_audience: formData.target_audience }),
        ...(formData.page_type_hint && { page_type_hint: formData.page_type_hint }),
      };
      
      const result = await analyzeUrl(payload);
      onResult(result);
    } catch (err: any) {
      onError(err.response?.data?.detail || err.message || 'Falha ao analisar URL');
    } finally {
      onLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-1">
          URL *
        </label>
        <input
          type="url"
          id="url"
          required
          value={formData.url}
          onChange={(e) => setFormData({ ...formData, url: e.target.value })}
          placeholder="https://example.com"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label htmlFor="business_goal" className="block text-sm font-medium text-gray-700 mb-1">
          Objetivo de Negócio
        </label>
        <input
          type="text"
          id="business_goal"
          value={formData.business_goal}
          onChange={(e) => setFormData({ ...formData, business_goal: e.target.value })}
          placeholder="ex: aumentar conversões, gerar leads"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label htmlFor="target_audience" className="block text-sm font-medium text-gray-700 mb-1">
          Público-Alvo
        </label>
        <input
          type="text"
          id="target_audience"
          value={formData.target_audience}
          onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
          placeholder="ex: pequenos empresários, millennials"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label htmlFor="page_type_hint" className="block text-sm font-medium text-gray-700 mb-1">
          Tipo de Página (Dica)
        </label>
        <input
          type="text"
          id="page_type_hint"
          value={formData.page_type_hint}
          onChange={(e) => setFormData({ ...formData, page_type_hint: e.target.value })}
          placeholder="ex: produto, serviço, landing page"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
      >
        Analisar URL
      </button>
    </form>
  );
};

// Made with Bob
