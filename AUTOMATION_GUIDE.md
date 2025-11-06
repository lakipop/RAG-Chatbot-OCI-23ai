# Automation Scripts for OCI RAG Project

This folder contains several batch (.bat) files to automate common tasks. These scripts make it easy to set up and run the project without typing commands manually.

## 📋 Available Scripts

### 1. `setup.bat` - Initial Setup (Run Once)
**When to use**: First time setting up the project after cloning.

**What it does**:
- Creates Python virtual environment
- Installs all dependencies from requirements.txt
- Creates .env file from template

**Command**:
```powershell
setup.bat
```

**After running**: Edit the `.env` file with your credentials!

---

### 2. `run_ingestion.bat` - Load Documents (Run Once)
**When to use**: After setup, or when you add new documents to `/data` folder.

**What it does**:
- Runs the ingestion script (ingest.py)
- Loads all documents from `/data` folder
- Stores them in Oracle 23ai Vector Database

**Command**:
```powershell
run_ingestion.bat
```

**Duration**: 30-60 seconds depending on document count.

---

### 3. `start_chatbot.bat` - Launch Chatbot (Run Anytime)
**When to use**: After ingestion is complete, whenever you want to use the chatbot.

**What it does**:
- Launches the Streamlit web application
- Opens in your default browser at http://localhost:8501
- Keeps running until you close it

**Command**:
```powershell
start_chatbot.bat
```

**To stop**: Press Ctrl+C or close the window.

---

### 4. `quick_start.bat` - Full Reset + Start (Run When Needed)
**When to use**: When you want to refresh the database with new documents and start the chatbot.

**What it does**:
- Runs ingestion (clears and reloads all documents)
- Automatically launches chatbot if ingestion succeeds

**Command**:
```powershell
quick_start.bat
```

**Warning**: This re-runs ingestion, which clears existing data!

---

### 5. `cleanup.bat` - Clean Installation (Run If Issues Occur)
**When to use**: If you encounter setup issues or want to start fresh.

**What it does**:
- Removes virtual environment (venv folder)
- Removes Python cache files
- Keeps your .env file and data folder safe

**Command**:
```powershell
cleanup.bat
```

**After running**: You'll need to run `setup.bat` again.

---

## 🚀 Quick Start Workflow

### First Time Setup:
```powershell
# Step 1: Run setup
setup.bat

# Step 2: Edit .env file with your credentials
notepad .env

# Step 3: Load documents
run_ingestion.bat

# Step 4: Start chatbot
start_chatbot.bat
```

### Daily Use:
```powershell
# Just start the chatbot
start_chatbot.bat
```

### After Adding New Documents:
```powershell
# Re-run ingestion, then start chatbot
quick_start.bat
```

---

## 🔧 Troubleshooting

### Issue: "Python is not installed or not in PATH"
**Solution**: Install Python 3.11+ from https://www.python.org/ and make sure to check "Add Python to PATH" during installation.

### Issue: Script shows "Access Denied" or won't run
**Solution**: 
1. Open PowerShell as Administrator
2. Run: `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
3. Try running the .bat file again

### Issue: "Virtual environment not found"
**Solution**: Run `setup.bat` first to create the environment.

### Issue: Ingestion fails with database error
**Solution**: 
1. Check your .env file credentials
2. Verify Oracle Database is accessible
3. Check your network/firewall settings

---

## 📁 What Each Script Does (Technical Details)

| Script | Creates venv? | Installs deps? | Runs ingestion? | Starts app? |
|--------|--------------|----------------|-----------------|-------------|
| `setup.bat` | ✅ | ✅ | ❌ | ❌ |
| `run_ingestion.bat` | ❌ | ❌ | ✅ | ❌ |
| `start_chatbot.bat` | ❌ | ❌ | ❌ | ✅ |
| `quick_start.bat` | ❌ | ❌ | ✅ | ✅ |
| `cleanup.bat` | ❌ (removes) | ❌ | ❌ | ❌ |

---

## 💡 Tips

1. **Keep the terminal window open**: When you run `start_chatbot.bat`, keep that window open. Closing it will stop the chatbot.

2. **Ingestion is one-time**: You only need to run ingestion once, or when you add new documents. The chatbot reads from the database, not the files.

3. **Use quick_start for demos**: If you're showing the project to someone, `quick_start.bat` ensures everything is fresh and ready.

4. **Safe cleanup**: `cleanup.bat` preserves your credentials (.env) and documents (data/), so you can safely clean and restart if needed.

---

## 🎯 Recommended Workflow

### Development:
```
setup.bat → Edit .env → run_ingestion.bat → start_chatbot.bat
```

### Daily Use:
```
start_chatbot.bat
```

### After Code Changes:
```
cleanup.bat → setup.bat → run_ingestion.bat → start_chatbot.bat
```

### Demo/Presentation:
```
quick_start.bat
```

---

**Last Updated**: November 2025
