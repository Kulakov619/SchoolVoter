from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os


ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

app = Flask(__name__)

def load_data():
    try:
        with open('names_to_keys.json', 'r', encoding='utf-32') as f:
            names_to_keys = json.load(f)
        
        with open('keys.json', 'r', encoding='utf-8') as f:
            keys_data = json.load(f)
        
        return names_to_keys, keys_data
    except FileNotFoundError as e:
        print(f"Ошибка загрузки файла: {e}")
        return {}, {}
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return {}, {}

# def load_password():
#     try:
#         with open('password.txt', 'r', encoding='utf-8') as f:
#             return f.read().strip()
#     except FileNotFoundError:
#         return ""

def load_parties():
    try:
        with open('parties.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_results():
    try:
        with open('results.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_results(results):
    try:
        with open('results.json', 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка сохранения результатов: {e}")
        return False

def set_key_voted(key):
    try:
        with open('keys.json', 'r', encoding='utf-8') as f:
            keys_data = json.load(f)
        
        keys_data[key] = True
        
        with open('keys.json', 'w', encoding='utf-8') as f:
            json.dump(keys_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Ошибка обновления ключа: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_vote', methods=['POST'])
def check_vote():
    try:
        full_name = request.form.get('full_name', '').strip()
        
        if not full_name:
            return render_template('index.html', error='Пожалуйста, введите ФИО')
        
        names_to_keys, keys_data = load_data()
        
        if full_name in names_to_keys:
            key = names_to_keys[full_name]
            
            if key in keys_data:
                voted = keys_data[key]
                result = "ДА" if voted else "НЕТ"
                status = "voted" if voted else "not_voted"
                
                return render_template('index.html', 
                                     full_name=full_name, 
                                     result=result, 
                                     status=status)
            else:
                return render_template('index.html', 
                                     error=f'Ключ для {full_name} не найден в базе голосования')
        else:
            return render_template('index.html', 
                                 error=f'ФИО "{full_name}" не найдено в базе данных')
    
    except Exception as e:
        return render_template('index.html', error=f'Произошла ошибка: {str(e)}')

@app.route('/api/parties', methods=['GET'])
def get_parties():
    parties = load_parties()
    return jsonify(parties)

@app.route('/api/vote', methods=['POST'])
def vote():
    try:
        data = request.get_json()
        full_name = data.get('full_name', '').strip()
        party_id = data.get('party_id', '').strip()
        admin_password = data.get('admin_password', '').strip()
        
        if not full_name or not party_id or not admin_password:
            return jsonify({'success': False, 'message': 'Недостаточно данных'})
        
        correct_password = ADMIN_PASSWORD
        if admin_password != correct_password:
            return jsonify({'success': False, 'message': 'Неверный admin пароль'})
        
        names_to_keys, keys_data = load_data()
        
        if full_name not in names_to_keys:
            return jsonify({'success': False, 'message': 'ФИО не найдено в базе данных'})
        
        key = names_to_keys[full_name]
        
        if key in keys_data and keys_data[key]:
            return jsonify({'success': False, 'message': 'Этот человек уже голосовал'})
        
        results = load_results()
        results[party_id] = results.get(party_id, 0) + 1
        save_results(results)
        
        set_key_voted(key)
        
        return jsonify({'success': True, 'message': 'Голос успешно засчитан'})
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Ошибка: {str(e)}'})

if __name__ == '__main__':
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "unsafe-dev-key")
    app.run(debug=False, host='0.0.0.0', port=5000)
