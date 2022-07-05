from app import main


if __name__ == '__main__':
    try:
        main.run()
    except Exception as err:
        print(f"Oops! Application exited")
