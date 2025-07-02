import React, { useState } from 'react';
import { 
  BarChart3, 
  Database, 
  AlertTriangle, 
  CheckCircle,
  TrendingUp,
  Info,
  ChevronDown,
  ChevronUp
} from 'lucide-react';

const InsightsPanel = ({ insights }) => {
  const [expandedSections, setExpandedSections] = useState({
    basic: true,
    quality: true,
    patterns: true,
    recommendations: true
  });

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  if (!insights) {
    return (
      <div className="bg-white rounded-2xl shadow-lg p-6">
        <div className="text-center text-gray-500">
          <Database className="h-12 w-12 mx-auto mb-4 opacity-50" />
          <p>Upload a file to see insights</p>
        </div>
      </div>
    );
  }

  const { basic_stats, data_quality, patterns, recommendations } = insights;

  const getQualityColor = (percentage) => {
    if (percentage >= 90) return 'text-green-600 bg-green-100';
    if (percentage >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const SectionHeader = ({ title, icon: Icon, section, count }) => (
    <button
      onClick={() => toggleSection(section)}
      className="w-full flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg transition-colors"
    >
      <div className="flex items-center space-x-3">
        <Icon className="h-5 w-5 text-blue-600" />
        <h3 className="font-semibold text-gray-900">{title}</h3>
        {count !== undefined && (
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
            {count}
          </span>
        )}
      </div>
      {expandedSections[section] ? (
        <ChevronUp className="h-4 w-4 text-gray-400" />
      ) : (
        <ChevronDown className="h-4 w-4 text-gray-400" />
      )}
    </button>
  );

  return (
    <div className="bg-white rounded-2xl shadow-lg h-[700px] overflow-y-auto custom-scrollbar">
      <div className="p-6 border-b border-gray-200">
        <h2 className="text-xl font-bold text-gray-900 flex items-center">
          <TrendingUp className="h-6 w-6 mr-2 text-blue-600" />
          Data Insights
        </h2>
        <p className="text-sm text-gray-600 mt-1">
          AI-generated analysis of your dataset
        </p>
      </div>

      <div className="p-6 space-y-6">
        {/* Basic Statistics */}
        <div className="border border-gray-200 rounded-lg overflow-hidden">
          <SectionHeader 
            title="Dataset Overview" 
            icon={Database} 
            section="basic"
          />
          
          {expandedSections.basic && (
            <div className="p-4 bg-gray-50 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-white p-3 rounded-lg">
                  <p className="text-sm text-gray-600">Rows</p>
                  <p className="text-xl font-bold text-gray-900">
                    {basic_stats?.shape?.[0]?.toLocaleString() || 'N/A'}
                  </p>
                </div>
                <div className="bg-white p-3 rounded-lg">
                  <p className="text-sm text-gray-600">Columns</p>
                  <p className="text-xl font-bold text-gray-900">
                    {basic_stats?.shape?.[1] || 'N/A'}
                  </p>
                </div>
              </div>
              
              <div className="bg-white p-3 rounded-lg">
                <p className="text-sm text-gray-600 mb-2">Column Types</p>
                <div className="flex flex-wrap gap-2">
                  <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                    {basic_stats?.numeric_columns?.length || 0} Numeric
                  </span>
                  <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded">
                    {basic_stats?.categorical_columns?.length || 0} Categorical
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Data Quality */}
        <div className="border border-gray-200 rounded-lg overflow-hidden">
          <SectionHeader 
            title="Data Quality" 
            icon={CheckCircle} 
            section="quality"
          />
          
          {expandedSections.quality && (
            <div className="p-4 bg-gray-50 space-y-3">
              <div className="bg-white p-3 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <p className="text-sm text-gray-600">Completeness</p>
                  <span className={`px-2 py-1 text-xs rounded ${
                    getQualityColor((data_quality?.completeness || 0) * 100)
                  }`}>
                    {((data_quality?.completeness || 0) * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-600 h-2 rounded-full" 
                    style={{ width: `${(data_quality?.completeness || 0) * 100}%` }}
                  ></div>
                </div>
              </div>
              
              <div className="bg-white p-3 rounded-lg">
                <p className="text-sm text-gray-600">Duplicate Rows</p>
                <p className="text-lg font-semibold text-gray-900">
                  {data_quality?.duplicate_rows || 0}
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Patterns */}
        {patterns && patterns.length > 0 && (
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <SectionHeader 
              title="Detected Patterns" 
              icon={BarChart3} 
              section="patterns"
              count={patterns.length}
            />
            
            {expandedSections.patterns && (
              <div className="p-4 bg-gray-50 space-y-2">
                {patterns.map((pattern, index) => (
                  <div key={index} className="bg-white p-3 rounded-lg flex items-start space-x-3">
                    <Info className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-700">{pattern}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Recommendations */}
        {recommendations && recommendations.length > 0 && (
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <SectionHeader 
              title="Recommendations" 
              icon={AlertTriangle} 
              section="recommendations"
              count={recommendations.length}
            />
            
            {expandedSections.recommendations && (
              <div className="p-4 bg-gray-50 space-y-2">
                {recommendations.map((recommendation, index) => (
                  <div key={index} className="bg-white p-3 rounded-lg flex items-start space-x-3">
                    <AlertTriangle className="h-4 w-4 text-yellow-600 mt-0.5 flex-shrink-0" />
                    <p className="text-sm text-gray-700">{recommendation}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default InsightsPanel;