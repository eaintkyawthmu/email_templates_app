from app import create_app
from app.models import TemplateManager

app = create_app()

with app.app_context():
    TemplateManager.create_indexes() 


if __name__ == "__main__":
    app.run(debug=True)
