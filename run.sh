if [ -d "/path/to/dir" ]
then
    cd /home/ubuntu/mocking-spongebot
fi

docker build -t mocking-spongebot . && docker run -d mocking-spongebot