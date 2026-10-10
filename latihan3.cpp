#include<iostream>
using namespace std;
long long pangkat(int a, int b){
    long long hasil = 1;
    for(int i=0; i<b; i++){
        hasil *= a;
    }
    return hasil;
}
int main(){
    int a, b;
    cout<<"Masukkan basis: ";
    cin>>a;
    cout<<"Masukkan pangkat: ";
    cin>>b;
    cout<<"Hasil: "<<pangkat(a, b)<<endl;
} 