#!/bin/sh
echo Building basic image

docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=yourStrong(!)Password' -p 1433:1433 -d mcr.microsoft.com/mssql/server:2019-CU5-ubuntu-16.04


#echo Building final image

#docker build -t definite_image -f Dockerfile.Step2 .

