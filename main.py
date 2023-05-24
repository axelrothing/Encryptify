from website import create_app




app = create_app()
if __name__ == "__main__":
    print("Flask Server Started!")
    app.run(debug=True)

