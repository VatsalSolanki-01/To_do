from flask import Flask, request, redirect, url_for, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "notes.db"

# --- Create DB if it doesn't exist ---
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute('''CREATE TABLE notes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        content TEXT NOT NULL
                    )''')
        conn.commit()
        conn.close()

# --- HTML Template (Phone UI) ---
TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Notes</title>
<style>
  :root {
    --bg: #0b0b0c;
    --panel: #141416;
    --panel-2: #1b1c1f;
    --text: #f5f5f7;
    --muted: #b8b8bd;
    --accent: #ff9f0a;
    --accent-press: #ff8a00;
    --border: #2a2a2e;
    --shadow: 0 10px 30px rgba(0,0,0,0.35);
    --radius-xl: 18px;
    --radius: 12px;
  }

  * { box-sizing: border-box; }
  html, body { height: 100%; margin:0; }
  body {
    display: flex;
    justify-content: center;
    align-items: center;
    background: radial-gradient(1200px 800px at 80% -10%, rgba(255,159,10,0.08), transparent 60%),
                radial-gradient(1200px 800px at -10% 90%, rgba(255,159,10,0.06), transparent 60%),
                var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", Roboto, "Segoe UI", sans-serif;
  }

  /* Phone frame styling */
  .phone-frame {
    width: 375px; /* phone width */
    height: 700px; /* phone height */
    background: var(--bg);
    border: 10px solid #222;
    border-radius: 36px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.6);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    position: relative;
  }

  /* Notch */
  .notch {
    width: 150px;
    height: 30px;
    background: #222;
    border-radius: 0 0 20px 20px;
    margin: 0 auto;
    position: absolute;
    top: -1px;
    left: 50%;
    transform: translateX(-50%);
  }

  .app-content { flex: 1; overflow-y: auto; }

  /* Top bar */
  .appbar{
    position: sticky; top:0; z-index: 20;
    backdrop-filter: blur(12px);
    background: linear-gradient(180deg, rgba(10,10,10,0.75), rgba(10,10,10,0.35) 90%, transparent);
    border-bottom: 1px solid var(--border);
    padding: 18px 20px 14px;
  }
  .brand{ display:flex; align-items:center; gap:12px; }
  .dot{ width: 12px; height: 12px; border-radius: 50%; background: var(--accent); }
  .title{ font-size: 22px; font-weight: 700; }

  .container{ margin: 24px auto; padding: 0 20px 40px; }

  .composer{
    background: linear-gradient(180deg, var(--panel), var(--panel-2));
    border: 1px solid var(--border);
    border-radius: var(--radius-xl);
    box-shadow: var(--shadow);
    padding: 16px;
  }

  textarea{
    width: 100%;
    min-height: 110px;
    resize: vertical;
    border: 1px solid var(--border);
    background: #0f1012;
    color: var(--text);
    border-radius: 14px;
    padding: 14px;
    font-size: 15px;
  }
  textarea::placeholder{ color: #8f8f95; }
  .actions{ display:flex; justify-content:flex-end; margin-top: 12px; }
  button{
    border: none; cursor: pointer;
    background: var(--accent);
    color: #0a0a0a; font-weight: 700;
    padding: 10px 16px; border-radius: 999px;
    box-shadow: 0 6px 18px rgba(255,159,10,0.25);
  }

  .list{ margin-top: 22px; display: grid; gap: 12px; }
  .note{
    background: linear-gradient(180deg, #111214, #0e0f12);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 14px;
    white-space: pre-wrap;
  }
  .section-title{ margin: 26px 6px 10px; color: var(--muted); font-size: 12px; text-transform: uppercase; }
</style>
</head>
<body>
  <div class="phone-frame">
    <div class="notch"></div>
    <div class="app-content">
      <header class="appbar">
        <div class="brand">
          <span class="dot"></span>
          <div class="title">Notes</div>
        </div>
      </header>

      <main class="container">
        <section class="composer">
          <div class="label">New Note</div>
          <form method="POST" action="{{ url_for('add_note') }}">
            <textarea name="content" placeholder="Write your note…" required></textarea>
            <div class="actions">
              <button type="submit">Add Note</button>
            </div>
          </form>
        </section>

        <div class="section-title">Saved</div>
        <section class="list">
          {% for note in notes %}
            <div class="note">{{ note[1] }}</div>
          {% else %}
            <div class="note" style="opacity:.7">No notes yet. Add your first one ✍️</div>
          {% endfor %}
        </section>
      </main>
    </div>
  </div>
</body>
</html>
"""

# --- Routes ---
@app.route('/')
def index():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM notes ORDER BY id DESC")
    notes = c.fetchall()
    conn.close()
    return render_template_string(TEMPLATE, notes=notes)

@app.route('/add', methods=['POST'])
def add_note():
    content = request.form['content']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO notes (content) VALUES (?)", (content,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)