#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> nums = {4, 1, 7, 3};
    int sum = 0;
    for (int x : nums) sum += x;
    cout << "Sum = " << sum << endl;
    cout << "Average = " << (double)sum / nums.size() << endl;
    return 0;
}
