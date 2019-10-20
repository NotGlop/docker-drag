# docker-drag
This repository contains Python scripts for interacting with Docker Hub without needing the Docker client itself.

It interacts with APIs following the Docker Hub API v2 spec.
See [https://docs .docker.com/registry/spec/api/]()

## Pull a Docker image in HTTPS

`python docker_pull.py hello-world`

`python docker_pull.py alpine:3.9`

`python docker_pull.py kalilinux/kali-linux-docker`

<p align="center">
  <img src="https://user-images.githubusercontent.com/26483750/63388733-b419f480-c3a9-11e9-8617-7c5b47b76dbd.gif">
</p>

## Windows Container Support
This project offers limited support for Windows containers.
Microsoft hosts Windows containers on [https://mcr.microsoft.com/v2]()
and its API behaves differently than Docker Hub. As a result, some
containers may not properly download. This is most prevalent when 
Docker Hub is hosting the container but it depends upon an underlying
Windows image. For example:

`python docker_pull.py hello-world:nanoserver-1803`

will return an error since the hello-world Dockerfile pulls the 
Windows nanoserver image. If you still want to use the hello-world
container, you can manually pull its dependencies like so:

hello-world dockerfile:
```Dockerfile
FROM mcr.microsoft.com/windows/nanoserver:1803
COPY hello.txt C:
CMD ["cmd", "/C", "type C:\\hello.txt"]
```
Get the nanoserver image tar from docker_pull:

`python docker_pull.py mcr.microsoft.com/windows/nanoserver:1803-amd64`

Note: when downloading windows containers, you may need to use a more specific tag. 
Even though windows lists tags such as "1803", you may need to specify a more detailed tag such as "1803-amd64" since not all tags on mcr.microsoft.com actually link to a container download.

Then transfer the tar file to the docker machine and load the image:

`docker load -i windows_nanoserver.tar`

Then build the hello-world image from the dockerfile and nanoserver image.



## Limitations
- Takes the default manifest (independent of the architecture)
- Only support v2 manifests

## Well known bugs
2 open bugs which shouldn't affect the efficiency of the script nor the pulled image:
- Unicode content (for example `\u003c`) gets automatically decoded by `json.loads()` which differs from the original Docker client behaviour (`\u003c` should not be decoded when creating the TAR file). This is due to the json Python library automatically converting string to unicode.
- Fake layers ID are not calculated the same way than Docker client does (I don't know yet how layer hashes are generated, but it seems deterministic and based on the client)
