from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

INDEX_HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Laboratorio 4 - Docker</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background: linear-gradient(135deg, #1e3a8a 0%, #0ea5e9 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      color: #1f2937;
    }
    .card {
      background: #ffffff;
      border-radius: 16px;
      padding: 40px;
      max-width: 480px;
      width: 100%;
      box-shadow: 0 20px 50px rgba(0,0,0,0.25);
    }
    h1 {
      font-size: 28px;
      color: #1e3a8a;
      margin-bottom: 8px;
    }
    .subtitle {
      color: #6b7280;
      font-size: 14px;
      margin-bottom: 28px;
    }
    .badge {
      display: inline-block;
      background: #dbeafe;
      color: #1e3a8a;
      font-size: 12px;
      font-weight: 600;
      padding: 4px 10px;
      border-radius: 999px;
      margin-bottom: 20px;
    }
    form {
      display: flex;
      flex-direction: column;
      gap: 12px;
      margin-bottom: 20px;
    }
    label {
      font-size: 13px;
      font-weight: 600;
      color: #374151;
    }
    input[type=number] {
      padding: 12px 14px;
      border: 2px solid #e5e7eb;
      border-radius: 8px;
      font-size: 16px;
      transition: border-color 0.2s;
    }
    input[type=number]:focus {
      outline: none;
      border-color: #0ea5e9;
    }
    button {
      background: #0ea5e9;
      color: white;
      border: none;
      padding: 12px;
      border-radius: 8px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.2s;
    }
    button:hover { background: #0284c7; }
    .result {
      margin-top: 20px;
      padding: 18px;
      background: #f0fdf4;
      border-left: 4px solid #10b981;
      border-radius: 8px;
      display: none;
    }
    .result.show { display: block; }
    .result .label { font-size: 13px; color: #065f46; margin-bottom: 4px; }
    .result .value { font-size: 28px; font-weight: 700; color: #064e3b; }
    .error {
      margin-top: 20px;
      padding: 14px;
      background: #fef2f2;
      border-left: 4px solid #ef4444;
      border-radius: 8px;
      color: #991b1b;
      font-size: 14px;
      display: none;
    }
    .error.show { display: block; }
    .endpoints {
      margin-top: 28px;
      padding-top: 20px;
      border-top: 1px solid #e5e7eb;
      font-size: 12px;
      color: #6b7280;
    }
    .endpoints code {
      background: #f3f4f6;
      padding: 2px 6px;
      border-radius: 4px;
      font-family: "SF Mono", Monaco, monospace;
    }
  </style>
</head>
<body>
  <div class="card">
    <span class="badge">Docker Container</span>
    <h1>Hola desde Docker</h1>
    <p class="subtitle">Laboratorio 4 — Cloud Computing UdeA</p>

    <form id="sumarForm">
      <div>
        <label for="a">Número A</label>
        <input type="number" id="a" name="a" step="any" required value="10">
      </div>
      <div>
        <label for="b">Número B</label>
        <input type="number" id="b" name="b" step="any" required value="25">
      </div>
      <button type="submit">Calcular suma</button>
    </form>

    <div class="result" id="result">
      <div class="label">Resultado</div>
      <div class="value" id="resultValue">0</div>
    </div>

    <div class="error" id="error"></div>

    <div class="endpoints">
      <p><strong>Endpoints disponibles:</strong></p>
      <p><code>GET /sumar?a=&lt;n&gt;&amp;b=&lt;n&gt;</code> — operación (JSON)</p>
      <p><code>GET /health</code> — healthcheck</p>
    </div>
  </div>

  <script>
    const form = document.getElementById('sumarForm');
    const result = document.getElementById('result');
    const resultValue = document.getElementById('resultValue');
    const error = document.getElementById('error');

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const a = document.getElementById('a').value;
      const b = document.getElementById('b').value;

      result.classList.remove('show');
      error.classList.remove('show');

      try {
        const res = await fetch(`/sumar?a=${encodeURIComponent(a)}&b=${encodeURIComponent(b)}`);
        const data = await res.json();
        if (!res.ok) throw new Error(data.error || 'Error desconocido');
        resultValue.textContent = data.resultado;
        result.classList.add('show');
      } catch (err) {
        error.textContent = err.message;
        error.classList.add('show');
      }
    });
  </script>
</body>
</html>
"""


@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML)


@app.route("/sumar", methods=["GET"])
def sumar():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
    except (TypeError, ValueError):
        return jsonify({
            "error": "Los parametros 'a' y 'b' deben ser numericos"
        }), 400

    resultado = a + b
    return jsonify({
        "operacion": "suma",
        "a": a,
        "b": b,
        "resultado": resultado
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)