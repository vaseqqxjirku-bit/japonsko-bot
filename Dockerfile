FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir discord.py PyNaCl
CMD ["python", "radio_bot.py"]
