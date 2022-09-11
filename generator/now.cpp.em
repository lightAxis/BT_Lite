// this is autogen-code from @(here)
@# func_name = str
@# var = List[Variables]
@#       Variables = {name: str, type: str}

#include <stdio.h>
@{
pa1 = makeGen()
pa2 = make()
}
void @(func_name)@(pa1)
{
    printf("test\n");
    return;
}

int main(int argc, char **argv)
{
@[for var_ in var]@
    @(var_.type) @(var_.name);
@[end for]
    @(func_name)@(pa2);

    return 0;
}