from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from random import choice

wordDB : list[str] = ["bread", "clock", "kebab", "magic", "opera"]

class WordleGame() :
    def __init__(self):
        self.answer : str = choice(wordDB)
    def guess(self, word:str) -> list[str] :
        res = ["out"] * 5
        for idx, letter in enumerate(word) : 
            if letter == self.answer[idx] :
                res[idx] = "strike"
            elif letter in self.answer :
                res[idx] = "ball"
            else :
                res[idx] = "out"
        return res
    def get_answer(self) -> str:
        return self.answer

class WordleGuess(BaseModel):
    attempt: int = Field(ge=1, le=6)
    word: str

    @field_validator("word", mode="before")
    @classmethod
    def val_word(cls, word:str):
        if len(word) != 5 :
            raise ValueError("Guess word must be 5 letters.")
        return word

app = FastAPI()
game = WordleGame()

@app.post("/guess")
def wordle_guess(wg: WordleGuess) -> dict:
    return {"current attempts" : wg.attempt,
            "guess feedback" : game.guess(wg.word)
            }

@app.get("/answer")
def check_answer() -> str:
    return game.get_answer()