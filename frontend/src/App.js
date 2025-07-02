import React, { useState, useEffect } from 'react';
import './index.css';
import FileUpload from './components/FileUpload';
import ChatInterface from './components/ChatInterface';
import InsightsPanel from './components/InsightsPanel';
import Header from './components/Header';
import { api } from './services/api';

function App() {
  const [currentDataset, setCurrentDataset] = useState(null);
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await api.uploadFile(file);
      setCurrentDataset({
        id: result.dataset_id,
        filename: result.filename
      });
      setInsights(result.insights);
    } catch (err) {
      setError(err.message || 'Failed to upload file');
    } finally {
      setLoading(false);
    }
  };

  const handleNewDataset = () => {
    setCurrentDataset(null);
    setInsights(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <Header />
      
      <main className="container mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-700 font-medium">Error: {error}</p>
          </div>
        )}

        {!currentDataset ? (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                AI Data Analysis Agent
              </h1>
              <p className="text-xl text-gray-600 mb-8">
                Upload your Excel file and start asking questions about your data
              </p>
            </div>
            
            <FileUpload onFileUpload={handleFileUpload} loading={loading} />
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Main Chat Interface */}
            <div className="lg:col-span-2">
              <ChatInterface 
                datasetId={currentDataset.id}
                filename={currentDataset.filename}
                onNewDataset={handleNewDataset}
              />
            </div>
            
            {/* Insights Panel */}
            <div className="lg:col-span-1">
              <InsightsPanel insights={insights} />
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;