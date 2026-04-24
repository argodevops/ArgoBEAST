
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt* . 
RUN pip install --no-cache-dir argobeast     && if [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; fi
RUN useradd -m argouser
USER argouser
ENV PS1="[argobeast lab]: "     IS_IN_LAB=True 
