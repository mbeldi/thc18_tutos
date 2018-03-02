### flip the birde (crypto) : intermediate

#### Description
```
nc localhost 41222
```

Message is encrypted with AES-128-CBC with unknown key and IV.
Your task is to modify the ciphertext!
To bypass the authentication, the plaintext must contain 'admin=true;'.

#### To run
```
docker pull izharr/flip-the-birde
docker run -d --name <container_name> -p 41222:41222 izharr/flip-the-birde
```

