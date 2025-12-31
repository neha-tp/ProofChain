let numbers = [3, 7, 2, 9, 5];

let squared = numbers.map(n => n * n);

let sum = squared.reduce((a, b) => a + b, 0);

console.log("Squared array:", squared);

console.log("Sum of squares:", sum);

let max = Math.max(...numbers);

console.log("Maximum number:", max);
