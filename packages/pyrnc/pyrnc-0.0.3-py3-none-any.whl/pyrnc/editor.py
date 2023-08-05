import pickle
from flask import Flask, jsonify, request, send_from_directory
from pyrnc.load import default_path
from pyrnc.parser import Item, Match, JointPages
import os
import socket
import webbrowser


PNAME_GLOBAL = None
app = Flask(__name__)


@app.route("/")
def editor_mainpage():
    return send_from_directory("web", "editor.html")


@app.route("/read_pickle")
def read_pickle():
    global PNAME_GLOBAL
    p = pickle.load(open(os.path.join(default_path, PNAME_GLOBAL), "rb"))
    return jsonify(
        [
            {"index": i,
            "content": html(match),
            "title": title(match.title),
            "(un)mark": mark_button(i, match.marked)
            }
            for (i, match) in enumerate(p.joint_matches)
        ]
    )


@app.route("/mark_index")
def mark_index():
    global PNAME_GLOBAL
    index = int(request.args.get("index"))
    p = pickle.load(open(os.path.join(default_path, PNAME_GLOBAL), "rb"))
    if p.joint_matches[index].marked is None:
        p.joint_matches[index] = Match(
            title=p.joint_matches[index].title,
            text=p.joint_matches[index].text,
            marked=True
        )
    else:
        p.joint_matches[index] = Match(
            title=p.joint_matches[index].title,
            text=p.joint_matches[index].text,
            marked=not p.joint_matches[index].marked
        )
    pickle.dump(p, open(os.path.join(default_path, PNAME_GLOBAL), "wb"))
    return jsonify({
        "marked": p.joint_matches[index].marked
    })


def html(m: Match):
    result = []
    for item in m.text:
        if item.selected:
            result.append(f'<span class="sel">{item.content}</span>')
        else:
            result.append(f'<span class="def">{item.content}</span>')
    bg = "style='background-color: lightgreen'" if m.marked else ""
    return f"<span {bg}>" + "".join(result) + "</span>"


def title(text: str):
    return f"<span class='title'>{text}</span>"


def mark_button(i: int, s: bool):
    inner = "Mark" if not s else "Unmark"
    return f"<button onclick='mark(this, {i})'>{inner}</button>"


def show(pname: str):
    global PNAME_GLOBAL
    PNAME_GLOBAL = pname
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    for _ in range(5): print()
    print(f"Proceed to the link to open the editor: http://localhost:{port}")
    for _ in range(5): print()
    webbrowser.open(f"http://localhost:{port}")
    app.run("0.0.0.0", port=port)
