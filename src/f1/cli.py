"""Linha de comando: ``python -m f1.cli --driver 55 --session 9159``."""

import argparse
import sys
from collections.abc import Sequence

from f1.analysis import max_speed
from f1.client import OpenF1Error, get_car_data
from f1.transform import clean


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Telemetria car_data da OpenF1")
    parser.add_argument("--driver", type=int, required=True)
    parser.add_argument("--session", type=int, required=True)
    parser.add_argument("--min-speed", type=int, default=None)
    args = parser.parse_args(argv)

    filters = {"speed>=": args.min_speed} if args.min_speed is not None else {}
    try:
        raw = get_car_data(args.session, args.driver, **filters)
    except OpenF1Error as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1
    data = clean(raw)
    for item in data:
        print(item)
    print(f"{len(data)} registros; velocidade máxima: {max_speed(data)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
