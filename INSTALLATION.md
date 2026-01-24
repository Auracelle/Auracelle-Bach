# Installation Guide - Auracelle Bach

This guide provides detailed installation instructions for different deployment scenarios.

## 📋 Prerequisites

- **Python**: 3.8 or higher
- **pip**: Latest version recommended
- **Git**: For repository cloning
- **Internet connection**: For API integrations

## 🚀 Quick Start Options

### Option 1: Google Colab (Easiest)

Perfect for quick testing and demos without local setup.

1. Open the notebook in Colab:
   - Click the "Open in Colab" badge in README
   - Or visit: `https://colab.research.google.com/github/YOUR_USERNAME/auracelle-bach/blob/main/CHIA_PERFECT_01_17_25_AURACELLE_BACH_3_D_BEHAVIOR_AND_COGNITIVE_INTEGRATED.ipynb`

2. Run all cells:
   - Click **Runtime → Run all**
   - Wait for dependencies to install (~2-3 minutes)

3. Access the application:
   - An ngrok URL will be generated automatically
   - Click the URL to open Auracelle Bach interface

**Advantages**:
- No local installation required
- Free GPU access (if needed)
- Easy sharing with collaborators

**Limitations**:
- Session timeout after inactivity
- Requires ngrok authentication for persistent URLs

### Option 2: Local Installation (Recommended for Development)

#### Step 1: Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/auracelle-bach.git
cd auracelle-bach
```

#### Step 2: Create Virtual Environment

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows**:
```cmd
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Run Application

```bash
streamlit run app.py
```

The application will open automatically in your default browser at `http://localhost:8501`

### Option 3: Docker Deployment (Coming Soon)

Docker support for containerized deployment is under development.

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# API Keys (Optional but recommended)
WORLD_BANK_API_KEY=your_key_here
OECD_API_KEY=your_key_here
PRIVACY_INTL_API_KEY=your_key_here

# Ngrok Configuration (for Colab)
NGROK_AUTH_TOKEN=your_ngrok_token

# Application Settings
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=true
```

### Ngrok Setup (for Public URLs)

1. Sign up at https://ngrok.com
2. Get your auth token from dashboard
3. Configure in Colab or locally:

```python
from pyngrok import conf
conf.get_default().auth_token = "your_token_here"
```

## 🧪 Verify Installation

Run this test script to verify everything is working:

```python
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import networkx as nx

print("✅ All core dependencies imported successfully!")
```

Or run the included test:
```bash
python -m pytest tests/test_installation.py
```

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem**: `ModuleNotFoundError: No module named 'streamlit'`

**Solution**:
```bash
pip install --upgrade -r requirements.txt
```

#### 2. Port Already in Use

**Problem**: `Port 8501 is already in use`

**Solution**:
```bash
streamlit run app.py --server.port 8502
```

#### 3. API Connection Errors

**Problem**: API calls failing or timing out

**Solution**:
- Check internet connection
- Verify API keys are correctly set
- Check API rate limits
- Review firewall/proxy settings

#### 4. Memory Issues

**Problem**: Out of memory errors with large datasets

**Solution**:
- Use data sampling for initial testing
- Increase system memory allocation
- Consider cloud deployment (Colab, AWS, etc.)

#### 5. Streamlit White Screen

**Problem**: Streamlit loads but shows blank page

**Solution**:
```bash
# Clear Streamlit cache
streamlit cache clear

# Update Streamlit
pip install --upgrade streamlit
```

### Platform-Specific Issues

#### macOS
- If pip fails, ensure Xcode Command Line Tools are installed:
  ```bash
  xcode-select --install
  ```

#### Windows
- If you encounter SSL errors:
  ```bash
  pip install --upgrade certifi
  ```
  
- For path issues, use forward slashes or raw strings

#### Linux
- May need additional system packages:
  ```bash
  sudo apt-get update
  sudo apt-get install python3-dev build-essential
  ```

## 📦 Dependency Details

### Core Dependencies
- **streamlit**: Web application framework
- **pandas**: Data manipulation
- **numpy**: Numerical computing
- **scipy**: Scientific computing

### Visualization
- **plotly**: Interactive visualizations
- **matplotlib**: Static visualizations
- **seaborn**: Statistical graphics
- **pyvis**: Network visualizations

### Machine Learning
- **scikit-learn**: ML algorithms and tools

### Network Analysis
- **networkx**: Graph theory and network analysis

## 🔄 Updating

To update to the latest version:

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install --upgrade -r requirements.txt

# Clear cache
streamlit cache clear
```

## 🌐 Alternative Deployment Options

### Streamlit Cloud
1. Fork the repository
2. Sign up at https://streamlit.io/cloud
3. Connect your GitHub repository
4. Deploy with one click

### Heroku
```bash
# Add Procfile
echo "web: streamlit run app.py" > Procfile

# Deploy
heroku create auracelle-bach
git push heroku main
```

### AWS/GCP/Azure
Detailed cloud deployment guides available in `/docs/deployment/`

## 💻 Development Setup

For contributors:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/

# Check code style
flake8 .
black --check .
```

## 📊 Performance Optimization

For large-scale deployments:
- Enable Streamlit caching: Use `@st.cache_data` decorators
- Optimize data loading: Use chunking for large datasets
- Profile performance: `streamlit run app.py --server.runOnSave true`

## 🆘 Getting Help

If you encounter issues not covered here:

1. Check [GitHub Issues](https://github.com/YOUR_USERNAME/auracelle-bach/issues)
2. Review [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
3. Open a new issue with:
   - Python version: `python --version`
   - OS information
   - Error messages
   - Steps to reproduce

## 📞 Support

- **Email**: support@auracelle.org
- **GitHub Discussions**: For community support
- **Documentation**: Full docs at `/docs/`

---

**Successfully installed? Start with the [Quick Start Tutorial](docs/QUICKSTART.md)!**
