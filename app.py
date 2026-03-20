import os
from typing import Any

from cohere import Client
from cohere.core.api_error import ApiError
from cohere.errors import ForbiddenError, InvalidTokenError, TooManyRequestsError, UnauthorizedError
import httpx
from flask import Flask, current_app, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

DEFAULT_MODEL = "command-a-03-2025"
DEFAULT_MAX_TOKENS = 160
DEFAULT_TEMPERATURE = 0.9
DEFAULT_TIMEOUT_SECONDS = 20.0


def _env_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


def _env_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


def _apply_env_overrides(config: dict[str, Any]) -> None:
    env_secret_key = os.getenv("FLASK_SECRET_KEY", "").strip()
    env_api_key = os.getenv("COHERE_API_KEY", "").strip()
    env_model = os.getenv("COHERE_MODEL", "").strip()

    if env_secret_key:
        config["SECRET_KEY"] = env_secret_key
    if env_api_key:
        config["COHERE_API_KEY"] = env_api_key
    if env_model:
        config["COHERE_MODEL"] = env_model
    if os.getenv("COHERE_MAX_TOKENS") is not None:
        config["COHERE_MAX_TOKENS"] = _env_int("COHERE_MAX_TOKENS", config["COHERE_MAX_TOKENS"])
    if os.getenv("COHERE_TEMPERATURE") is not None:
        config["COHERE_TEMPERATURE"] = _env_float("COHERE_TEMPERATURE", config["COHERE_TEMPERATURE"])
    if os.getenv("COHERE_TIMEOUT_SECONDS") is not None:
        config["COHERE_TIMEOUT_SECONDS"] = _env_float(
            "COHERE_TIMEOUT_SECONDS",
            config["COHERE_TIMEOUT_SECONDS"],
        )


class PromptForm(FlaskForm):
    text = TextAreaField(
        "Prompt",
        filters=[lambda value: value.strip() if value else ""],
        validators=[
            DataRequired(message="Please enter a prompt."),
            Length(max=2000, message="Prompts must be 2000 characters or fewer."),
        ],
    )
    submit = SubmitField("Generate Response")


def build_cohere_client(api_key: str) -> Client:
    return Client(
        api_key,
        timeout=current_app.config["COHERE_TIMEOUT_SECONDS"],
    )


def generate_response(prompt: str) -> tuple[str | None, str | None]:
    api_key = current_app.config.get("COHERE_API_KEY", "").strip()
    if not api_key:
        return None, "Add your Cohere API key in local_settings.py or set COHERE_API_KEY."

    client = build_cohere_client(api_key)

    try:
        response = client.chat(
            message=prompt,
            model=current_app.config["COHERE_MODEL"],
            max_tokens=current_app.config["COHERE_MAX_TOKENS"],
            temperature=current_app.config["COHERE_TEMPERATURE"],
        )
    except httpx.TimeoutException:
        if not current_app.testing:
            current_app.logger.exception("Cohere chat request timed out")
        return None, "The chatbot took too long to respond. Try a shorter prompt in a moment."
    except (UnauthorizedError, InvalidTokenError):
        if not current_app.testing:
            current_app.logger.exception("Cohere rejected the API key")
        return None, "Your Cohere API key was rejected. Update COHERE_API_KEY and try again."
    except ForbiddenError:
        if not current_app.testing:
            current_app.logger.exception("Cohere forbade the request")
        return None, "Cohere rejected this request. Check your API key permissions."
    except TooManyRequestsError:
        if not current_app.testing:
            current_app.logger.exception("Cohere rate limited the request")
        return None, "Cohere rate-limited the chatbot. Please wait a bit and try again."
    except ApiError as exc:
        if not current_app.testing:
            current_app.logger.exception(
                "Cohere API error (status_code=%s)",
                getattr(exc, "status_code", None),
            )
        return None, "Cohere rejected the request. Check the model name and token settings."
    except Exception:
        if not current_app.testing:
            current_app.logger.exception("Cohere chat request failed")
        return None, "The chatbot could not reach Cohere just now. Please try again."

    output = getattr(response, "text", "").strip()
    if not output:
        return None, "Cohere returned an empty response. Try rephrasing your prompt."

    return output, None


def create_app(test_config: dict[str, Any] | None = None) -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_mapping(
        SECRET_KEY="dev-secret-key",
        COHERE_API_KEY="",
        COHERE_MODEL=DEFAULT_MODEL,
        COHERE_MAX_TOKENS=DEFAULT_MAX_TOKENS,
        COHERE_TEMPERATURE=DEFAULT_TEMPERATURE,
        COHERE_TIMEOUT_SECONDS=DEFAULT_TIMEOUT_SECONDS,
    )
    app.config.from_pyfile("local_settings.py", silent=True)
    _apply_env_overrides(app.config)

    if test_config:
        app.config.update(test_config)

    @app.route("/", methods=["GET", "POST"])
    def home() -> str:
        form = PromptForm()
        output = None
        error = None

        if form.validate_on_submit():
            output, error = generate_response(form.text.data.strip())

        return render_template("home.html", form=form, output=output, error=error)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
