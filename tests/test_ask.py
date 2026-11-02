"""app.ask の会話モードのテスト（APIキー不要。偽のクライアントを使う）。"""

from types import SimpleNamespace

from app import ask


class FakeChat:
    def __init__(self):
        self.history = []

    def send_message(self, text):
        self.history.append(text)
        return SimpleNamespace(
            text=f"回答{len(self.history)}",
            usage_metadata=SimpleNamespace(prompt_token_count=3, candidates_token_count=2),
        )


def test_chat_keeps_history(capsys):
    session = FakeChat()
    client = SimpleNamespace(chats=SimpleNamespace(create=lambda model: session))
    inputs = iter(["最初の質問", "続きの質問", "exit"])
    ask.chat(client=client, input_fn=lambda _: next(inputs))
    assert session.history == ["最初の質問", "続きの質問"]
    out = capsys.readouterr().out
    assert "回答2" in out and "入力=3 出力=2" in out
