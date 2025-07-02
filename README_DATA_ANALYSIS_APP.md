# DataInsight AI - Intelligent Data Analysis Agent

A modern, AI-powered data analysis application that allows users to upload Excel/CSV files and ask natural language questions about their data. The application features a beautiful React frontend and a powerful Python backend with intelligent data analysis capabilities.

## Features

### 🤖 AI-Powered Analysis
- Natural language query processing
- Automatic insights generation
- Pattern detection and recommendations
- Smart pandas code generation

### 🎨 Modern UI/UX
- Beautiful, responsive design with Tailwind CSS
- Drag-and-drop file upload
- Real-time chat interface
- Interactive insights panel
- Code syntax highlighting

### 📊 Data Processing
- Support for Excel (.xlsx, .xls) and CSV files
- Comprehensive data quality assessment
- Statistical analysis and correlations
- Missing data detection
- Outlier identification

### 💬 Conversational Interface
- Ask questions in natural language
- Get explanations with generated code
- Follow-up questions support
- Example question suggestions

## Technology Stack

### Frontend
- **React 18** - Modern UI framework
- **Tailwind CSS** - Utility-first styling
- **Lucide React** - Beautiful icons
- **Axios** - HTTP client
- **React Dropzone** - File upload handling

### Backend
- **FastAPI** - High-performance API framework
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **OpenPyXL/XlsxWriter** - Excel file handling
- **Uvicorn** - ASGI server

## Quick Start

### Prerequisites
- Python 3.8+ 
- Node.js 16+
- npm or yarn

### 1. Clone and Setup Backend

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the backend server
python main.py
```

The backend will start on `http://localhost:8000`

### 2. Setup Frontend

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will start on `http://localhost:3000`

## Usage Guide

### 1. Upload Your Data
- Drag and drop your Excel (.xlsx, .xls) or CSV file
- The AI will automatically analyze your data and generate insights
- View the initial analysis in the insights panel

### 2. Ask Questions
Use natural language to query your data:

**Basic Statistics:**
- "What are the average values in my dataset?"
- "Show me the maximum and minimum values"
- "How many rows are in my data?"

**Data Quality:**
- "Are there any missing values?"
- "How many duplicate rows do I have?"
- "What's the data quality score?"

**Analysis:**
- "Show me correlations between columns"
- "What patterns do you see in the data?"
- "Give me a statistical summary"

**Custom Queries:**
- "Which column has the highest variance?"
- "What are the unique values in each column?"

### 3. View Results
- Get instant answers with explanations
- See the generated pandas code
- Copy code snippets for your own use
- Ask follow-up questions for deeper analysis

## API Endpoints

### POST /upload
Upload and analyze a data file
- **Input:** Multipart form data with file
- **Output:** Dataset ID and initial insights

### POST /query
Query the uploaded dataset
- **Input:** `{"dataset_id": "string", "question": "string"}`
- **Output:** Answer, generated code, and explanation

### GET /datasets
List all uploaded datasets

### DELETE /datasets/{dataset_id}
Delete a specific dataset

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html       # HTML template
│   ├── src/
│   │   ├── components/      # React components
│   │   │   ├── Header.js
│   │   │   ├── FileUpload.js
│   │   │   ├── ChatInterface.js
│   │   │   ├── InsightsPanel.js
│   │   │   └── CodeBlock.js
│   │   ├── services/
│   │   │   └── api.js        # API service
│   │   ├── App.js           # Main React component
│   │   ├── index.js         # React entry point
│   │   └── index.css        # Global styles
│   ├── package.json         # Node dependencies
│   ├── tailwind.config.js   # Tailwind configuration
│   └── postcss.config.js    # PostCSS configuration
└── README_DATA_ANALYSIS_APP.md
```

## Key Features Explained

### 🧠 AI Agent Intelligence
The DataAnalysisAgent class provides:
- **Pattern Detection:** Identifies correlations, trends, and outliers
- **Code Generation:** Creates pandas code based on natural language queries
- **Smart Explanations:** Provides context and insights for results
- **Data Quality Assessment:** Evaluates completeness, duplicates, and data types

### 🎨 Beautiful UI Components
- **FileUpload:** Drag-and-drop with visual feedback and loading states
- **ChatInterface:** WhatsApp-style messaging with code blocks and examples
- **InsightsPanel:** Collapsible sections with data quality metrics
- **CodeBlock:** Syntax-highlighted code with copy functionality

### 🔒 Security Features
- Safe code execution environment
- File type validation
- Error handling and user feedback
- CORS configuration for frontend-backend communication

## Customization

### Adding New Question Types
Edit the `_generate_pandas_code` method in `main.py`:

```python
elif 'your_keyword' in question_lower:
    return "your_pandas_code"
```

### Styling Changes
Modify `tailwind.config.js` for custom colors and themes:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom color palette
      }
    }
  }
}
```

### Adding New Insights
Extend the `analyze_dataset` method to include additional analysis:

```python
def analyze_dataset(self, df):
    insights = {
        # ... existing insights
        "custom_analysis": self._your_custom_analysis(df)
    }
    return insights
```

## Troubleshooting

### Common Issues

**Backend not starting:**
- Ensure Python 3.8+ is installed
- Check virtual environment activation
- Verify all dependencies are installed

**Frontend not loading:**
- Ensure Node.js 16+ is installed
- Clear npm cache: `npm cache clean --force`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`

**File upload errors:**
- Check file format (only .xlsx, .xls, .csv supported)
- Ensure file size is reasonable (< 100MB recommended)
- Check backend logs for specific error messages

**CORS errors:**
- Verify backend is running on port 8000
- Check CORS configuration in `main.py`
- Ensure frontend is accessing correct backend URL

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the API documentation
3. Open an issue on GitHub
4. Check the console logs for error details

---

**Happy Data Analysis! 🚀📊**