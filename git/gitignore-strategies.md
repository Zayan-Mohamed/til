# .gitignore Best Practices: Root vs. Multiple Files

Should you use one giant `.gitignore` or scatter them across directories?

## The Rule of Thumb
**Stick to a single root `.gitignore`** for standard projects. It centralizes configuration and prevents "hunting" for hidden rules.

## Exceptions (When to use multiple)
1.  **Monorepos:** If a subdirectory is an independent project (e.g., `packages/client` vs `packages/server`), give it its own `.gitignore` to keep it self-contained.
2.  **Forcing Empty Directories:** Git ignores empty folders. To commit a `logs/` folder without tracking its contents, place a `.gitignore` inside it:
    ```gitignore
    # Ignore everything inside
    *
    # Except this file
    !.gitignore
    ```
3.  **Generated Code:** If a CLI tool generates a folder with its own `.gitignore`, leave it alone.

## Debugging Trick
Not sure which file is ignoring your code?
```bash
git check-ignore -v path/to/file
# Output: .gitignore:23:node_modules    path/to/file
