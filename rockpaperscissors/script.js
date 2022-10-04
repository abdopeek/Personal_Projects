var scissors = document.getElementById("scissors");
var paper = document.getElementById("paper");
var rock = document.getElementById("rock");
var comp = ['r','s','p'];
var userresult = document.getElementById("userscore")
var compresult = document.getElementById("compscore");
var result = document.getElementById("result");

paper.addEventListener("click", function(){
    game(paper) }
);
rock.addEventListener("click", function() {
    game(rock) }
);
scissors.addEventListener("click", function() {
    game(scissors) }
);

function game(choice) {
    var compchoice = comp[Math.floor(Math.random() * 3)];
    var userchoice = choice.id;

    if (userchoice == "rock") {
        if (compchoice == "r"){
            result.textContent = "Its a draw!";
        }
        else if (compchoice == "s") {
            result.textContent = "You win!";
            userresult.textContent = Number(userresult.textContent) + 1;
        }  
        else {
            result.textContent = "Computer wins!";
            compresult.textContent = Number(compresult.textContent) + 1;
        }
     }

    if (userchoice == "paper") {
        if (compchoice == "r") {
            result.textContent = "Computer Wins!";
            compresult.textContent = Number(compresult.textContent) + 1;
        }
        else if (compchoice == "p") {
            result.textContent = "Its a draw!";
        }
        else {
            result.textContent = "You win!";
            userresult.textContent = Number(userresult.textContent) + 1;

        }
    }

    if (userchoice == "scissors") {
        if (compchoice == "r") {
            result.textContent = "You win!";
            userresult.textContent = Number(userresult.textContent) + 1;
        }
        else if (compchoice == "s") {
            result.textContent = "Its a draw!";
        }
        else {
            result.textContent = "You lose!"
            compresult.textContent = Number(compresult.textContent) + 1;
        }
    }
}
