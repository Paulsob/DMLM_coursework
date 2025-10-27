document.getElementById('predictBtnImg').onclick = async () => {
  const fileInput = document.getElementById('inputImg');
  if (!fileInput.files.length) {
    alert("Выберите изображение");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("type", "image");

  const resp = await fetch('http://127.0.0.1:5000/predict', {
    method: 'POST',
    body: formData
  });

  const data = await resp.json();
  document.getElementById('outputImg').innerText = `Результат: ${data.final_result}`;
};



document.getElementById('predictBtnMusic').onclick = async () => {
  const fileInput = document.getElementById('inputMusic');
  if (!fileInput.files.length) {
    alert("Выберите аудиофайл");
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);
  formData.append("type", "music");

  const resp = await fetch('http://127.0.0.1:5000/predict', {
    method: 'POST',
    body: formData
  });

  const data = await resp.json();
  document.getElementById('outputMusic').innerText = `Результат: ${data.final_result}`;
};



document.getElementById('predictBtnTxt').onclick = async () => {
  const text = document.getElementById('inputTxt').value.trim();
  if (!text) {
    alert("Выберите текст");
    return;
  }

  const resp = await fetch('http://127.0.0.1:5000/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text, type: 'text' })
  });

  const data = await resp.json();
  document.getElementById('outputTxt').innerText = `Результат: ${data.final_result}`;
};
