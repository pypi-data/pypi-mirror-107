from argparse import ArgumentParser


class Arguments:
    arguments = None

    def __init__(self):
        parser = ArgumentParser(
            description="Command-line program to download music from YouTube and other websites."
        )
        parser.add_argument("url", help="URL of the music to download")

        self.arguments = parser.parse_args()

    def check(self):
        """
        Checks the value and compatibility of arguments.
        """
        print("check done")
