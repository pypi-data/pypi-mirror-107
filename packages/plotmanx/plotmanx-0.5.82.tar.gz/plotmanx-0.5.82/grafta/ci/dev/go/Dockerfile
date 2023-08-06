# STAGE 1: build
#FROM golang:1.13.1-alpine3.10 as build
FROM golang:1.16.2-alpine3.10 as build

WORKDIR /source

COPY . .
 
RUN CGO_ENABLED=0 go build -ldflags "-s -w" -o bin/client -v cmd/client/main.go
 
# STAGE 2: run
FROM alpine:3.10 as run
 
COPY --from=build /source/bin/client /client
 
ENTRYPOINT ["/client"]