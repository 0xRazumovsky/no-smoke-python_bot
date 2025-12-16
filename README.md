Smoke‑Free Buddy is a tiny Telegram bot that sends supportive messages to help quit smoking. It is written with aiogram 3 and designed to run as a webhook handler (e.g., AWS Lambda).

**Response in Russian only**

## What it does

- `/start` replies with a keyboard button “Получить мысль”.
- `/thought` or the button returns a random encouraging message in Russian.
- Uses one webhook-friendly entrypoint: `src.main:handler`.

## Run it yourself

1. Create a bot via BotFather and copy the token.
2. Set an env var `BOT_TOKEN=<your_token>` (or `TELEGRAM_BOT_TOKEN`) — a `.env` file works locally.
3. Install deps: `python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`.
4. Deploy as a webhook function (AWS Lambda/Yandex Cloud/etc.) with handler `src.main.handler` and your env var attached. Expose it through HTTPS (API Gateway, Function URL, etc.).
5. Point Telegram to it: `curl -X POST "https://api.telegram.org/bot$BOT_TOKEN/setWebhook" -d "url=https://<your-endpoint>"`.

## Notes

- The included Dockerfile expects the bot entrypoint to be `bot.py`; rename `src/main.py` or tweak the COPY/CMD lines if you prefer container deployment.
- Keep the token private; never commit real credentials.
- Messages are in Russian—adjust `MESSAGES` and `THOUGHT_BUTTON` in `src/main.py` if you want another language.
