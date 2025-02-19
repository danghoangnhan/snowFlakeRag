from argparse import ArgumentParser
import json
from urllib.request import HTTPError
from railib import api, config, show


def create(database: str, source: str, profile: str):
    cfg = config.read(profile=profile)
    ctx = api.Context(**cfg)
    rsp = api.create_database(ctx, database, source=source)
    print(json.dumps(rsp, indent=2))

def get(database: str, profile: str):
    cfg = config.read(profile=profile)
    ctx = api.Context(**cfg)
    rsp = api.get_database(ctx, database)
    print(json.dumps(rsp, indent=2))

if __name__ == "__main__":
    p = ArgumentParser()
    p.add_argument("database", type=str, help="database name")
    p.add_argument("-p", "--profile", type=str, help="profile name", default="default")
    args = p.parse_args()
    try:
        create(args.database, args.profile)
    except HTTPError as e:
        show.http_error(e)