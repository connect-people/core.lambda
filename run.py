from src import create_app, db

app = create_app()
app.app_context().push()  # lambda start


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False)
