# docker-drag
This repository contains Python scripts for interacting with Docker Hub or other registries, without needing the Docker client itself.

It relies on the Docker registry [HTTPS API v2](https://docs.docker.com/registry/spec/api/).

## Pull a Docker image in HTTPS

`python docker_pull.py hello-world`

`python docker_pull.py mysql/mysql-server:8.0`

`python docker_pull.py mcr.microsoft.com/mssql-tools`

`python docker_pull.py consul@sha256:6ba4bfe1449ad8ac5a76cb29b6c3ff54489477a23786afb61ae30fb3b1ac0ae9`

<p align="center">
  <img src="https://user-images.githubusercontent.com/26483750/77766160-8da6f080-703f-11ea-953c-fd69978cb3bf.gif">
</p>

## Limitations
- Only support v2 manifests: some registries, like quay.io which only uses v1 manifests, may not work.

## Well known bugs
2 open bugs which shouldn't affect the efficiency of the script nor the pulled image:
- Unicode content (for example `\u003c`) gets automatically decoded by `json.loads()` which differs from the original Docker client behaviour (`\u003c` should not be decoded when creating the TAR file). This is due to the json Python library automatically converting string to unicode.
- Fake layers ID are not calculated the same way than Docker client does (I don't know yet how layer hashes are generated, but it seems deterministic and based on the client)
