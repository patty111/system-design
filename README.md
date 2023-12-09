# URL Shortener
May take a while to start the server

read/write ratio should be 100/1

short url key length: 8

how to shorten url?
1. random id or uuid
-> need to check frequently to prevent collisions -> bottleneck

2. hashing(md5, sha)
   
3. counter->token range