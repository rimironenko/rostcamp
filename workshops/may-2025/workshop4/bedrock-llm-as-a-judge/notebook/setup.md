# Setuv Virtual Env for local Jupyter

```bash
# Create virtual environment
python -m venv myenv

# Activate it (Windows)
myenv\Scripts\activate

# Activate it (macOS/Linux)
source myenv/bin/activate

# Install jupyter and ipykernel
pip install jupyter ipykernel

# Install the kernel for Jupyter
python -m ipykernel install --user --name=myenv --display-name="Python (myenv)"

# Start Jupyter
jupyter notebook
```