#!/usr/bin/env python3
"""Check an OpenScreen CLI JSON result and an optional resulting file."""

import argparse
import json
import sys
from pathlib import Path


class CheckError(Exception):
    pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", required=True, choices=["record", "sources", "captions", "export", "pack", "info"])
    parser.add_argument("--exit-code", required=True, type=int, help="Actual CLI process exit code; do not use the checker's exit code")
    parser.add_argument("--input", required=True, type=Path, help="File containing CLI --json stdout")
    parser.add_argument("--artifact", type=Path, help="Expected exported file or saved project, if applicable")
    args = parser.parse_args()
    try:
        if args.exit_code != 0:
            raise CheckError(f"OpenScreen {args.command} exited with {args.exit_code}; read its stderr before retrying")
        try:
            lines = args.input.read_text(encoding="utf-8").splitlines()
        except OSError as exc:
            raise CheckError(f"Cannot read stdout file {args.input}: {exc}") from exc
        if not lines or any(not line.strip() for line in lines):
            raise CheckError("stdout is empty or contains a blank line; expected JSON output")
        try:
            objects = [json.loads(line) for line in lines]
        except json.JSONDecodeError as exc:
            raise CheckError(f"stdout is not valid line-delimited JSON: {exc}") from exc
        if not all(isinstance(obj, dict) for obj in objects):
            raise CheckError("expected a JSON object on each line")
        if args.command == "info":
            if len(objects) != 1 or not objects[0] or "event" in objects[0]:
                raise CheckError("info --json must produce one non-empty summary object without an event field")
            result = objects[0]
            if result.get("screenVideoExists") is not True or not result.get("projectPath"):
                raise CheckError("info reports a missing screen video or project path")
        else:
            result = objects[-1]
            if result.get("event") != "done" or result.get("success") is not True:
                raise CheckError("final event is not a successful done event; inspect stdout and stderr")
            if any(obj.get("event") == "error" for obj in objects):
                raise CheckError("stdout includes an error event despite a successful final event")
            required = {"record": "screenVideoPath", "sources": "sources", "captions": "projectPath", "export": "outputPath", "pack": "projectPath"}
            key = required[args.command]
            if key not in result or result[key] is None:
                raise CheckError(f"successful {args.command} result is missing {key}")
            if args.command == "record" and args.artifact and result.get("projectPath") is None:
                raise CheckError("record result lacks projectPath; was --project supplied?")
            if args.command == "pack":
                files = result.get("files")
                if not isinstance(files, list) or not files or result["projectPath"] not in files:
                    raise CheckError("pack result must list its project and copied files")
                for file in files:
                    if not isinstance(file, str) or not Path(file).is_file() or Path(file).stat().st_size == 0:
                        raise CheckError(f"pack file is missing or empty: {file}")
        if args.artifact:
            artifact = args.artifact.expanduser().resolve()
            if args.command == "pack":
                if not artifact.is_dir():
                    raise CheckError(f"expected bundle directory not found: {artifact}")
                if any(not Path(file).resolve().is_relative_to(artifact) for file in result["files"]):
                    raise CheckError(f"pack result includes a file outside bundle: {artifact}")
            else:
                if not artifact.is_file() or artifact.stat().st_size == 0:
                    raise CheckError(f"expected non-empty file not found: {artifact}")
                field = {"record": "projectPath", "captions": "projectPath", "export": "outputPath"}.get(args.command)
                if field and Path(result[field]).expanduser().resolve() != artifact:
                    raise CheckError(f"result {field} does not match expected file: {artifact}")
        print(json.dumps({"status": "ok", "command": args.command, "artifact": str(args.artifact) if args.artifact else None}, ensure_ascii=False))
        return 0
    except (CheckError, OSError, ValueError) as exc:
        print(f"OpenScreen result check failed: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
