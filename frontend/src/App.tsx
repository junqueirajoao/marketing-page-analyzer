import { useState } from 'react';
import { UrlAnalyzerForm } from './components/UrlAnalyzerForm';
import { BriefingAnalyzerForm } from './components/BriefingAnalyzerForm';
import { AnalysisResult } from './components/AnalysisResult';
import { AnalysisResponse } from './lib/api';

type TabType = 'url' | 'briefing';

function App() {
  const [activeTab, setActiveTab] = useState<TabType>('url');
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
            Marketing Page Analyzer
          </h1>
          <p className="text-gray-600">
            Analise suas páginas de marketing ou briefings para obter insights e recomendações acionáveis.
          </p>
        </div>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <div className="flex border-b border-gray-200 mb-6">
            <button
              onClick={() => {
                setActiveTab('url');
                setResult(null);
                setError('');
              }}
              className={`px-4 py-2 font-medium text-sm focus:outline-none ${
                activeTab === 'url'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Analisar por URL
            </button>
            <button
              onClick={() => {
                setActiveTab('briefing');
                setResult(null);
                setError('');
              }}
              className={`px-4 py-2 font-medium text-sm focus:outline-none ${
                activeTab === 'briefing'
                  ? 'border-b-2 border-blue-600 text-blue-600'
                  : 'text-gray-500 hover:text-gray-700'
              }`}
            >
              Analisar por Briefing
            </button>
          </div>

          {/* Forms */}
          {activeTab === 'url' ? (
            <UrlAnalyzerForm
              onResult={handleResult}
              onError={handleError}
              onLoading={handleLoading}
            />
          ) : (
            <BriefingAnalyzerForm
              onResult={handleResult}
              onError={handleError}
              onLoading={handleLoading}
            />
          )}

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
          <p>Marketing Page Analyzer - Bob-a-thon</p>
        </div>
      </div>
    </div>
  );
}

export default App;

// Made with Bob
