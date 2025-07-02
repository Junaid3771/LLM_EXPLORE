import React from 'react';
import { BarChart3, Brain } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg">
              <Brain className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">DataInsight AI</h1>
              <p className="text-sm text-gray-500">Intelligent Data Analysis</p>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            <div className="flex items-center space-x-2 text-gray-600">
              <BarChart3 className="h-4 w-4" />
              <span className="text-sm">Powered by AI</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;