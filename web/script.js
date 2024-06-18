async function dealCards() {
    try {
        let response = await eel.deal_cards()();
        updateUI(response);
    } catch (error) {
        console.error(error);
    }
}

async function collectBets() {
    try {
        let response = await eel.collect_bets()();
        updateUI(response);
    } catch (error) {
        console.error(error);
    }
}

async function dealFlop() {
    disableButton("flop-button");
    try {
        let response = await eel.deal_community_cards(3)();
        updateUI(response);
    } catch (error) {
        console.error(error);
    }
}

async function dealTurn() {
    disableButton("turn-button");
    try {
        let response = await eel.deal_community_cards(1)();
        updateUI(response);
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
    enableButton("flop-button");
    enableButton("turn-button");
    enableButton("river-button");
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
    document.getElementById("player1-hand").innerText = response.player1.hand.join(", ");

    document.getElementById("player2-name").innerText = response.player2.name;
    document.getElementById("player2-chips").innerText = response.player2.chips;
    document.getElementById("player2-hand").innerText = response.player2.hand.join(", ");

    updateCommunityCards(response);
}

function updateCommunityCards(response) {
    let communityCards = response.community_cards.map(card => `<div class="card">${card}</div>`).join("");
    document.getElementById("cards").innerHTML = communityCards;
}

function disableButton(buttonId) {
    document.getElementById(buttonId).disabled = true;
}

function enableButton(buttonId) {
    document.getElementById(buttonId).disabled = false;
}