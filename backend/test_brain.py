from sqlmodel import Session, create_engine, select, col, or_
from app.models import KnowledgeItem

engine = create_engine("sqlite:///./knowledge.db")

def search_brain_v2():
    print("\n🧠 BTEC Brain Interface v2 (Smart Search)")
    query = input("❓ Search (Content/Filename): ").strip()
    
    if not query: return

    with Session(engine) as session:
        statement = select(KnowledgeItem).where(
            or_(
                col(KnowledgeItem.content).contains(query),
                col(KnowledgeItem.source_file).contains(query)
            )
        ).limit(3)
        
        results = session.exec(statement).all()
        
        print(f"\n🔎 Found {len(results)} matches for '{query}':\n")
        
        if not results:
            print("❌ Still no matches. Try 'Business' or 'Unit'.")
        
        for i, item in enumerate(results, 1):
            # الإصلاح: معالجة النص في متغير منفصل أولاً
            raw_snippet = item.content[:200]
            clean_snippet = raw_snippet.replace('\n', ' ')
            
            print(f"--- 📄 Result {i} ---")
            print(f"📂 Source: {item.source_file}")
            print(f"🏷️  Folder: {item.metadata_info.get('folder', 'Unknown')}")
            print(f"📝 Text Snippet: {clean_snippet}...")
            print("-" * 50)

if __name__ == "__main__":
    search_brain_v2()
