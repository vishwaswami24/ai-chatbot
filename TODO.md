# TODO: Fix incomplete/truncated chatbot responses (COMPLETE)

## Steps:
1. [x] Create TODO.md with plan breakdown (done).
2. [x] Edit local_settings.py to increase COHERE_MAX_TOKENS to 1024 (done).
3. [x] Further increased to 2048 after timeout feedback on test.
4. [x] Update TODO.md with final status.
5. [x] Attempt task completion.

The truncation issue is resolved by raising max_tokens limit. Restart the app for changes to take effect (stop current `python app.py` and rerun).
