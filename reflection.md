# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?
The guessing system was completely broken when I started, and it looked completely confusing and inconsistent. The developer debug menu updated right after user interaction (causing a delay in what is shown vs what actually happen). Moreover, the hints display the opposite of what is correct, the new game button didn't work, and the scoring system is incorrectly implemented to include negative values. 

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Difficulty Attributes | 8 guesses easy, 6 normal, 5 hard | 6 easy, 8 normal, 5 hard. "Range: 1 to 100. Attempts allowed: 8 (expected 6)" | No console error, more like a bug in game design itself. |

BUG:
attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
# Invalid assignment

FIX:
attempt_limit_map = {
    "Easy": 8,
    "Normal": 6,
    "Hard": 5,
}
# Valid


| Score Assignment | 
Clean attribution based on number of guesses | 
Incorrect calculations, random checks for even numbers. "You won! The secret was 6. Final score: 70 (expected 80)" | 
Negative numbers as score, incorrect score on perfect game, no console errors though. |

BUG:
points = 100 - 10 * (attempt_number + 1)
# Does not account for perfect game, oversubtracts

FIX:
points = 100 - 10 * (attempt_number - 1)
# Accounts for perfect game


| New Game Button | 
Start a fresh new game, new score, history, status, working as intended arbitrary number of times | 
Previous game details not reset even after button click, status permanently stuck on playing, last game history still showing. "(No example can be shown because it's all stuck on the won/lost screen.)" | 
New Game button did not allow user to submit new guesses, stuck permanently until manual app reset. |

BUG:
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(1, 100)
    st.success("New game started.")
    st.rerun()
# Missing reset for state values on new_game

FIX:
if new_game:
    # Start a fresh round for the current difficulty and clear the previous score.
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()
# Resets all necessary values before new_game

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
ChatGPT (Codex).

- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).

One AI suggestion I accepted was resetting the score on new game. Initially, I decided to have the score carry over between games so a cumulative score could be achieved. However, after running the app and seeing as there is no score display until after a game is complete, I decided to have the score reset on each new game.
I made sure to verify it worked by running tests on each "Win" status in the update_score function and checking the score to see it reset.

- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

One AI suggestion I did not accept was the idea to refuse float values and only accept integers. While I understood why non-numeric values like string and None should be refused, I believed that floats could just be truncated into the integer version instead of saying the value was not a valid input. Even though allowing floats could make the UX a bit confusing at first, it would eventually allow for decimal guesses on a future game to be a (terrifying) possibility (meaning it would scale better if the game ever updated).
---

## 3. Debugging and testing your fixes
- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was fixed when test cases passed, quality test cases were used, and the actual experience in the app by a user did not contain the bug during gameplay.

One test I ran was inputting floats and seeing if they were accepted as inputs. I also checked to see what would happen if I got the number in one go (which initially returned 80 instead of 100). I ran tests and played the game myself to see it work.

AI helped design the tests, I made sure to include all the edge cases (even ridiculous ones). Codex would write the tests using assert in the tests file, and I ensured that each case was tested properly and gave the expected result (and not the result codex wrote just to please the test).

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

For a friend who has never used Streamlit but has used React or other JS frameworks, its similar in concept to restarting the whole page on user interaction. The only difference being that React compares the Virtual DOM and actual DOM and changes only whats necessary, while Streamlit will run the entire python script again on user interaction (saving info in a variable).

For a friend who has never used Streamlit or has any coding experience, its similar to commissioning an artist, except every time you tell them to make adjustments, they restart the entire drawing with your change in mind. Using the st session state would be similar to a sticky note on the side of the artist's desk which keeps track of all of your adjustments so as to not forget.
---

## 5. Looking ahead: your developer habits
- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

Definitely documenting my AI usage and changes. I tend to end up combining both AI suggestions and my own thought process without writing it down, similar to Agile development. While it's quick and efficient, documentation can make it really hard for outsiders, or me in the future, to understand the thought process or build. While I can check GitHub, it won't specify who made the change and why unless I leave comments (which aren't perfect).

I would definitely have it write comments above each line of code it changed. This not only lets me know where the AI agent worked, but also what they changed and why. Once I compare the change to what I know is right, or what I actually want, I can edit the code correctly without guessing what's happening.

This process really opened my eyes to the potential of AI code. Previously, I looked at agents as great coders who don't remember anything and could potentially make huge mistakes. However, under the right practices, they can make developer work a lot quicker in the right hands. They don't necessarily have to be perfect or one-shotters, but they can make debugging and writing quality code a little easier.

