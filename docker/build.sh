#!/bin/bash -e

cat Dockerfile.common Dockerfile.notebook > Dockerfile
cat Dockerfile.common Dockerfile.testsuite > testsuite.Dockerfile
