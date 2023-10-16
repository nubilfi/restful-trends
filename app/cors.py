from app.settings import settings

def cors_config():
    # List of allowed domains and subdomains
    allowed_domains = [
        "example1.com",
        "example2.com",
    ]

    # Generate allow_origins list dynamically
    allow_origins = [f"https://www.{domain}" for domain in allowed_domains]
    allow_origins += [f"https://{subdomain}.{domain}" for domain in allowed_domains for subdomain in ("api")]

    # Determine the mode based on the DEVELOPMENT_MODE environment variable
    development_mode = settings.development_mode == "true"

    # Configure CORS middleware
    if development_mode:
        # Allow requests from all origins in development
        cors_middleware = {
            "allow_origins": ["*"],
            "allow_methods": ["GET", "POST"],
            "allow_headers": ["*"],
            "allow_credentials": False,
            "max_age": 3600
        }
    else:
        # Configure production CORS settings here
        cors_middleware = {
            "allow_origins": allow_origins,
            "allow_methods": ["GET", "POST"],
            "allow_headers": ["*"],
            "allow_credentials": False,
            "max_age": 3600
        }

    return cors_middleware
