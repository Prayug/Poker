async function dealCards() {
    let response = await eel.deal_cards()();
    updateUI(response);
}

async function collectBets() {
    let response = await eel.collect_bets()();
    updateUI(response);
}

async function dealFlop() {
    let response = await eel.deal_community_cards(3)();
    updateUI(response);
}

async function dealTurn() {
    let response = await eel.deal_community_cards(1)();
    updateUI(response);
}

async function dealRiver() {
    let response = await eel.deal_community_cards(1)();
    updateUI(response);
}

async function showdown() {
    let response = await eel.showdown()();
    updateUI(response);
}

function updateUI(response) {
    document.getElementById("player1-name").innerText = response.player1.name;
    document.getElementById("player1-chips").innerText = response.player1.chips;
    document.getElementById("player1-hand").innerText = response.player1.hand.join(", ");

    document.getElementById("player2-name").innerText = response.player2.name;
    document.getElementById("player2-chips").innerText = response.player2.chips;
    document.getElementById("player2-hand").innerText = response.player2.hand.join(", ");

    document.getElementById("cards").innerText = response.community_cards.join(", ");
    document.getElementById("log-text").innerText = response.log.join("\n");
}
