from JsonDecorator import *
import logging
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
    handlers=[
        logging.FileHandler("log.txt", encoding="utf-8"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("logger")

db = load_from_json("keys.json")
res = load_from_json("results.json")
parties_data = load_from_json("parties.json")

def set_key_already_used(key: str):
    db[key] = True
    logger.info(f"{key} voted")
    save_to_json(db, "keys.json")


def add_results(num: str):
    res[num] = res.get(num, 0) + 1
    logger.info(f"{num} has been chosen")
    save_to_json(res, "results.json")


@app.route('/api/is_key_used', methods=['GET'])
def is_key_used():
    key = str(request.headers.get("key"))

    if key not in db:
        return "not_in_database"
    else:
        is_used = db.get(key)

        if is_used:
            return "already_used"
        else:
            return "new_key"


@app.route('/api/vote', methods=['POST'])
def vote():
    num = str(request.headers.get("number"))
    key = str(request.headers.get("key"))

    if key not in db:
        return "not_in_database"
    else:
        is_used = db.get(key)

        if is_used:
            return "already_used"
        else:
            set_key_already_used(key)
            add_results(num)
            return "ok"


@app.route('/api/parties', methods=['GET'])
def get_parties():
    from flask import jsonify
    return jsonify(parties_data)


@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Система Голосования</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                padding: 20px;
            }
            
            .container {
                max-width: 800px;
                margin: 0 auto;
                background: rgba(255, 255, 255, 0.95);
                border-radius: 20px;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
                padding: 40px;
                backdrop-filter: blur(10px);
            }
            
            .header {
                text-align: center;
                margin-bottom: 40px;
            }
            
            .header-content {
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 20px;
                margin-bottom: 10px;
            }
            
            .header-icon {
                height: 60px;
                width: auto;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            
            .header h1 {
                color: #333;
                font-size: 2.5em;
                margin: 0;
                background: linear-gradient(135deg, #667eea, #764ba2);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            .header p {
                color: #666;
                font-size: 1.1em;
            }
            
            .form-section {
                margin-bottom: 40px;
            }
            
            .form-group {
                margin-bottom: 25px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #333;
                font-size: 1.1em;
            }
            
            input[type="text"] {
                width: 100%;
                padding: 15px 20px;
                border: 2px solid #e1e5e9;
                border-radius: 12px;
                font-size: 1em;
                transition: all 0.3s ease;
                background: #f8f9fa;
            }
            
            input[type="text"]:focus {
                outline: none;
                border-color: #667eea;
                background: white;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            
            .parties-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            
            .party-card {
                border: 2px solid #e1e5e9;
                border-radius: 16px;
                padding: 20px;
                cursor: pointer;
                transition: all 0.3s ease;
                background: white;
                position: relative;
                overflow: hidden;
            }
            
            .party-card::before {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                height: 4px;
                transition: all 0.3s ease;
            }
            
            .party-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
            }
            
            .party-card.selected {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
            }
            
            .party-card.selected::before {
                background: linear-gradient(135deg, #667eea, #764ba2);
            }
            
            .party-header {
                display: flex;
                align-items: center;
                margin-bottom: 15px;
            }
            
            .party-icon {
                font-size: 2em;
                margin-right: 15px;
            }
            
            .party-name {
                font-weight: bold;
                font-size: 1.2em;
                color: #333;
            }
            
            .party-description {
                color: #666;
                line-height: 1.6;
                font-size: 0.95em;
            }
            
            .submit-btn {
                width: 100%;
                padding: 18px;
                background: linear-gradient(135deg, #667eea, #764ba2);
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 1.2em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .submit-btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
            }
            
            .submit-btn:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: none;
                box-shadow: none;
            }
            
            .result {
                margin-top: 30px;
                padding: 20px;
                border-radius: 12px;
                font-weight: 600;
                text-align: center;
                font-size: 1.1em;
                transition: all 0.3s ease;
                display: none;
            }
            
            .result.success {
                background: linear-gradient(135deg, #4CAF50, #45a049);
                color: white;
                display: block;
            }
            
            .result.error {
                background: linear-gradient(135deg, #f44336, #d32f2f);
                color: white;
                display: block;
            }
            
            .hidden {
                display: none !important;
            }
            
            @media (max-width: 768px) {
                .container {
                    padding: 20px;
                    margin: 10px;
                }
                
                .header-content {
                    flex-direction: column;
                    gap: 15px;
                }
                
                .header-icon {
                    height: 50px;
                }
                
                .header h1 {
                    font-size: 2em;
                }
                
                .parties-grid {
                    grid-template-columns: 1fr;
                }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="header-content">
                    <img src="/static/vibori_icon.png" alt="Иконка голосования" class="header-icon">
                    <h1>Система Голосования</h1>
                </div>
                <p>Выберите партию, которая лучше всего представляет ваши интересы</p>
            </div>
            
            <form id="voteForm">
                <div class="form-section">
                    <div class="form-group">
                        <label for="key">🔑 Ваш уникальный ключ:</label>
                        <input type="text" id="key" name="key" placeholder="Введите ваш ключ для голосования" required>
                    </div>
                </div>
                
                <div class="form-section">
                    <label>🏛️ Выберите партию:</label>
                    <div class="parties-grid" id="partiesGrid">
                        <!-- Партии будут загружены динамически -->
                    </div>
                </div>
                
                <button type="submit" class="submit-btn" id="submitBtn" disabled>
                    ✨ Проголосовать
                </button>
            </form>
            
            <div class="result" id="result"></div>
        </div>
        
        <script>
            let parties = {};
            let selectedParty = null;
            
            // Загрузка данных о партиях
            async function loadParties() {
                try {
                    const response = await fetch('/api/parties');
                    parties = await response.json();
                    renderParties();
                } catch (error) {
                    console.error('Ошибка загрузки партий:', error);
                    // Fallback данные
                    parties = {
                        "1": {"name": "Партия Прогресса", "description": "Технологическое развитие и инновации", "color": "#4CAF50", "icon": "🚀"},
                        "2": {"name": "Союз Справедливости", "description": "Социальная справедливость и равенство", "color": "#2196F3", "icon": "⚖️"},
                        "3": {"name": "Консервативная Партия", "description": "Традиционные ценности и стабильность", "color": "#FF9800", "icon": "🏛️"}
                    };
                    renderParties();
                }
            }
            
            function renderParties() {
                const grid = document.getElementById('partiesGrid');
                grid.innerHTML = '';
                
                Object.entries(parties).forEach(([id, party]) => {
                    const card = document.createElement('div');
                    card.className = 'party-card';
                    card.dataset.partyId = id;
                    
                    card.innerHTML = `
                        <div class="party-header">
                            <span class="party-icon">${party.icon}</span>
                            <span class="party-name">${party.name}</span>
                        </div>
                        <div class="party-description">${party.description}</div>
                    `;
                    
                    // Добавляем стиль для цвета партии
                    if (party.color) {
                        card.style.setProperty('--party-color', party.color);
                        card.addEventListener('mouseenter', () => {
                            card.style.borderColor = party.color;
                        });
                        card.addEventListener('mouseleave', () => {
                            if (!card.classList.contains('selected')) {
                                card.style.borderColor = '#e1e5e9';
                            }
                        });
                    }
                    
                    card.addEventListener('click', () => selectParty(id, card));
                    grid.appendChild(card);
                });
            }
            
            function selectParty(partyId, cardElement) {
                // Убираем выделение с предыдущей карточки
                document.querySelectorAll('.party-card').forEach(card => {
                    card.classList.remove('selected');
                    card.style.borderColor = '#e1e5e9';
                });
                
                // Выделяем новую карточку
                cardElement.classList.add('selected');
                if (parties[partyId].color) {
                    cardElement.style.borderColor = parties[partyId].color;
                }
                
                selectedParty = partyId;
                document.getElementById('submitBtn').disabled = false;
            }
            
            function showResult(message, isError = false) {
                const result = document.getElementById('result');
                result.textContent = message;
                result.className = `result ${isError ? 'error' : 'success'}`;
                result.style.display = 'block';
            }
            
            function hideResult() {
                const result = document.getElementById('result');
                result.style.display = 'none';
            }
            
            document.getElementById('voteForm').addEventListener('submit', async function(e) {
                e.preventDefault();
                hideResult();
                
                const key = document.getElementById('key').value.trim();
                const submitBtn = document.getElementById('submitBtn');
                
                if (!selectedParty) {
                    showResult('Пожалуйста, выберите партию для голосования', true);
                    return;
                }
                
                submitBtn.disabled = true;
                submitBtn.textContent = '⏳ Обработка...';
                
                try {
                    // Проверяем ключ
                    let resp = await fetch('/api/is_key_used', {
                        method: 'GET',
                        headers: { 'key': key }
                    });
                    let status = await resp.text();

                    if (status === "not_in_database") {
                        showResult("❌ Ключ не найден в базе данных", true);
                        return;
                    }
                    if (status === "already_used") {
                        showResult("⚠️ Этот ключ уже использован для голосования", true);
                        return;
                    }

                    // Отправляем голос
                    resp = await fetch('/api/vote', {
                        method: 'POST',
                        headers: { 'key': key, 'number': selectedParty }
                    });
                    status = await resp.text();

                    if (status === "ok") {
                        showResult("✅ Спасибо за ваш голос! Ваш выбор учтен.", false);
                        // Очищаем форму
                        document.getElementById('key').value = '';
                        document.querySelectorAll('.party-card').forEach(card => {
                            card.classList.remove('selected');
                            card.style.borderColor = '#e1e5e9';
                        });
                        selectedParty = null;
                        submitBtn.disabled = true;
                    } else if (status === "already_used") {
                        showResult("⚠️ Этот ключ уже использован для голосования", true);
                    } else if (status === "not_in_database") {
                        showResult("❌ Ключ не найден в базе данных", true);
                    } else {
                        showResult("❌ Произошла ошибка. Попробуйте еще раз", true);
                    }
                } catch (error) {
                    showResult("❌ Ошибка соединения. Проверьте интернет", true);
                } finally {
                    submitBtn.disabled = false;
                    submitBtn.textContent = '✨ Проголосовать';
                }
            });
            
            // Загружаем партии при загрузке страницы
            loadParties();
        </script>
    </body>
    </html>
    """


if __name__ == '__main__':
    app.run(debug=True)
