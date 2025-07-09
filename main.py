from flask import Flask, request, redirect, jsonify
import requests

app = Flask(__name__)

# Ваши данные Patreon (замените на свои реальные значения)
CLIENT_ID = "CYjKuyuvNwbTpcfWT_JG6URhBCLzV4BI0CPtk0yufB6BBx6jKajTMNe-epagISdF"  # Скопируйте из Patreon Developer Portal
CLIENT_SECRET = "m0REieElPE8AhTjRLNPmkiTduQd6Kna2GfMz6ITJ3w9M2HFdK2yTeta62-ampyKP"  # Скопируйте из Patreon Developer Portal
REDIRECT_URI = "http://localhost:5000/auth"  # Это адрес, куда Patreon отправит код после авторизации

# Главная страница сервера (для тестов)
@app.route('/')
def home():
    return "Сервер работает! Используй игру для авторизации."

# Запуск процесса авторизации
@app.route('/start_auth')
def start_auth():
    # Ссылка, которая отправит игрока на страницу входа Patreon
    auth_url = (
        f"https://www.patreon.com/oauth2/authorize?"
        f"response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    )
    return jsonify({"auth_url": auth_url})

# Обработка ответа от Patreon после авторизации
@app.route('/auth')
def auth():
    code = request.args.get('code')
    print(f"Received code: {code}")
    if not code:
        return jsonify({"error": "Код авторизации не получен"}), 400

    token_url = "https://www.patreon.com/api/oauth2/token"
    data = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI
    }
    print(f"Sending token request with data: {data}")
    response = requests.post(token_url, data=data)
    print(f"Token response: {response.text}")
    token_data = response.json()

    if "access_token" not in token_data:
        return jsonify(token_data), 400

    access_token = token_data["access_token"]
    user_url = (
        "https://www.patreon.com/api/oauth2/v2/identity?"
        "include=memberships&fields[user]=full_name&"
        "fields[member]=patron_status,currently_entitled_amount_cents,pledge_relationship_start"
    )
    headers = {"Authorization": f"Bearer {access_token}"}
    user_response = requests.get(user_url, headers=headers)
    user_data = user_response.json()
    print(f"User data: {user_data}")

    is_patron = False
    is_follower = False
    is_former_patron = False
    pledge_amount = 0
    tier = "none"

    if "included" in user_data and len(user_data["included"]) > 0:
        for item in user_data["included"]:
            if item["type"] == "member":
                patron_status = item["attributes"].get("patron_status")
                currently_entitled_amount_cents = item["attributes"].get("currently_entitled_amount_cents")
                print(f"Processing member: patron_status={patron_status}, currently_entitled_amount_cents={currently_entitled_amount_cents}")
                if patron_status == "active_patron" and currently_entitled_amount_cents is not None:
                    if currently_entitled_amount_cents > 0:
                        is_patron = True
                        pledge_amount = currently_entitled_amount_cents
                        if pledge_amount >= 1000:
                            tier = "high_tier"
                        elif pledge_amount >= 500:
                            tier = "mid_tier"
                        elif pledge_amount > 0:
                            tier = "low_tier"
                    elif currently_entitled_amount_cents == 0:
                        is_follower = True
                # Исправление: если patron_status null и сумма 0, это бесплатный подписчик
                elif patron_status is None and currently_entitled_amount_cents == 0:
                    is_follower = True
                elif patron_status in ["declined_patron", "former_patron"]:
                    is_former_patron = True
                    pledge_amount = 0 if currently_entitled_amount_cents is None else currently_entitled_amount_cents
                break

    global last_result
    last_result = {
        "is_patron": is_patron,
        "is_follower": is_follower,
        "is_former_patron": is_former_patron,
        "pledge_amount": pledge_amount,
        "tier": tier
    }
    print(f"Saved last_result: {last_result}")

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Авторизация завершена</title>
        <script type="text/javascript">
            setTimeout(function() {
                window.close();
            }, 1000);
        </script>
    </head>
    <body>
        <p>Success!.</p>
    </body>
    </html>
    """

@app.route('/get_status')
def get_status():
    if 'last_result' not in globals():
        return jsonify({"error": "Сначала нужно авторизоваться через Patreon"}), 400
    return jsonify(last_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
