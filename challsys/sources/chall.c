#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int getFood(int a) {
  a = a & 0xf001b001;
  return a ^ 0x445f0410;
}

int main()
{
  const int pass = 0xf00df00d; 
  char* flag = "pass: f00df00d";
  int check = 0x12345678;
  char buffer[30];
  fgets(buffer,48,stdin);

  printf("[check] 0x%x\n", check);

  if (check==0xf00df00d)
   {
     printf("You're getting on the right way but you're missing something!\n");
   }

  if (check == getFood(0xf00df00d))
   {
     printf("You Win! Congratulations!!\n");
     system("cat flag");
   }

  if (strcmp(buffer,"f00df00d\n")==0)
   {
     printf("This challenge is easy but not to that point!\n");   
   }

   return 0;
}
