
General advice for git and python coding:

### Coding & Git etiquette

#### Code
1. Please write in PEP-8 (auto-formatter <3)
2. Please use type-hinting as much as possible
3. Preferable to use a one-line doc-string to document a function
4. Please use the __ prefix to indicate private variables.
5. Please use the following import order:
```python
import a_standard
import b_standard

import a_third_party
import b_third_party

from a_soc import f
from a_soc import g
from b_soc import d
```
[source](https://stackoverflow.com/a/20763446)
### Github
1. Think of a commit message as "This commit I will []", e.g. git commit -m "add README.md"
2. For teams: (Taken from boot.dev), should also work on gitlab.
When you're working with a  _team_, Git gets a bit more involved (and we'll cover more of this in part 2 of this course). Here's what I do:

-   Update my local  `main`  branch with  `git pull origin main`
-   Checkout a new branch for the changes I want to make with  `git switch -c <branchname>`
-   Make changes to files
-   `git add .`
-   `git commit -m "a message describing the changes"`
-   `git push origin <branchname>`  (I push to the  _new_  branch name, not  `main`)
-   Open a  [pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/about-pull-requests)  on GitHub to merge my changes into  `main`
-   Ask a team member to review my pull request
-   Once approved, click the "Merge" button on GitHub to merge my changes into  `main`
-   Delete my feature branch, and repeat with a new branch for the next set of changes