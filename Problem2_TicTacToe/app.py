from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

board = [""] * 9

def check_winner(b):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for i,j,k in wins:
        if b[i] == b[j] == b[k] and b[i] != "":
            return b[i]
    return None

def is_full(b):
    return "" not in b

def minimax(b, is_max):
    winner = check_winner(b)
    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif is_full(b):
        return 0

    if is_max:
        best = -100
        for i in range(9):
            if b[i] == "":
                b[i] = "O"
                score = minimax(b, False)
                b[i] = ""
                best = max(best, score)
        return best
    else:
        best = 100
        for i in range(9):
            if b[i] == "":
                b[i] = "X"
                score = minimax(b, True)
                b[i] = ""
                best = min(best, score)
        return best

def best_move():
    best_val = -100
    move = -1
    for i in range(9):
        if board[i] == "":
            board[i] = "O"
            val = minimax(board, False)
            board[i] = ""
            if val > best_val:
                move = i
                best_val = val
    return move

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global board
    data = request.get_json()
    idx = data['index']

    if board[idx] == "":
        board[idx] = "X"

        if not check_winner(board) and not is_full(board):
            ai = best_move()
            if ai != -1:
                board[ai] = "O"

    return jsonify({
        "board": board,
        "winner": check_winner(board)
    })

@app.route('/reset')
def reset():
    global board
    board = [""] * 9
    return jsonify({"status": "reset"})

if __name__ == '__main__':
    app.run(debug=True)