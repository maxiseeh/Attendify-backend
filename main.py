from app import create_app

app = create_app()


@app.route("/")
def home():
    return {
        "message": "Attendify API is running!",
        "status": "ok",
        "endpoints": {
            "register": "/api/auth/register",
            "login": "/api/auth/login",
            "attendance": "/api/attendance/mark",
            "sessions": "/api/sessions/",
            "wifi_scan": "/api/wifi/scan",
            "reports": "/api/reports/summary"
        }
    }, 200


if __name__ == "__main__":
    app.run(debug=True)
