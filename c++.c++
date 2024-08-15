#include <iostream>

int main()
{
    int x;
    int y;
    int z;
    
    float  m;

    std::cout<< "digite sua nota da primeira prova";
    std::cin >>(x);

    std::cout << "digite sua nota da segunda prova";
    std::cin>>(y);

    std::cout<<"digite a sua nota da terceira prova";
    std::cin>>(z);

    m=(x+y+z)/3;

    std::cout<<"A sua media e\n";
    std::cout<< (m);


}
() return 0;