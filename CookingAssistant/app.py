from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from rag_system import RAGSystem
from recipe_filter import filter_recipes, get_filter_options
import os

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

rag_system = None


def init_rag():
    global rag_system
    rag_system = RAGSystem()
    if rag_system.load_vectorstore():
        rag_system.setup_qa_chain()
        print('RAG系统初始化成功')
        return True
    else:
        print('向量数据库不存在，请先运行 build_kb.py')
        return False


@app.route('/')
def index():
    return send_from_directory('static', 'index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    if not rag_system:
        return jsonify({'error': 'RAG系统未初始化'}), 500

    data = request.json
    question = data.get('question', '')

    if not question:
        return jsonify({'error': '问题不能为空'}), 400

    try:
        result = rag_system.query(question)
        return jsonify({
            'success': True,
            'answer': result['answer'],
            'sources': result['sources']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/filter-options', methods=['GET'])
def filter_options():
    try:
        options = get_filter_options()
        return jsonify({
            'success': True,
            'data': options
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/filter', methods=['POST'])
def filter():
    data = request.json or {}

    try:
        results = filter_recipes(
            category=data.get('category'),
            difficulty=data.get('difficulty'),
            property_type=data.get('property'),
            taste=data.get('taste') or data.get('tastes'),
            max_time=data.get('max_time'),
            ingredients=data.get('ingredients'),
            seasonings=data.get('seasonings'),
            utensils=data.get('utensils'),
            difficulties=data.get('difficulties'),
            keyword=data.get('keyword'),
            limit=data.get('limit', 20)
        )

        formatted_results = []
        for r in results:
            formatted_results.append({
                'id': r.get('id'),
                'title': r.get('title'),
                'category': r.get('category'),
                'difficulty': r.get('difficulty'),
                'time': r.get('time'),
                'property': r.get('property'),
                'taste': r.get('taste'),
                'ingredients': r.get('ingredients', [])[:5],
                'ingredient_count': len(r.get('ingredients', [])),
                'steps': r.get('steps', []),
                'tips': r.get('tips'),
                'suitable_for': r.get('suitable_for')
            })

        return jsonify({
            'success': True,
            'total': len(results),
            'results': formatted_results
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def status():
    if rag_system and rag_system.collection:
        return jsonify({
            'success': True,
            'status': 'ready'
        })
    return jsonify({
        'success': False,
        'status': 'not_initialized'
    })


if __name__ == '__main__':
    print('正在启动服务...')
    if init_rag():
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        print('请先运行 build_kb.py 构建知识库')
