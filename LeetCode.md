# LeetCode刷题总结
## 数组用法
```c++
//元素交换
swap(a[1], a[3]);
//数组颠倒
reverse(a.begin(), a.end());
//数组元素置为0
memset(a, 0, a.size());
//数组取值
a.push_back();
//定义二维数组
vector< vector<int> > result
```
## set集合的用法
集合中没有重复元素
``` c++
//定义一个int类型的集合
set<int> s;
set<int>::iterator it;
//插入元素10（插入的数值默认从小到大排序）
s.insert(10);
//删除元素10
s.erase(10);
//清空集合
s.clear();
//集合元素的个数
s.size();
//判断集合是否为空
s.empty();
//查找集合中是否与元素10，有的话返回10，没有则返回s.end()
it = s.find(10);
//
```
mutiset：多重集合与set最大的区别是它可以插入重复元素，如果删除的话，相同的会一起删除，如果查找的话，返回该元素的迭代器的位置，若有相同，返回第一个元素的地址，其它使用和set基本类似。
## 字符串
```c++
//排序
sort(a.begin(), a.end());
//将所有字符转换成小写
transform(s.begin(), s.end(), s.begin(),::tolower);
//截取字符串
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char* argv[])
{
    string name("rockderia");
    string firstname(name.substr(0,4));
    cout << firstname << endl;

    system("pause");
}
```
## 运算
异或（^）：二进制数进行运算相同为0，不同为1
与运算（&）：同时为1，才为1；
或运算（|）：同时为0，才为0；
取反（~）
左移（<<）：左边的二进制丢失，右边补0，左移最高位不包括1，左移相当于该数乘2；
右移（>>）:正数左补0，负数左补1
不同长度的数据进行位运算时，系统会自动补齐。
## 栈
栈具有先进后出的特性
