var prevTile = null;

//board & and solution are place
var board = [
    "--74916-5",
    "2---6-3-9",
    "-----7-1-",
    "-586----4",
    "--3----9-",
    "--62--187",
    "9-4-7---2",
    "67-83----",
    "81--45---"
]

var solution = [
    "387491625",
    "241568379",
    "569327418",
    "758619234",
    "123784596",
    "496253187",
    "934176852",
    "675832941",
    "812945763"
]

window.onload = function() {
    setGame();
}

//Establishes the Board display
function setGame() {
    // Board 9x9
    for (let r = 0; r < 9; r++) {
        for (let c = 0; c < 9; c++) {
            let tile = document.createElement("div");
            tile.id = r.toString() + "-" + c.toString();
            if (board[r][c] != "-") {
                tile.innerText = board[r][c];
                tile.classList.add("tile-start");
            }
            if (r == 2 || r == 5) {
                tile.classList.add("horizontal-line");
            }
            if (c == 2 || c == 5) {
                tile.classList.add("vertical-line");
            }
            tile.addEventListener("click", selectTile);
            tile.classList.add("tile");
            document.getElementById("board").append(tile);
        }
    }
}

//Updates the Tile color and Number Cycle
function selectTile() {

    if (prevTile == null){
        this.classList.add("clicked");
        prevTile = this;
    }else{
        prevTile.classList.remove("clicked");
        this.classList.add("clicked");
        prevTile = this;
    }
    // "0-0" "0-1" .. "3-1"
    //Updates the Number in the Tile, 1-9
    if (!this.classList.contains("tile-start")){
        if (this.innerText == " "){
            this.innerText = 1;
        }else if (this.innerText == 9){
            this.innerText = " ";
            this.classList.remove("clicked")
        }else{
            this.innerText++;
        }
    }
}
