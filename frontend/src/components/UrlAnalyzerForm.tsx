import { useState } from 'react';
import { analyzeUrl, AnalyzeUrlPayload, AnalysisResponse } from '../lib/api';

interface UrlAnalyzerFormProps {
  onResult: (result: AnalysisResponse) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export const UrlAnalyzerForm: React.FC<UrlAnalyzerFormProps> = ({ onResult, onError, onLoading }) => {
  const [url, setUrl] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url) {
      onError('URL é obrigatória');
      return;
    }

    try {
      onLoading(true);
      onError('');
      
      const payload: AnalyzeUrlPayload = {
        url: url,
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
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <label htmlFor="url" className="block text-sm font-medium text-gray-700 mb-2">
          URL da Página *
        </label>
        <input
          type="url"
          id="url"
          required
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://example.com/sua-pagina"
          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-base"
        />
        <p className="mt-2 text-sm text-gray-500">
          Cole a URL da página que deseja analisar. O sistema irá automaticamente identificar o tipo, objetivo e público-alvo.
        </p>
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors font-medium text-base"
      >
        🚀 Analisar Página
      </button>
    </form>
  );
};

// Made with Bob
