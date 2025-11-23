E.md
+17
-1

# django
# django

This repository uses the `work` branch as its default. Some tools assume a `main` branch and will raise errors such as "Provided git ref main does not exist" when they cannot find it.

If you encounter that message:

1. Make sure you are on the `work` branch:
   ```bash
   git checkout work
   ```
2. If a tool specifically requires a `main` branch, create a local one that tracks `work`:
   ```bash
   git branch -f main work
   git checkout main
   ```

After creating the local `main` branch, rerun the command that previously failed.
