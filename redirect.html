<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Patreon Auth Redirect</title>
</head>
<body>
  <h2>Проверка Patreon...</h2>
  <p>Пожалуйста, подождите. Идёт проверка вашей подписки...</p>
  <p id="result">⏳</p>

  <script>
    // Получаем access_token из URL после #access_token=...
    const hash = window.location.hash;
    const params = new URLSearchParams(hash.substr(1));
    const token = params.get('access_token');

    const resultEl = document.getElementById("result");

    if (!token) {
      resultEl.innerText = "❌ Токен не найден. Возможно, вы не авторизовались.";
    } else {
      // Делаем запрос к API Patreon
      fetch("https://www.patreon.com/api/oauth2/v2/identity?include=memberships.currently_entitled_tiers&fields[member]=patron_status,currently_entitled_tiers", {
        headers: {
          "Authorization": `Bearer ${token}`
        }
      })
      .then(response => response.json())
      .then(data => {
        resultEl.innerText = "✅ Подписка проверена! Сохраняем файл...";

        const jsonStr = JSON.stringify(data, null, 2);

        // Создаём файл и инициируем загрузку
        const blob = new Blob([jsonStr], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const link = document.createElement("a");

        link.href = url;
        link.download = "patreon_status.json";
        link.click();

        resultEl.innerHTML += "<br><strong>Скачайте файл и поместите его в папку с игрой.</strong>";
      })
      .catch(error => {
        resultEl.innerText = "❌ Ошибка при запросе к Patreon API: " + error.message;
      });
    }
  </script>
</body>
</html>
