from flask.cli import main
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) != 2:
        for i, arg in enumerate(sys.argv):
            print(arg)
        sys.exit("Invalid arguments")

    static_dir = os.path.join(os.getcwd(), sys.argv[1])
    if os.path.isdir(static_dir) == False:
        sys.exit(static_dir + " is not directory.")
    sys.argv[1] = "run"
    os.environ["static_dir"] = static_dir
    os.environ["FLASK_ENV"] = "development"
    main()
