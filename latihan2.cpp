#include<iostream>
using namespace std;

int main(){
    for(int i=0; i<=50; i++){
        if(i%4==0 && i%7==0){
            cout<<"BUZZPOP"<<endl;
        }  
        else if(i%4==0){
            cout<<"BUZZ"<<endl;
        }
        else if(i%7==0){
            cout<<"POP"<<endl;
        }
        else{
            cout<<i<<endl;
        }
         
    }
} 