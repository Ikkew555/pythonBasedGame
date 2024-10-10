import random
import time
from django.shortcuts import render, redirect
from .models import Leaderboard, PlayerScore

# Define levels: easy, medium, and hard
LEVELS = {
    "easy": 8,  # 8 cards for easy (4 pairs)
    "medium": 16,  # 16 cards for medium (8 pairs)
    "hard": 24,  # 24 cards for hard (12 pairs)
}

# Define fruit lists for each level
FRUITS_EASY = [
    {"name": "banana", "image": "banana.png"},
    {"name": "apple", "image": "apple.png"},
    {"name": "orange", "image": "orange.png"},
    {"name": "grape", "image": "grape.png"},
]

FRUITS_MEDIUM = [
    {"name": "banana", "image": "banana.png"},
    {"name": "apple", "image": "apple.png"},
    {"name": "orange", "image": "orange.png"},
    {"name": "grape", "image": "grape.png"},
    {"name": "pineapple", "image": "pineapple.png"},
    {"name": "strawberry", "image": "strawberry.png"},
    {"name": "mango", "image": "mango.png"},
    {"name": "kiwi", "image": "kiwi.png"},
]

FRUITS_HARD = [
    {"name": "banana", "image": "banana.png"},
    {"name": "apple", "image": "apple.png"},
    {"name": "orange", "image": "orange.png"},
    {"name": "grape", "image": "grape.png"},
    {"name": "pineapple", "image": "pineapple.png"},
    {"name": "strawberry", "image": "strawberry.png"},
    {"name": "mango", "image": "mango.png"},
    {"name": "kiwi", "image": "kiwi.png"},
    {"name": "watermelon", "image": "watermelon.png"},
    {"name": "blueberry", "image": "blueberry.png"},
    {"name": "peach", "image": "peach.png"},
    {"name": "cherry", "image": "cherry.png"},
    {"name": "pear", "image": "pear.png"},
    {"name": "roseapple", "image": "roseapple.png"},
    {"name": "grapefruit", "image": "grapefruit.png"},
    {"name": "pomelo", "image": "ugliFruit.png"},
]


def start_game(request, level):
    """Starts a new game with the selected difficulty level."""
    request.session.flush()  # Clear all previous session data

    if level not in LEVELS:
        return redirect("index")

    num_pairs = LEVELS[level] // 2  # Number of pairs for the selected level
    request.session["level"] = level  # Store the level in session

    # Select the appropriate fruit list based on the level
    if level == "easy":
        selected_fruits = FRUITS_EASY
    elif level == "medium":
        selected_fruits = FRUITS_MEDIUM
    else:  # level == "hard"
        selected_fruits = FRUITS_HARD

    # Create a deck of fruit cards (each fruit appears twice)
    deck = random.sample(selected_fruits, num_pairs) * 2
    random.shuffle(deck)

    # Initialize the session variables
    request.session["deck"] = deck
    request.session["matched"] = []  # List to track matched cards
    request.session["flipped"] = []  # List to track flipped cards
    request.session["start_time"] = 0  # Initialize start time

    return render(
        request,
        "fruit_game/game.html",
        {
            "deck": deck,
            "level": level,  # Pass the level to the template
        },
    )


def match_card(request, card_index):
    """Handles card matching logic when a card is clicked."""
    deck = request.session.get("deck", [])
    matched = request.session.get("matched", [])
    flipped = request.session.get("flipped", [])
    start_time = request.session.get("start_time", 0)

    # Start the timer on the first card click
    if start_time == 0:
        start_time = time.time()
        request.session["start_time"] = start_time

    # Check if the card is already matched or flipped
    if card_index in matched or card_index in flipped:
        return render(
            request,
            "fruit_game/game.html",
            {
                "deck": deck,
                "matched": matched,
                "flipped": flipped,
                "time": int(time.time() - start_time),  # Update elapsed time
                "level": request.session["level"],  # Pass the level to the template
            },
        )

    # Add the card to the flipped cards
    flipped.append(card_index)
    request.session["flipped"] = flipped

    # Check if two cards are flipped
    if len(flipped) == 2:
        first_card = deck[flipped[0]]
        second_card = deck[flipped[1]]

        # Check for a match
        if first_card["name"] == second_card["name"]:
            matched.extend(flipped)  # Add matched cards to the matched list
            request.session["matched"] = matched

            # Check if all cards are matched
            if len(matched) == len(deck):
                elapsed_time = int(time.time() - start_time)  # Calculate elapsed time
                return render(
                    request,
                    "fruit_game/congratulations.html",
                    {
                        "time": elapsed_time,  # Pass the elapsed time
                    },
                )

        # Reset flipped cards regardless of match result
        request.session["flipped"] = []

    # Continue the game and show the current state
    return render(
        request,
        "fruit_game/game.html",
        {
            "deck": deck,
            "matched": matched,
            "flipped": flipped,
            "time": int(time.time() - start_time),  # Update elapsed time
            "level": request.session["level"],  # Pass the level to the template
        },
    )


def reset_game(request):
    """Resets the game session."""
    request.session.flush()  # Clear all session data
    return redirect("index")


def leaderboard(request):
    """Display the leaderboard with player scores."""
    scores = PlayerScore.objects.order_by("time")
    return render(request, "fruit_game/leaderboard.html", {"scores": scores})


def submit_score(request):
    player_name = request.GET.get("playerName")
    time_taken = request.GET.get("time")  # Get the time from the URL
    level = request.session.get(
        "level", "unknown"
    )  # Get the level from session (easy, medium, hard)

    # Save the score in the database
    if player_name and time_taken:
        PlayerScore.objects.create(name=player_name, time=int(time_taken), level=level)

    # Redirect to the index page to show the leaderboard
    return redirect("index")


def index(request):
    """Render the game index page, including leaderboard."""
    scores = PlayerScore.objects.all().order_by("time")
    # [
    #     :20
    # ]
    # Get only the top 10 scores
    return render(request, "fruit_game/index.html", {"scores": scores})


def congratulations(request):
    """Renders the congratulations page."""
    time_taken = request.GET.get("time", 0)  # Get the time from the request
    return render(request, "fruit_game/congratulations.html", {"time": time_taken})


def clear_leaderboard(request):
    # Delete all entries from the PlayerScore model
    PlayerScore.objects.all().delete()

    # Redirect back to the index page (or the leaderboard page)
    return redirect("index")  # Change to your actual index or leaderboard URL name
