const pieceMap = new Map()
  
pieceMap.set("1","♚")
pieceMap.set("3","♜")
pieceMap.set("5","♞")
pieceMap.set("6","♝")
pieceMap.set("8","♟")
pieceMap.set("9","♛")
pieceMap.set("-1","♔")
pieceMap.set("-3","♖")
pieceMap.set("-5","♘")
pieceMap.set("-6","♗")
pieceMap.set("-8","♙")
pieceMap.set("-9","♕")
pieceMap.set("0","<br>")
let firstPos= false
let secondPos = false


function cords(elem){
 
  if (!firstPos){


        firstPos = elem.id
        elem.parentNode.style =  "width:24pt; height:24pt; border-collapse:collapse; border-color: green; border-style: solid; border-width: 0pt 1pt 1pt 0pt"

        }
      else{
      get_board(firstPos, elem.id)
      firstPos=false
      }
      //do stuff
    }

function draw(board){
 
  for (var i = 0; i < 8; i++) {
    for (var j = 0; j< 8; j++) {
   
    elemento = document.getElementById(i+""+j);
    elemento.innerHTML = pieceMap.get(board[i][j]+"")
    
  }
  }

  
  
  }
  gameid =document.getElementById("gameidgetter").innerHTML.trim();
  



  function get_board(pos1,pos2){
    
    $.ajax({
            type: 'GET',
            url: "{% url 'main-play' %}",
            data: {"pos1": pos1,
                  "pos2":pos2,
                  "id":gameid},
            success: function (response) {
                // if not valid user, alert the user
                draw(response["board"])
            },
            error: function (response) {
                console.log(response)
            }
        })}


  function get_board_latest(){

    $.ajax({
            type: 'GET',
            url: "{% url 'main-play' %}",
            data: {"id":gameid},
            success: function (response) {
                // if not valid user, alert the user
                draw(response["board"])
            },
            error: function (response) {
                console.log(response)
            }
        })}

  

 
function get_board_temp(){
  t =document.getElementById("tempsend").value
  pos1 = t.split(" ")[0]+""
  pos2 = t.split(" ")[1]+""
  
  get_board(pos1,pos2)
}
//t =document.getElementById("buttonsend").onclick = ()=>{get_board_temp()};


  $(document).ready(function()
    {
      $( "#buttonsend" ).click(function() {
      get_board_temp()
        });

        $( "#buttonupdate" ).click(function() {
      get_board_latest()
        });
    }

  );
  get_board_latest()