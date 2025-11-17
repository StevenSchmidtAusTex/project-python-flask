import os
from app import create_app
from app.config import DevelopmentConfig, ProductionConfig, validate_production_config

config_class = (
    DevelopmentConfig if os.getenv("FLASK_ENV") == "development" else ProductionConfig
)

# Only validate if using production
if config_class == ProductionConfig:
    validate_production_config()

app = create_app(config_class=config_class)

if __name__ == "__main__":
    app.run()
