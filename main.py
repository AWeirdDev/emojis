import json
import sys
from base64 import b64decode

from primp import Client


def main(args: list[str]):
    if not args:
        print("usage: main.py <mode>")
        print("       modes: apple, google")
        exit(1)

    mode = args[0]

    if mode == "google":
        print("fetching list.with.images.json")

        client = Client()
        res = client.get(
            "https://raw.githubusercontent.com/chalda-pnuzig/emojis.json/refs/heads/master/src/list.with.images.json"
        )
        emojis = res.json()["emojis"]
        ln = len(emojis)
        names = []

        for i, emoji in enumerate(emojis):
            name = emoji["emoji"]

            print(f"\33[2K\r({i + 1}/{ln}) {name}", end="")

            img_url = emoji["image"]
            img_data = b64decode(
                img_url[len("data:image/png;base64,") :].encode("utf-8")
            )

            try:
                with open(f"google/{name}.png", "wb") as f:
                    f.write(img_data)

                names.append(name)
            except OSError:
                print(f"\33[2K\r({i + 1}/{ln}) FAIL {name}")

        with open("google/emojis.json", "w") as f:
            f.write(json.dumps(names))

        print("\33[2K\rdone!")

    elif mode == "apple":
        print("soon")


if __name__ == "__main__":
    main(sys.argv[1:])
