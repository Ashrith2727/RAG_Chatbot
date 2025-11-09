import os
import json
from datetime import datetime


LOGS_DIR = "logs"

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


def create_log_entry(user_query, docs, bot_response, agent_type="tutor"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    log_filename = f"{timestamp}.json"
    log_path = os.path.join(LOGS_DIR, log_filename)
    
    chunks_info = []
    sources_info = []
    
    for idx, doc in enumerate(docs):
        chunk_data = {
            "chunk_id": idx,
            "source": doc.metadata.get("source", "Unknown Source"),
            "page": doc.metadata.get("page", "N/A"),
            "content_preview": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content,
            "content_length": len(doc.page_content)
        }
        chunks_info.append(chunk_data)
        
        source = doc.metadata.get("source", "Unknown Source")
        if source not in sources_info:
            sources_info.append(source)
    
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "agent_type": agent_type,
        "user_query": user_query,
        "retrieval_info": {
            "total_chunks_retrieved": len(docs),
            "sources": sources_info,
            "chunks": chunks_info
        },
        "llm_info": {
            "context_sent": len(docs),
            "total_context_length": sum(len(d.page_content) for d in docs),
            "response_length": len(bot_response)
        },
        "bot_response_preview": bot_response[:500] + "..." if len(bot_response) > 500 else bot_response
    }
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)
    
    print(f"Log created: {log_filename}")
    return log_path
