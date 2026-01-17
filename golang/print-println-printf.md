# The Difference Between `fmt.Printf` | `fmt.Println` | `fmt.Print`

**Language:** <img src="https://skillicons.dev/icons?i=go" alt="Go" style="vertical-align: middle;" /> 


---

In Go, 
`fmt.Print`, `fmt.Printf`, `fmt.Println` are functions withing the `fmt` built-in package to output and Print the data to the console.
Each serves a distinct features

- ## `fmt.Print`
- Prints arguments with default formatting
- Add spaces only between arguments that are not strings
- No new line added 

- ### Usage example
```go
package main

import "fmt"

func main() {
    fmt.Print("Hello", " ", "World", 123) // Output: Hello World123
    fmt.Print("On the same line\n")       // Manually add a newline
}
```


- ## `fmt.Printf`
- f stands for **formatted** 
- Prints formatted output to the console using format specifiers like `%s` for strings or `%d` for integers
- No automatic spacing or newlines; You must manually add them (`\n`)

- ### Usage example
```go
package main

import "fmt"

func main() {
    name := "Bob"
    age := 30
    // Use format specifiers and manually add a newline \n
    fmt.Printf("%s is %d years old.\n", name, age)
    // Output: Bob is 30 years old.

    pi := 3.14159
    // Format a float to two decimal places
    fmt.Printf("Pi with two decimals: %.2f\n", pi)
    // Output: Pi with two decimals: 3.14
}
```


- ## `fmt.Println`
- The `ln` stands for **line** 
- Prints arguments with default formatting
- Automatically adds spaces between all the arguments 
- Atomatically adds a newline at the end

- ### Usage example
```go
package main

import "fmt"

func main() {
    fmt.Println("Hello", "World")
    // Output: Hello World
    // (with a newline at the end)

    fmt.Println(1, 2, 3)
    // Output: 1 2 3
    // (with a newline at the end)
}
```
