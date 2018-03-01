### Challsys (system) : easy

#### Description

You have the binary named "chall". Find a way to retrieve the flag.
We also provide a part of the source code:

```
/*
**************
 Missing code
**************
*/

  int check = 0x12345678;
  char buffer[30];
  fgets(buffer,40,stdin);
  printf("[check] 0x%x\n", check);

/*
**************
 Missing code
**************
*/
```

The source code is compiled using this command `gcc -m32 -fno-stack-protector -mpreferred-stack-boundary=2 chall.c -o chall`.

#### To run

```
docker pull mbeldi/challsys
docker run -d -p 32700:22 --name <container_name> --previleged mbeldi/challsys
ssh thc18@localhost -p 32700 (password: thc18)
```
