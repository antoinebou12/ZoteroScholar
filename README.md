# ZoteroScholar

Enhance your research workflow with ZoteroScholar, a tool that integrates Zotero's document management with the natural language processing capabilities of Ollama. Ideal for academics, researchers, and anyone looking to efficiently search through their collection of research documents.

![ZoteroScholar Screenshot](docs/image.png)

## Features

- **Easy Setup**: Requires only your Zotero User ID and API Key.
- **Document Synchronization**: Sync documents from your personal Zotero library or selected Zotero groups.
- **Document Querying**: Perform natural language queries on your document collection.
- **Docker Support**: Deploy easily using Docker and Docker Compose with GPU acceleration.

## Getting Started

### Prerequisites

- **Python 3.10+**
- **Pip**
- **Docker & Docker Compose**: [Install Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- **Docker Runtime** (for GPU support):
- **Zotero Account**: Obtain your Zotero User ID and API Key:
  - **User ID**: Found in your Zotero profile URL.
  - **API Key**: Generate in Zotero [Settings](https://www.zotero.org/settings) under 'Feeds/API'.

### Installation

#### Method 1: Using Python

1. **Clone the Repository**
    ```bash
    git clone https://github.com/coconutcow/zotero-scholar.git
    cd zotero-scholar
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Up Ollama LLM**
    - Install [Ollama](https://ollama.com/).
    - Pull the 7b chat model:
      ```bash
      ollama pull 7b-chat
      ```

4. **Run the Application**
    ```bash
    streamlit run run.py
    ```
    Access the app at `http://localhost:8501`.

#### Method 2: Using Docker

1. **Build and Run with Docker Compose**
    ```bash
    docker-compose up --build
    ```
    Access the app at `http://localhost:8501`.

## Directory Structure

```
zotero-scholar/
├── Dockerfile
├── docker-compose.yml
├── README.md
├── requirements.txt
├── run.py
├── utils/
│   ├── __init__.py
│   ├── pdf_loader.py
│   ├── query_processor.py
│   ├── text_processor.py
│   └── zotero_downloader.py
├── data/
│   └── zotero_papers/ (created after syncing)
└── docs/
    └── image.png
```

## Usage

1. **Sync Documents**
   - Enter your Zotero User ID and API Key.
   - Choose your library source (Personal or Groups).
   - Click "Sync Documents" to download your documents.

2. **Query Documents**
   - Enter your query in the text area.
   - Click "Get Answer" to retrieve relevant information from your collection.

## Contributing

Contributions are welcome! Fork the repository, make your changes, and submit a pull request.

## License

ZoteroScholar is licensed under the [MIT License](LICENSE).
