from dashboard.app import create_app


app = create_app()


if __name__ == "__main__":
    # Bind to localhost for safety; change host to '0.0.0.0' if remote access needed.
    app.run(host="127.0.0.1", port=5000, debug=True)
