document.addEventListener('DOMContentLoaded', (event) => {
    initializeGame();
});

async function initializeGame() {
    try {
        let response = await eel.get_initial_state()();
        updateUI(response);
        hideBlinds();
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
        enableButton("check-button");
        enableButton("raise-button");
        enableButton("fold-button");
        let response = await eel.deal_cards()();
        updateUI(response);
        showBlinds();
        enableButton("check-button");        
        updateBestHand(response);
    } catch (error) {
        console.error(error);
        enableButton("deal-cards-button");
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
            updateBestHand(response);
            updateUI(response);
            showMessage(`You raised ${raise_amount}. AI calls.`);
            response = await eel.collect_bets("check")();
            updateUI(response);
        } else if (action === "check") {
            response = await eel.collect_bets(action)();
            updateBestHand(response);
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
        try {
            hideBestHand();
            let response = await eel.reset_game()();
            updateUI(response);
            hideBlinds();
            disableButton("play-next-round-button");
            enableButton("deal-cards-button");
        } catch (error) {
            console.error(error);
        }
    }
}

async function handleFoldClick() {
    try {
        hideBestHand();
        let response = await eel.fold()();
        updateUI(response);
        hideBlinds();
        showMessage("You folded. AI wins the round.");
        
        // Disable all action buttons except "Play Next Round"
        disableButton("deal-cards-button");
        disableButton("check-button");
        disableButton("raise-button");
        disableButton("fold-button");
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

    // Update pot and bets information
    document.getElementById("pot").innerText = `Pot: ${response.pot}`;
    document.getElementById("highest-bet").innerText = `Highest Bet: ${response.highest_bet}`;

    // Update blinds and dealer information
    updateBlinds(response.current_dealer);

    // Enable Play Next Round button if the game is in showdown state
    if (response.is_showdown) {
        enableButton("play-next-round-button");
    }
}


function updateBlinds(currentDealer) {
    const player1Blind = document.getElementById("player1-blind");
    const player2Blind = document.getElementById("player2-blind");

    if (currentDealer === 0) { 
        player1Blind.classList.add('big-blind');
        player1Blind.classList.remove('small-blind');
        player1Blind.style.display = 'inline-block';

        player2Blind.classList.add('small-blind');
        player2Blind.classList.remove('big-blind');
        player2Blind.style.display = 'inline-block';
    } else { 
        player1Blind.classList.add('small-blind');
        player1Blind.classList.remove('big-blind');
        player1Blind.style.display = 'inline-block';

        player2Blind.classList.add('big-blind');
        player2Blind.classList.remove('small-blind');
        player2Blind.style.display = 'inline-block';
    }
}

function hideBlinds() {
    const player1Blind = document.getElementById("player1-blind");
    const player2Blind = document.getElementById("player2-blind");
    player1Blind.style.display = 'none';
    player2Blind.style.display = 'none';
}

function showBlinds() {
    const player1Blind = document.getElementById("player1-blind");
    const player2Blind = document.getElementById("player2-blind");

    player1Blind.style.display = 'inline-block';
    player2Blind.style.display = 'inline-block';
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

function hideBestHand() {
    const best_hand_container = document.getElementById("player1-best-hand");
    best_hand_container.style.display = "none";
}


function updateBestHand(response) {
    const player1BestHandElement = document.getElementById("player1-best-hand");
    if (response.player1.best_hand) {
        player1BestHandElement.style.display = 'block';
        player1BestHandElement.innerText = `Best Hand: ${response.player1.best_hand}`;
    }
}

