from configargparse import ArgumentParser
from application import app

from yarl import URL
from utls import DEFAULT_PG_URL

# ConfigArgParse allows to use env variables in addition to arguments.
# E.g. you may configure your server using STAFF_HOST, STAFF_PORT, STAFF_DB_URL
# env vars.
parser = ArgumentParser(auto_env_var_prefix='STAFF_')
parser.add_argument('--host', type=str, default='127.0.0.1',
                    help='Host to listen')
parser.add_argument('--port', type=int, default=8080,
                    help='Port to listen')
parser.add_argument('--pg-url', type=URL, default=URL(DEFAULT_PG_URL),
                    help='URL to use to connect to the postgres database')


if __name__ == '__main__':
    args = parser.parse_args()
    host = args.host
    port = args.port
    pg_url = args.pg_url
    app.main(host, port, pg_url)
