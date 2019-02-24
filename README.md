# docker-drag
This repository contains Python scripts for interacting with Docker Hub without needing the Docker client itself.

It interacts exclusively with the Docker Hub HTTPS API.


## Pull a Docker image in HTTPS

`python docker_pull.py hello-world`

`python docker_pull.py alpine:3.9`

`python docker_pull.py kalilinux/kali-linux-docker`


## Limitations
- Takes the default manifest (independant of the architecture)
- Only support v2 manifests (not sure if someone need to retrieve v1 manifests)


## Well known bugs
2 open bugs which shouldn't affect the efficiency of the script nor the pulled image:
- Unicode content (for example `\u003c`) gets automatically decoded by `json.loads()` which differs from the original Docker client behaviour (`\u003c` should not be decoded when creating the TAR file). This is due to the json Python library automatically converting string to unicode.
- Fake layers ID are not calculated the same way than Docker client does (I don't know yet how layer hashes are generated, but it seems deterministic and based on the client)
