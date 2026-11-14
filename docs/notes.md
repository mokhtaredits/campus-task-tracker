# Technical Notes



## Biggest Docker problem



After installing Docker Desktop, `docker version` showed the client

but could not connect to the Docker Engine. I opened Docker Desktop,

waited until it displayed `Engine running`, and ran `docker version`

again. This time it showed both the client and server. I then built

the image, started the container with Docker Compose, and confirmed

that it was healthy and that `/health` returned `{"status":"ok"}`.



## Most important Git and GitHub lesson



My first push returned HTTP 403 because Git used a different GitHub

account. I updated the remote URL to specify the repository owner's

account, signed in through the browser, and successfully pushed `main`.

I learned to check which account Git uses when a push is denied.


