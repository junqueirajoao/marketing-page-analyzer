import { useState } from 'react';
import { UrlAnalyzerForm } from './components/UrlAnalyzerForm';
import { AnalysisResult } from './components/AnalysisResult';
import { AnalysisResponse } from './lib/api';

function App() {
  const [result, setResult] = useState<AnalysisResponse | null>(null);
  const [error, setError] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  const handleResult = (data: AnalysisResponse) => {
    setResult(data);
    setError('');
  };

  const handleError = (errorMessage: string) => {
    setError(errorMessage);
    setResult(null);
  };

  const handleLoading = (isLoading: boolean) => {
    setLoading(isLoading);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-4xl mx-auto py-8 px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Financial Marketing Pages Analyzer
          </h1>
          <p className="text-gray-600">
            Analise páginas de marketing financeiro reais para obter insights acionáveis baseados em IA.
          </p>
        </div>

        {/* Main Form */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <UrlAnalyzerForm
            onResult={handleResult}
            onError={handleError}
            onLoading={handleLoading}
          />

          {/* Loading State */}
          {loading && (
            <div className="mt-6 text-center">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              <p className="mt-2 text-gray-600">Analisando...</p>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mt-6 bg-red-50 border border-red-200 rounded-md p-4">
              <p className="text-red-800 text-sm">{error}</p>
            </div>
          )}

          {/* Result */}
          {result && !loading && <AnalysisResult data={result} />}
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-sm text-gray-500">
          <p>Financial Marketing Pages Analyzer - AI-Powered Page Analysis</p>
        </div>
      </div>
    </div>
  );
}

export default App;

// Made with Bob
