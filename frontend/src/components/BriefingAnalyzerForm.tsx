import React, { useState } from 'react';
import { analyzeBriefing, AnalyzeBriefingPayload, AnalysisResponse } from '../lib/api';

interface BriefingAnalyzerFormProps {
  onResult: (result: AnalysisResponse) => void;
  onError: (error: string) => void;
  onLoading: (loading: boolean) => void;
}

export const BriefingAnalyzerForm: React.FC<BriefingAnalyzerFormProps> = ({ onResult, onError, onLoading }) => {
  const [formData, setFormData] = useState({
    briefing: '',
    business_goal: '',
    target_audience: '',
    constraints: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.briefing) {
      onError('Briefing is required');
      return;
    }

    try {
      onLoading(true);
      onError('');
      
      const payload: AnalyzeBriefingPayload = {
        briefing: formData.briefing,
        ...(formData.business_goal && { business_goal: formData.business_goal }),
        ...(formData.target_audience && { target_audience: formData.target_audience }),
        ...(formData.constraints && { 
          constraints: formData.constraints.split(',').map(c => c.trim()).filter(c => c) 
        }),
      };
      
      const result = await analyzeBriefing(payload);
      onResult(result);
    } catch (err: any) {
      onError(err.response?.data?.detail || err.message || 'Failed to analyze briefing');
    } finally {
      onLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="briefing" className="block text-sm font-medium text-gray-700 mb-1">
          Briefing *
        </label>
        <textarea
          id="briefing"
          required
          value={formData.briefing}
          onChange={(e) => setFormData({ ...formData, briefing: e.target.value })}
          placeholder="Describe your marketing page requirements..."
          rows={6}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label htmlFor="business_goal_briefing" className="block text-sm font-medium text-gray-700 mb-1">
          Business Goal
        </label>
        <input
          type="text"
          id="business_goal_briefing"
          value={formData.business_goal}
          onChange={(e) => setFormData({ ...formData, business_goal: e.target.value })}
          placeholder="e.g., increase conversions, generate leads"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label htmlFor="target_audience_briefing" className="block text-sm font-medium text-gray-700 mb-1">
          Target Audience
        </label>
        <input
          type="text"
          id="target_audience_briefing"
          value={formData.target_audience}
          onChange={(e) => setFormData({ ...formData, target_audience: e.target.value })}
          placeholder="e.g., small business owners, millennials"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <div>
        <label htmlFor="constraints" className="block text-sm font-medium text-gray-700 mb-1">
          Constraints (comma-separated)
        </label>
        <input
          type="text"
          id="constraints"
          value={formData.constraints}
          onChange={(e) => setFormData({ ...formData, constraints: e.target.value })}
          placeholder="e.g., mobile-first, no video, budget limit"
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
        />
      </div>

      <button
        type="submit"
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
      >
        Analyze Briefing
      </button>
    </form>
  );
};

// Made with Bob
