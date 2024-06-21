import os
from app import create_app
from app.models import TemplateManager
import favicon

app = create_app()

# The Vercel entry point for the serverless function
def handler(event, context):
    return app(event, context)

icons = favicon.get('https://www.python.org/')
icon = icons[0]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

