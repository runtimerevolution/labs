# RAG Architecture

## Challenges

1. Context embeddings creation

    * how are embeddings created? which strategy was used?

2. Query + context

    * Ensure query + context reflect what's intended
    * provides an acceptable answer

3. Include the generated answer in the correct place in the project

## RAG General view

```mermaid
flowchart
    
    subgraph Prompt
        A[/Query/] --> B[Embedding model<br> <strong>text-embedding-ada-002</strong>]
        B --> C[Embeddings]
    end
    subgraph Context
        E[/Data source/] --> F[Embedding model<br> <strong>text-embedding-ada-002</strong>]
        F --> G[Embeddings]
    end
    subgraph Vector Database
        C --> D[(<strong>PostgreSQL PGVector</strong>)]
        G --> D
    end
    subgraph LLM
        A --> H[/Query + Context/]
        D --> H
        H --> I[OpenAPI o1]
        I --> J[/Response/]
    end
```

## Integrations

```mermaid
flowchart
    subgraph CodeMonkey
        API
    end

    subgraph Local
        C[Repository]
    end

    subgraph Github
        D[Repository]
        Issues
        App
    end

    Github <--> CodeMonkey
    Local <--> CodeMonkey
```

## Embeddings and LLM

| Embeddings | LLM |
| --- | --- |
| text-embedding-ada-002 | OpenAPI o1 | 
| text-embedding-ada-002 | Llama 3.2 (local) | 
