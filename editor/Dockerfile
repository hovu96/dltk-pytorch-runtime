FROM pytorch/pytorch:1.0-cuda10.0-cudnn7-runtime
ENV INSTALL_PATH /src
ENV NOTEBOOK_PATH /notebooks
RUN mkdir -p $INSTALL_PATH
WORKDIR $INSTALL_PATH
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/ ./
EXPOSE 8888
WORKDIR $NOTEBOOK_PATH
ENTRYPOINT python $INSTALL_PATH/app.py
