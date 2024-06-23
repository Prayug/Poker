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
        enableButton("check-button");
    } catch (error) {
        console.error(error);
        enableButton("deal-cards-button"); // Re-enable in case of error
    }
}

async function collectBets(action, raise_amount = null) {
    try {
        let response;
        if (action === "raise") {
            if (raise_amount === null || raise_amount < 0) {
                return;
            }
            response = await eel.collect_bets(action, raise_amount)();
            updateUI(response);
            showMessage(`You raised ${raise_amount}. AI calls.`);
        } else if (action === "check") {
            response = await eel.collect_bets(action)();
            updateUI(response);
            showMessage("Check");

            if (response.log.includes("Dealing Flop") || response.log.includes("Dealing Turn") || response.log.includes("Dealing River")) {
                enableButton("play-next-round-button");
            }
        }
    } catch (error) {
        console.error(error);
    }
}

async function handleCheckClick() {
    await collectBets("check");
}

async function handleRaiseClick() {
    const raiseAmount = document.getElementById("raise-input").value;
    if (raiseAmount) {
        await collectBets("raise", raiseAmount);
        hideRaiseInput();
    }
}

async function playNextRound() {
    if (!document.getElementById("play-next-round-button").disabled) {
        ["turn-button", "river-button", "flop-button"].forEach(disableButton);
        enableButton("deal-cards-button");

        try {
            let response = await eel.play_next_round()();
            updateUI(response);
        } catch (error) {
            console.error(error);
        }
    }
}

async function handleFoldClick() {
    try {
        let response = await eel.fold()();
        updateUI(response);
        showMessage("You folded. AI wins the round.");
        enableButton("play-next-round-button");
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
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = true;
    }
}

function enableButton(buttonId) {
    const button = document.getElementById(buttonId);
    if (button) {
        button.disabled = false;
    }
}

function showMessage(text) {
    const messageDiv = document.getElementById("message");
    messageDiv.innerText = text;
    messageDiv.style.display = "block";
    messageDiv.style.opacity = 1;

    setTimeout(() => {
        messageDiv.style.opacity = 0;
        setTimeout(() => {
            messageDiv.style.display = "none";
        }, 1000); 
    }, 750);
}

function showRaiseInput() {
    const raiseInputContainer = document.getElementById("raise-input-container");
    raiseInputContainer.style.display = "block";
}

function hideRaiseInput() {
    const raiseInputContainer = document.getElementById("raise-input-container");
    raiseInputContainer.style.display = "none";
}
