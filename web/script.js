document.addEventListener('DOMContentLoaded', (event) => {
    initializeGame();
});

async function initializeGame() {
    try {
        let response = await eel.get_initial_state()();
        updateUI(response);
        
        // Enable or disable the "Deal Cards" button based on the game state
        if (response.player1.hand.length > 0) {
            disableButton("deal-cards-button");
            enableButton("flop-button");
        }
    } catch (error) {
        console.error(error);
    }
}

async function dealCards() {
    disableButton("deal-cards-button");
    try {
        let response = await eel.deal_cards()();
        updateUI(response);
        enableButton("flop-button");
    } catch (error) {
        console.error(error);
        enableButton("deal-cards-button"); // Re-enable in case of error
    }
}

async function collectBets(action) {
    try {
        let response;
        if (action === "raise") {
            let raise_amount = prompt("Enter raise amount:");
            if (raise_amount === null) {
                return;
            }
            response = await eel.collect_bets(action, raise_amount)();
            updateUI(response);
            alert(`You raised ${raise_amount}. AI calls.`);
        } else if (action === "check") {
            response = await eel.collect_bets(action)();
            updateUI(response);
            if (response.log.includes("both players check")) {
                alert("Both players checked. Dealing the next stage.");
            } else {
                alert("You checked. AI checks.");
            }
        }
    } catch (error) {
        console.error(error);
    }
}

async function dealFlop() {
    disableButton("flop-button");
    try {
        let response = await eel.deal_community_cards(3)();
        updateUI(response);
        enableButton("turn-button");
    } catch (error) {
        console.error(error);
    }
}

async function dealTurn() {
    disableButton("turn-button");
    try {
        let response = await eel.deal_community_cards(1)();
        updateUI(response);
        enableButton("river-button");
    } catch (error) {
        console.error(error);
    }
}

async function dealRiver() {
    disableButton("river-button");
    try {
        let response = await eel.deal_community_cards(1)();
        updateUI(response);
    } catch (error) {
        console.error(error);
    }
}

async function showdown() {
    try {
        let response = await eel.showdown()();
        updateUI(response);
    } catch (error) {
        console.error(error);
    }
}

async function playNextRound() {
    disableButton("turn-button");
    disableButton("river-button");
    disableButton("flop-button");
    enableButton("deal-cards-button");

    try {
        let response = await eel.play_next_round()();
        updateUI(response);
    } catch (error) {
        console.error(error);
    }
}

function updateUI(response) {
    document.getElementById("player1-name").innerText = response.player1.name;
    document.getElementById("player1-chips").innerText = response.player1.chips;
    updateHand(document.getElementById("player1-hand"), response.player1.hand);

    document.getElementById("player2-name").innerText = response.player2.name;
    document.getElementById("player2-chips").innerText = response.player2.chips;
    updateHand(document.getElementById("player2-hand"), response.player2.hand);

    updateCommunityCards(response);
}

function updateHand(element, hand) {
    element.innerHTML = hand.map(card => `<img src="${card}" class="card">`).join("");
}

function updateCommunityCards(response) {
    let communityCards = response.community_cards.map(card => `<img src="${card}" class="card">`).join("");
    document.getElementById("cards").innerHTML = communityCards;
}

function disableButton(buttonId) {
    document.getElementById(buttonId).disabled = true;
}

function enableButton(buttonId) {
    document.getElementById(buttonId).disabled = false;
}
