from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
import chromadb
from config import Config


class RAGSystem:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len
        )
        self.vectorstore = None
        self.collection = None
        self.qa_chain = None
        self.client = None

    def prepare_documents(self, recipes):
        documents = []

        for recipe in recipes:
            ingredients_str = ', '.join(recipe.get('ingredients', []))
            seasonings_str = ', '.join(recipe.get('seasonings', []))
            steps_str = '\n'.join([f"{i+1}. {step}" for i, step in enumerate(recipe.get('steps', []))])

            content = f"""
菜名：{recipe.get('title', '')}
分类：{recipe.get('category', '')}
难度：{recipe.get('difficulty', '')}
烹饪时间：{recipe.get('time', '')}
食物属性：{recipe.get('property', '')}（{recipe.get('taste', '')}）
适合场景：{recipe.get('suitable_for', '')}

【食材】（{len(recipe.get('ingredients', []))}种）
{ingredients_str}

【调料】
{seasonings_str}

【做法】
{steps_str}

小贴士：{recipe.get('tips', '')}
营养价值：{recipe.get('nutrition', '')}
"""
            doc = Document(
                page_content=content,
                metadata={
                    'id': recipe.get('id', 0),
                    'title': recipe.get('title', ''),
                    'category': recipe.get('category', ''),
                    'difficulty': recipe.get('difficulty', ''),
                    'time': recipe.get('time', ''),
                    'property': recipe.get('property', ''),
                    'taste': recipe.get('taste', ''),
                    'ingredient_count': len(recipe.get('ingredients', []))
                }
            )
            documents.append(doc)

        return self.text_splitter.split_documents(documents)

    def build_vectorstore(self, split_docs):
        self.client = chromadb.PersistentClient(path=Config.CHROMA_DB_PATH)

        try:
            self.client.delete_collection(name="cooking")
        except:
            pass

        self.collection = self.client.create_collection(name="cooking")

        texts = [doc.page_content for doc in split_docs]
        metadatas = [doc.metadata for doc in split_docs]
        ids = [f"doc_{i}" for i in range(len(split_docs))]

        self.collection.add(documents=texts, metadatas=metadatas, ids=ids)
        print(f"已构建向量数据库，包含 {len(texts)} 个文档片段")

    def load_vectorstore(self):
        try:
            self.client = chromadb.PersistentClient(path=Config.CHROMA_DB_PATH)
            self.collection = self.client.get_collection(name="cooking")
            return True
        except:
            return False

    def _retrieve_docs(self, question):
        results = self.collection.query(
            query_texts=[question],
            n_results=Config.TOP_K
        )

        docs = []
        if results and results['documents']:
            for doc, metadata in zip(results['documents'][0], results['metadatas'][0]):
                docs.append(f"【{metadata['title']}】({metadata['category']}, {metadata['property']})\n{doc}")

        return '\n\n'.join(docs) if docs else "未找到相关菜谱"

    def setup_qa_chain(self):
        llm = ChatOllama(
            model=Config.OLLAMA_MODEL,
            temperature=0.7,
            base_url=Config.OLLAMA_BASE_URL
        )

        prompt = ChatPromptTemplate.from_template("""你是一位专业的烹饪助手。请根据提供的菜谱信息回答用户的问题。

菜谱参考：
{context}

用户问题：{question}

请给出详细、实用的回答。如果用户询问具体菜谱，请包含：
- 菜名和分类
- 食材和调料（包含用量）
- 详细做法步骤
- 食物属性（凉/热）和口味
- 小贴士和烹饪技巧
""")

        self.qa_chain = (
            {"context": self._retrieve_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

    def query(self, question):
        if not self.qa_chain:
            return {'answer': 'RAG系统未初始化', 'sources': []}

        answer = self.qa_chain.invoke(question)

        results = self.collection.query(
            query_texts=[question],
            n_results=Config.TOP_K
        )

        sources = []
        if results and results['metadatas']:
            for metadata in results['metadatas'][0]:
                sources.append({
                    'id': metadata.get('id', 0),
                    'title': metadata.get('title', '未知'),
                    'category': metadata.get('category', '未知'),
                    'difficulty': metadata.get('difficulty', '未知'),
                    'time': metadata.get('time', '未知'),
                    'property': metadata.get('property', '未知'),
                    'taste': metadata.get('taste', '未知')
                })

        return {
            'answer': answer,
            'sources': sources
        }
