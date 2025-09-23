from app import create_app
import nest_asyncio

app = create_app()

if __name__ == "__main__":
    nest_asyncio.apply()
    app.run(host="0.0.0.0", port=3000, debug=True)
