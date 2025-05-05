# Google Calculator Test Cases

This document outlines the test cases for the Google Calculator component, accessible by searching "calculator" on Google. The calculator supports buttons `0-9`, `.`, `=`, `+`, `-`, `×`, `÷`, and `AC/CE`. Test cases are prioritized based on critical functionality, user impact, and likelihood of bugs. The automation suite (in `tests/test_calculator.py`) covers the top 7 test cases.

## Test Cases

| ID  | Test Case Name                       | Description                                                                 | Input                     | Expected Output | Priority | Implemented in Automation |
|-----|--------------------------------------|-----------------------------------------------------------------------------|---------------------------|-----------------|----------|---------------------------|
| TC01 | Basic Addition                      | Verify adding two positive integers yields the correct result.               | `2+3=`                    | `5`             | 1        | Yes                       |
| TC02 | Basic Subtraction                   | Verify subtracting two positive integers yields the correct result.          | `5-2=`                    | `3`             | 2        | Yes                       |
| TC03 | Basic Multiplication                | Verify multiplying two positive integers yields the correct result.          | `4×3=`                    | `12`            | 3        | Yes                       |
| TC04 | Basic Division                      | Verify dividing two positive integers yields the correct result.             | `8÷2=`                    | `4`             | 4        | Yes                       |
| TC05 | Clear Functionality (AC/CE)         | Verify the `AC/CE` button resets the calculator to its initial state.        | `7+3`, `AC/CE`, `1+1=`    | `2`             | 5        | Yes                       |
| TC06 | Decimal Addition                    | Verify adding two decimal numbers yields the correct result.                 | `1.5+2.5=`                | `4`             | 6        | Yes                       |
| TC07 | Complex Expression with Precedence  | Verify a complex expression respects operator precedence.                   | `10÷2+3×4-5=`             | `12`            | 7        | Yes                       |
| TC08 | Division by Zero                    | Verify the calculator handles division by zero appropriately.                | `5÷0=`                    | `Error` or `undefined` | 8 | No                        |
| TC09 | Negative Number Calculation         | Verify subtraction resulting in a negative number.                          | `3-5=`                    | `-2`            | 9        | No                        |
| TC10 | Large Number Calculation            | Verify the calculator handles large numbers correctly.                       | `999999+1=`               | `1000000`       | 10       | No                        |
| TC11 | Chained Operations                  | Verify chained operations work without pressing `=` until the end.           | `2+3+4=`                  | `9`             | 11       | No                        |
| TC12 | Zero Addition                       | Verify addition with zero.                                                  | `0+5=`                    | `5`             | 12       | No                        |
| TC13 | Multiple Decimal Points             | Verify the calculator handles multiple decimal points in a single number.    | `1..5+2=`                 | `3.5` or error  | 13       | No                        |
| TC14 | Leading Zeros                       | Verify that leading zeros are handled correctly.                            | `007+3=`                  | `10`            | 14       | No                        |
| TC15 | Empty Input                         | Verify the calculator handles pressing `=` without input.                    | `=`                       | `0` or no change | 15      | No                        |

## Notes
- **Priority**: Ranked from 1 (most important) to 15 (least important) based on critical functionality, user impact, edge case significance, and likelihood of bugs.
- **Implemented in Automation**: The top 7 test cases (TC01–TC07) are implemented in the Playwright-based automation suite (`tests/test_calculator.py`). Lower-priority test cases (TC08–TC15) can be added as needed.
- **Expected Output for TC08**: The exact output for division by zero (`Error` or `undefined`) depends on Google's implementation and should be verified before automating.
- **Expected Output for TC13**: The behavior for multiple decimal points (e.g., ignoring extra points or throwing an error) depends on the calculator's implementation.