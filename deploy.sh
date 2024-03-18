#!/bin/bash

while getopts e:n: flag; do
    case "${flag}" in
    e) envFile=${OPTARG} ;;
    n) name=${OPTARG} ;;
    esac
done

export $(grep -v '^#' ${envFile:='.env'} | xargs -d '\n')
envsubst <docker-swarm.yml | docker stack deploy -c - ${name:=winichat}

