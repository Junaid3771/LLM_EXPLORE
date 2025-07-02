from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import numpy as np
import io
import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel
import uuid
from datetime import datetime
import openai
from pathlib import Path

app = FastAPI(title="Data Analysis Agent", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for uploaded datasets
datasets = {}

class QueryRequest(BaseModel):
    dataset_id: str
    question: str

class Dataset:
    def __init__(self, df: pd.DataFrame, filename: str):
        self.df = df
        self.filename = filename
        self.uploaded_at = datetime.now()
        self.id = str(uuid.uuid4())

class DataAnalysisAgent:
    """AI Agent for analyzing data and generating insights"""
    
    def __init__(self):
        # Initialize with basic analysis capabilities
        pass
    
    def analyze_dataset(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Generate initial insights about the dataset"""
        insights = {
            "basic_stats": self._get_basic_stats(df),
            "data_quality": self._assess_data_quality(df),
            "patterns": self._detect_patterns(df),
            "recommendations": self._generate_recommendations(df)
        }
        return insights
    
    def _get_basic_stats(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Get basic statistics about the dataset"""
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        stats = {
            "shape": df.shape,
            "columns": df.columns.tolist(),
            "numeric_columns": numeric_cols,
            "categorical_columns": categorical_cols,
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict()
        }
        
        if numeric_cols:
            stats["numeric_summary"] = df[numeric_cols].describe().to_dict()
        
        return stats
    
    def _assess_data_quality(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Assess data quality issues"""
        total_cells = df.shape[0] * df.shape[1]
        missing_cells = df.isnull().sum().sum()
        
        quality = {
            "completeness": 1 - (missing_cells / total_cells),
            "missing_percentage": (missing_cells / total_cells) * 100,
            "duplicate_rows": df.duplicated().sum(),
            "unique_values_per_column": {col: df[col].nunique() for col in df.columns}
        }
        
        return quality
    
    def _detect_patterns(self, df: pd.DataFrame) -> List[str]:
        """Detect interesting patterns in the data"""
        patterns = []
        
        # Check for correlations in numeric data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()
            high_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    if abs(corr_matrix.iloc[i, j]) > 0.7:
                        high_corr.append(f"{corr_matrix.columns[i]} and {corr_matrix.columns[j]} (correlation: {corr_matrix.iloc[i, j]:.2f})")
            
            if high_corr:
                patterns.append(f"Strong correlations found: {', '.join(high_corr)}")
        
        # Check for trends in time-based data
        date_cols = df.select_dtypes(include=['datetime64']).columns
        if len(date_cols) > 0:
            patterns.append(f"Time-based data detected in columns: {', '.join(date_cols)}")
        
        # Check for outliers
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)]
            if len(outliers) > 0:
                patterns.append(f"Outliers detected in {col}: {len(outliers)} values")
        
        return patterns
    
    def _generate_recommendations(self, df: pd.DataFrame) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Missing data recommendations
        missing_pct = (df.isnull().sum() / len(df)) * 100
        high_missing = missing_pct[missing_pct > 20]
        if len(high_missing) > 0:
            recommendations.append(f"Consider handling missing data in: {', '.join(high_missing.index)}")
        
        # Data type recommendations
        for col in df.columns:
            if df[col].dtype == 'object':
                try:
                    pd.to_numeric(df[col])
                    recommendations.append(f"Column '{col}' might be converted to numeric type")
                except:
                    pass
        
        # Performance recommendations
        if df.shape[0] > 100000:
            recommendations.append("Large dataset detected - consider data sampling for faster analysis")
        
        return recommendations
    
    def answer_question(self, df: pd.DataFrame, question: str) -> Dict[str, Any]:
        """Answer user questions about the data"""
        question_lower = question.lower()
        
        # Generate pandas code based on question
        code = self._generate_pandas_code(df, question)
        
        try:
            # Execute the code safely
            result = self._execute_code(df, code)
            
            # Generate explanation
            explanation = self._explain_result(question, result, df)
            
            return {
                "answer": result,
                "code": code,
                "explanation": explanation,
                "success": True
            }
        except Exception as e:
            return {
                "answer": f"Error executing analysis: {str(e)}",
                "code": code,
                "explanation": "Could not execute the analysis due to an error.",
                "success": False
            }
    
    def _generate_pandas_code(self, df: pd.DataFrame, question: str) -> str:
        """Generate pandas code based on the question"""
        question_lower = question.lower()
        
        # Simple pattern matching for common questions
        if any(word in question_lower for word in ['mean', 'average']):
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                return f"df[{numeric_cols.tolist()}].mean()"
        
        elif any(word in question_lower for word in ['max', 'maximum', 'highest']):
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                return f"df[{numeric_cols.tolist()}].max()"
        
        elif any(word in question_lower for word in ['min', 'minimum', 'lowest']):
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 0:
                return f"df[{numeric_cols.tolist()}].min()"
        
        elif any(word in question_lower for word in ['count', 'how many']):
            return "df.shape[0]"
        
        elif any(word in question_lower for word in ['correlation', 'corr']):
            return "df.corr()"
        
        elif any(word in question_lower for word in ['describe', 'summary', 'statistics']):
            return "df.describe()"
        
        elif any(word in question_lower for word in ['null', 'missing', 'nan']):
            return "df.isnull().sum()"
        
        elif any(word in question_lower for word in ['unique', 'distinct']):
            return "df.nunique()"
        
        else:
            return "df.describe()"
    
    def _execute_code(self, df: pd.DataFrame, code: str) -> Any:
        """Safely execute pandas code"""
        # Create a safe environment
        safe_dict = {'df': df, 'pd': pd, 'np': np}
        
        try:
            result = eval(code, {"__builtins__": {}}, safe_dict)
            
            # Convert result to JSON-serializable format
            if isinstance(result, pd.DataFrame):
                return result.to_dict('records')
            elif isinstance(result, pd.Series):
                return result.to_dict()
            elif isinstance(result, np.ndarray):
                return result.tolist()
            else:
                return result
        except Exception as e:
            raise e
    
    def _explain_result(self, question: str, result: Any, df: pd.DataFrame) -> str:
        """Generate explanation for the result"""
        explanations = {
            'mean': "This shows the average values for numeric columns in your dataset.",
            'max': "These are the maximum values found in each numeric column.",
            'min': "These are the minimum values found in each numeric column.",
            'count': f"Your dataset contains {result} rows of data.",
            'correlation': "This correlation matrix shows how strongly different variables are related to each other.",
            'describe': "This statistical summary provides key metrics like mean, standard deviation, and quartiles.",
            'missing': "This shows the count of missing values in each column.",
            'unique': "This shows the number of unique values in each column."
        }
        
        question_lower = question.lower()
        for key, explanation in explanations.items():
            if key in question_lower:
                return explanation
        
        return "Here's the result of your data analysis query."

# Initialize the agent
agent = DataAnalysisAgent()

@app.get("/")
async def root():
    return {"message": "Data Analysis Agent API"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Upload and process Excel file"""
    if not file.filename.endswith(('.xlsx', '.xls', '.csv')):
        raise HTTPException(status_code=400, detail="Only Excel (.xlsx, .xls) and CSV files are supported")
    
    try:
        contents = await file.read()
        
        # Read the file based on extension
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        else:
            df = pd.read_excel(io.BytesIO(contents))
        
        # Create dataset object
        dataset = Dataset(df, file.filename)
        datasets[dataset.id] = dataset
        
        # Generate initial insights
        insights = agent.analyze_dataset(df)
        
        return {
            "dataset_id": dataset.id,
            "filename": file.filename,
            "insights": insights,
            "message": "File uploaded and analyzed successfully"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/query")
async def query_data(request: QueryRequest):
    """Answer questions about the uploaded dataset"""
    if request.dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    dataset = datasets[request.dataset_id]
    result = agent.answer_question(dataset.df, request.question)
    
    return result

@app.get("/datasets")
async def list_datasets():
    """List all uploaded datasets"""
    return {
        "datasets": [
            {
                "id": dataset.id,
                "filename": dataset.filename,
                "uploaded_at": dataset.uploaded_at.isoformat(),
                "shape": dataset.df.shape
            }
            for dataset in datasets.values()
        ]
    }

@app.delete("/datasets/{dataset_id}")
async def delete_dataset(dataset_id: str):
    """Delete a dataset"""
    if dataset_id not in datasets:
        raise HTTPException(status_code=404, detail="Dataset not found")
    
    del datasets[dataset_id]
    return {"message": "Dataset deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)