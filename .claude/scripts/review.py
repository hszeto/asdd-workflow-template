#!/usr/bin/env python3
"""Render ASDD spec/plan markdown as an interactive review page.

render <md>            write <md>.html next to the markdown
serve <html> [--once]  serve the page on localhost; saves answers to <stem>.answers.json
apply <md>             fold saved answers into the markdown, then re-render
"""

import argparse
import datetime
import html
import json
import re
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOST = "127.0.0.1"
DEFAULT_PORT = 8765
OPEN_QUESTIONS = "Open Questions"
MAX_ANSWER = 20000

CHECK_RE = re.compile(r"^(\s*)- \[( |x|X)\] (.*)$")
BULLET_RE = re.compile(r"^(\s*)- (.*)$")
ANSWER_RE = re.compile(r"^\s+- Answer:\s?(.*)$")
HEAD_RE = re.compile(r"^(#{1,3}) (.*)$")

CSS = """
body{font-family:-apple-system,system-ui,sans-serif;max-width:760px;margin:0 auto;
padding:24px 16px 96px;line-height:1.5;color:#1d1d1f;background:#fafafa}
h1{font-size:1.5rem} h2{font-size:1.15rem;border-bottom:1px solid #ddd;padding-bottom:4px;margin-top:28px}
ul{padding-left:20px} li{margin:4px 0} li.gate{list-style:none;margin-left:-20px}
label{cursor:pointer} input[type=checkbox]{transform:scale(1.2);margin-right:8px}
code{background:#ececec;padding:1px 4px;border-radius:4px}
pre{background:#f0f0f0;padding:12px;overflow-x:auto;border-radius:6px}
.q{margin:14px 0;padding:12px;background:#fff;border:1px solid #e3e3e3;border-radius:8px}
.q p{margin:0 0 8px;font-weight:600}
textarea{width:100%;box-sizing:border-box;font:inherit;padding:8px;border:1px solid #ccc;border-radius:6px;min-height:3em}
.bar{position:fixed;left:0;right:0;bottom:0;padding:12px 16px;background:#fff;border-top:1px solid #ddd}
.bar button{font:inherit;padding:10px 18px;border-radius:6px;border:0;background:#1d1d1f;color:#fff;cursor:pointer}
#status{margin-left:12px;color:#555}
"""

JS = """
document.getElementById('save').addEventListener('click', async () => {
  const questions = {}, gates = {};
  document.querySelectorAll('textarea[data-id]').forEach(t => questions[t.dataset.id] = t.value.trim());
  document.querySelectorAll('input[data-id]').forEach(c => gates[c.dataset.id] = c.checked);
  const statusEl = document.getElementById('status');
  statusEl.textContent = 'Saving...';
  try {
    const r = await fetch('/submit', {method: 'POST', headers: {'Content-Type': 'application/json'},
                                      body: JSON.stringify({questions, gates})});
    statusEl.textContent = r.ok ? 'Saved. Go back to Claude Code.' : 'Save failed (' + r.status + ').';
  } catch (e) {
    statusEl.textContent = 'Save failed. Is the review server still running?';
  }
});
"""


def inline(text):
    s = html.escape(text, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)


def parse(lines):
    """Return blocks in document order. Each block records its source line index."""
    blocks, section, in_code, code = [], None, False, []
    qn = gn = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            if in_code:
                blocks.append(("code", code))
                code = []
            in_code = not in_code
            i += 1
            continue
        if in_code:
            code.append(line)
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        if m := HEAD_RE.match(line):
            if len(m.group(1)) == 2:
                section = m.group(2).strip()
            blocks.append(("h", len(m.group(1)), m.group(2)))
            i += 1
            continue
        if m := CHECK_RE.match(line):
            gn += 1
            blocks.append(("gate", f"G{gn}", m.group(3), m.group(2).lower() == "x", i))
            i += 1
            continue
        if m := BULLET_RE.match(line):
            if not m.group(1) and section == OPEN_QUESTIONS:
                qn += 1
                ans_idx, answer = None, ""
                if i + 1 < len(lines) and (a := ANSWER_RE.match(lines[i + 1])):
                    ans_idx, answer = i + 1, a.group(1)
                blocks.append(("q", f"Q{qn}", m.group(2), answer, i, ans_idx))
                i = (ans_idx or i) + 1
                continue
            blocks.append(("li", m.group(2)))
            i += 1
            continue
        blocks.append(("p", line.strip()))
        i += 1
    return blocks


def render_page(md_text, title_fallback):
    blocks = parse(md_text.splitlines())
    title = next((b[2] for b in blocks if b[0] == "h" and b[1] == 1), title_fallback)
    out, in_ul = [], False

    def close_ul():
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    def open_ul():
        nonlocal in_ul
        if not in_ul:
            out.append("<ul>")
            in_ul = True

    for b in blocks:
        kind = b[0]
        if kind == "li":
            open_ul()
            out.append(f"<li>{inline(b[1])}</li>")
            continue
        if kind == "gate":
            open_ul()
            _, gid, text, checked, _ = b
            mark = " checked" if checked else ""
            out.append(
                f'<li class="gate"><label><input type="checkbox" data-id="{gid}"{mark}>'
                f"{inline(text)}</label></li>"
            )
            continue
        close_ul()
        if kind == "h":
            out.append(f"<h{b[1]}>{inline(b[2])}</h{b[1]}>")
        elif kind == "p":
            out.append(f"<p>{inline(b[1])}</p>")
        elif kind == "code":
            out.append(f"<pre><code>{html.escape(chr(10).join(b[1]))}</code></pre>")
        elif kind == "q":
            _, qid, text, answer, _, _ = b
            out.append(
                f'<div class="q"><p>{qid}. {inline(text)}</p>'
                f'<textarea data-id="{qid}" rows="2">{html.escape(answer)}</textarea></div>'
            )
    close_ul()

    body = "\n".join(out)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body>
{body}
<div class="bar"><button id="save">Save answers</button><span id="status"></span></div>
<script>{JS}</script>
</body></html>
"""


def cmd_render(md_path):
    md = Path(md_path)
    html_path = md.with_suffix(".html")
    html_path.write_text(render_page(md.read_text(), md.stem))
    print(html_path)
    return html_path


def answers_path(html_path):
    return html_path.with_suffix(".answers.json")


class ReviewHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path not in ("/", "/index.html"):
            self.send_error(404)
            return
        body = self.server.html_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/submit":
            self.send_error(404)
            return
        try:
            data = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            questions = {k: str(v)[:MAX_ANSWER] for k, v in data["questions"].items()
                         if re.fullmatch(r"Q\d+", k)}
            gates = {k: bool(v) for k, v in data["gates"].items() if re.fullmatch(r"G\d+", k)}
        except (KeyError, TypeError, ValueError):
            self.send_error(400)
            return
        payload = {
            "submitted_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "questions": questions,
            "gates": gates,
        }
        self.server.answers_path.write_text(json.dumps(payload, indent=2))
        body = b'{"ok": true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        print(f"Saved answers to {self.server.answers_path}", flush=True)
        if self.server.once:
            threading.Thread(target=self.server.shutdown, daemon=True).start()


def cmd_serve(html_arg, port, once):
    html_path = Path(html_arg).resolve()
    server = ThreadingHTTPServer((HOST, port), ReviewHandler)
    server.html_path = html_path
    server.answers_path = answers_path(html_path)
    server.once = once
    print(f"Review page: http://{HOST}:{port}/  (Ctrl-C to stop)", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def cmd_apply(md_arg):
    md = Path(md_arg)
    html_path = md.with_suffix(".html")
    ans_file = answers_path(html_path)
    saved = json.loads(ans_file.read_text())
    lines = md.read_text().splitlines()
    edits = []
    for b in parse(lines):
        if b[0] == "q":
            _, qid, _, _, idx, ans_idx = b
            if qid not in saved["questions"]:
                continue
            value = " ".join(saved["questions"][qid].split())
            if value:
                line = f"  - Answer: {value}"
                edits.append((ans_idx if ans_idx is not None else idx, "set", line, ans_idx is None))
            elif ans_idx is not None:
                edits.append((ans_idx, "delete", None, False))
        elif b[0] == "gate":
            _, gid, _, _, idx = b
            if gid in saved["gates"]:
                mark = "x" if saved["gates"][gid] else " "
                line = re.sub(r"\[( |x|X)\]", f"[{mark}]", lines[idx], count=1)
                edits.append((idx, "set", line, False))
    for idx, action, line, insert in sorted(edits, key=lambda e: e[0], reverse=True):
        if action == "delete":
            del lines[idx]
        elif insert:
            lines.insert(idx + 1, line)
        else:
            lines[idx] = line
    md.write_text("\n".join(lines) + "\n")
    ans_file.unlink()
    html_path.write_text(render_page("\n".join(lines) + "\n", md.stem))
    print(f"Updated {md} ({len(edits)} changes), re-rendered {html_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("render").add_argument("md")
    s = sub.add_parser("serve")
    s.add_argument("html")
    s.add_argument("--once", action="store_true", help="exit after the first save")
    s.add_argument("--port", type=int, default=DEFAULT_PORT)
    sub.add_parser("apply").add_argument("md")
    args = parser.parse_args()

    if args.cmd == "render":
        cmd_render(args.md)
    elif args.cmd == "serve":
        try:
            cmd_serve(args.html, args.port, args.once)
        except OSError as err:
            raise SystemExit(f"Could not start review server on port {args.port}: {err}")
    elif args.cmd == "apply":
        cmd_apply(args.md)


if __name__ == "__main__":
    main()
