# Windows Setup Guide for DataInsight AI

## 🖥️ Windows Requirements

Before starting, ensure you have:
- **Python 3.8+** - [Download from python.org](https://www.python.org/downloads/)
- **Node.js 16+** - [Download from nodejs.org](https://nodejs.org/)
- **Git** (if cloning from repository)

## 🚀 Quick Setup (Automated)

### Option 1: One-Click Setup
```powershell
# Run the setup script
.\setup_windows.bat
```

This will automatically:
- Set up Python virtual environment
- Install backend dependencies
- Install frontend dependencies
- Provide instructions for starting the application

## 📋 Manual Setup (Step by Step)

### Step 1: Setup Backend
```powershell
# Open PowerShell in project directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Setup Frontend
```powershell
# Open NEW PowerShell window
cd frontend

# Install Node.js dependencies
npm install
```

## 🏃‍♂️ Running the Application

### Start Backend (Terminal 1)
```powershell
# Option A: Use batch file
.\start_backend.bat

# Option B: Manual commands
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

### Start Frontend (Terminal 2)
```powershell
# Option A: Use batch file
.\start_frontend.bat

# Option B: Manual commands
cd frontend
npm start
```

## 🌐 Access the Application

Once both servers are running:
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🔧 Troubleshooting

### Python Issues
```powershell
# Check Python version
python --version

# If 'python' doesn't work, try:
python3 --version
py --version
```

### Node.js Issues
```powershell
# Check Node.js version
node --version
npm --version

# Clear npm cache if needed
npm cache clean --force
```

### PowerShell Execution Policy
If you get execution policy errors:
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use
If ports 3000 or 8000 are busy:
```powershell
# Find and kill processes using the port
netstat -ano | findstr :3000
netstat -ano | findstr :8000

# Kill process by PID
taskkill /PID <PID_NUMBER> /F
```

## 📁 Project Structure
```
cursor_agent_test/
├── backend/              # FastAPI backend
│   ├── main.py          # Main application
│   ├── requirements.txt # Python dependencies
│   └── venv/           # Virtual environment (created)
├── frontend/            # React frontend
│   ├── src/            # Source code
│   ├── package.json    # Node dependencies
│   └── node_modules/   # Dependencies (created)
├── sample_data/        # Sample CSV files
├── setup_windows.bat   # Windows setup script
├── start_backend.bat   # Start backend
└── start_frontend.bat  # Start frontend
```

## 🎯 Usage

1. **Upload File**: Drag & drop Excel/CSV files
2. **Get Insights**: View automatic analysis
3. **Ask Questions**: Chat with the AI about your data
4. **View Code**: See generated pandas code
5. **Follow Up**: Ask "why did this happen?" questions

## 🆘 Still Having Issues?

1. Check the error messages in both terminals
2. Ensure Python and Node.js are properly installed
3. Try running commands manually step by step
4. Check Windows Defender/firewall settings
5. Run PowerShell as Administrator if needed