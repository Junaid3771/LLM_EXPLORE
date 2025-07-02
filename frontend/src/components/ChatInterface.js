import React, { useState, useRef, useEffect } from 'react';
import { Send, User, Bot, Code, Upload, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import CodeBlock from './CodeBlock';

const ChatInterface = ({ datasetId, filename, onNewDataset }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content: `Great! I've analyzed your file "${filename}". You can now ask me questions about your data. Here are some examples:`,
      examples: [
        "What are the average values in my dataset?",
        "Show me the correlation between columns",
        "What are the maximum and minimum values?",
        "How many rows are in my dataset?",
        "Are there any missing values?"
      ],
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await api.queryData(datasetId, inputValue);
      
      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.explanation,
        answer: response.answer,
        code: response.code,
        success: response.success,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Sorry, I encountered an error while processing your question. Please try again.',
        error: error.message,
        success: false,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleExampleClick = (example) => {
    setInputValue(example);
    inputRef.current?.focus();
  };

  const formatAnswer = (answer) => {
    if (typeof answer === 'object') {
      if (Array.isArray(answer)) {
        return JSON.stringify(answer.slice(0, 5), null, 2) + (answer.length > 5 ? '\n... and more' : '');
      }
      return JSON.stringify(answer, null, 2);
    }
    return String(answer);
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg h-[700px] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-100 rounded-lg">
            <Bot className="h-5 w-5 text-blue-600" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">AI Assistant</h3>
            <p className="text-sm text-gray-500">Analyzing: {filename}</p>
          </div>
        </div>
        
        <button
          onClick={onNewDataset}
          className="flex items-center space-x-2 px-3 py-2 text-sm bg-gray-100 hover:bg-gray-200 rounded-lg transition-colors"
        >
          <Upload className="h-4 w-4" />
          <span>New File</span>
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 custom-scrollbar">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`chat-message flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`max-w-[80%] rounded-2xl p-4 ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}
            >
              {/* Avatar */}
              <div className="flex items-start space-x-3">
                <div className={`p-2 rounded-full ${
                  message.type === 'user' ? 'bg-blue-500' : 'bg-white'
                }`}>
                  {message.type === 'user' ? (
                    <User className="h-4 w-4 text-white" />
                  ) : (
                    <Bot className="h-4 w-4 text-blue-600" />
                  )}
                </div>
                
                <div className="flex-1">
                  {/* Content */}
                  <p className="mb-2">{message.content}</p>
                  
                  {/* Examples */}
                  {message.examples && (
                    <div className="space-y-2">
                      {message.examples.map((example, index) => (
                        <button
                          key={index}
                          onClick={() => handleExampleClick(example)}
                          className="block w-full text-left p-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg text-sm transition-all"
                        >
                          "{example}"
                        </button>
                      ))}
                    </div>
                  )}
                  
                  {/* Answer */}
                  {message.answer && (
                    <div className="mt-3 p-3 bg-white bg-opacity-20 rounded-lg">
                      <h4 className="font-medium mb-2 flex items-center">
                        <Code className="h-4 w-4 mr-2" />
                        Result:
                      </h4>
                      <pre className="text-sm overflow-x-auto">
                        {formatAnswer(message.answer)}
                      </pre>
                    </div>
                  )}
                  
                  {/* Code */}
                  {message.code && (
                    <div className="mt-3">
                      <CodeBlock code={message.code} language="python" />
                    </div>
                  )}
                  
                  {/* Error */}
                  {message.error && (
                    <div className="mt-3 p-3 bg-red-100 border border-red-200 rounded-lg">
                      <p className="text-red-700 text-sm">{message.error}</p>
                    </div>
                  )}
                  
                  {/* Timestamp */}
                  <p className="text-xs opacity-60 mt-2">
                    {message.timestamp.toLocaleTimeString()}
                  </p>
                </div>
              </div>
            </div>
          </div>
        ))}
        
        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl p-4 max-w-[80%]">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-white rounded-full">
                  <Bot className="h-4 w-4 text-blue-600" />
                </div>
                <div className="flex items-center space-x-2">
                  <Loader2 className="h-4 w-4 animate-spin text-blue-600" />
                  <span className="text-sm text-gray-600">Analyzing your question...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <div className="border-t border-gray-200 p-4">
        <div className="flex space-x-3">
          <input
            ref={inputRef}
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask a question about your data..."
            className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isLoading}
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputValue.trim() || isLoading}
            className="px-6 py-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;