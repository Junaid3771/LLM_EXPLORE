import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileSpreadsheet, Loader2 } from 'lucide-react';

const FileUpload = ({ onFileUpload, loading }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onFileUpload(acceptedFiles[0]);
    }
  }, [onFileUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv']
    },
    multiple: false,
    disabled: loading
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          relative border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 cursor-pointer
          ${isDragActive 
            ? 'border-blue-400 bg-blue-50 scale-105' 
            : 'border-gray-300 hover:border-blue-300 hover:bg-gray-50'
          }
          ${loading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          {loading ? (
            <>
              <div className="p-4 bg-blue-100 rounded-full">
                <Loader2 className="h-8 w-8 text-blue-600 animate-spin" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  Processing your file...
                </h3>
                <p className="text-gray-600">
                  Analyzing data and generating insights
                </p>
              </div>
            </>
          ) : (
            <>
              <div className={`p-4 rounded-full transition-colors ${
                isDragActive ? 'bg-blue-100' : 'bg-gray-100'
              }`}>
                {isDragActive ? (
                  <Upload className="h-8 w-8 text-blue-600" />
                ) : (
                  <FileSpreadsheet className="h-8 w-8 text-gray-600" />
                )}
              </div>
              
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">
                  {isDragActive ? 'Drop your file here' : 'Upload your data file'}
                </h3>
                <p className="text-gray-600 mb-4">
                  Drag and drop your Excel (.xlsx, .xls) or CSV file here, or click to browse
                </p>
                <div className="inline-flex items-center space-x-2 text-sm text-gray-500">
                  <span>Supported formats:</span>
                  <span className="px-2 py-1 bg-gray-100 rounded text-xs font-medium">.xlsx</span>
                  <span className="px-2 py-1 bg-gray-100 rounded text-xs font-medium">.xls</span>
                  <span className="px-2 py-1 bg-gray-100 rounded text-xs font-medium">.csv</span>
                </div>
              </div>
            </>
          )}
        </div>
        
        {/* Decorative elements */}
        <div className="absolute top-4 right-4 w-20 h-20 bg-gradient-to-br from-blue-100 to-purple-100 rounded-full opacity-50 -z-10"></div>
        <div className="absolute bottom-4 left-4 w-16 h-16 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full opacity-50 -z-10"></div>
      </div>
      
      <div className="mt-6 text-center">
        <p className="text-sm text-gray-500">
          Your data is processed locally and securely. We respect your privacy.
        </p>
      </div>
    </div>
  );
};

export default FileUpload;