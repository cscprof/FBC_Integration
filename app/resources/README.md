# Welcome to the Resources/Partner Blueprint

Most everything you need to know can be found within comments, but a general guide for how we suggest you go through the folder can be found here, as well as a to‑do list to pick up where we left off.

---

## Suggested First‑Time Traversal

| File | Description |
|------|-------------|
| **views.py** | Holds several routes for the resource and partner directory. In addition to page rendering, it contains the code for many of the interactive admin buttons. |
| **__init__.py** | Rarely needs editing. Worth a quick look if you want to ensure everything checks out under the hood. |
| **models.py** | Second most important file. Uses SQLAlchemy to access the database. This makes coding queries in `views.py` incredibly easy, but an accurate form of the database must exist in `views.py`. Import tables as any other Python module; a mismatch between `models.py` and the real database schema will break the connection. If correct, you’ll get automatic error checking on your SQL queries within a Python IDE. |
| **AddResource.xlsx** | Spreadsheet template to help add resources en masse. Slightly outdated (see To‑Do), but with one small adjustment it can be used or sent to other organizations so they can add their resources. |
| **categoryReplacement.py** | Independent program that can be used with the AddResource spreadsheet. The `resourceCategory` column in AddResource is a human‑readable dropdown; this script converts it to an integer before importing into the database. Given a CSV file as input, it outputs the same document with `resourceCategory` translated to an integer. |
| **resourceDirectory.html** | Landing page for the resource directory. Displays all categories as clickable links. Each link leads to `resourcesearch.html` with the category automatically selected. Both this page and `resourcesearch.html` have an “Add Resource” button for quick access, visible only to admins (code in `views.py`). |
| **resourcesearch.html** | Main resource directory. Automatically pulls all resources from the database and displays them. Resources can be sorted via a dropdown menu or searched via the search bar. The dropdown automatically sets itself to whichever category was selected on `resourceDirectory.html`. Each resource has an edit button, visible only to admins. |
| **admin.html** | Accessible only by admin users. Provides the same functionality as the add and edit buttons on other pages. |
| **partners.html / partners_admin.html** | Works like `resourcesearch` and `admin`, but for partners. |

---

## Full Process for Adding Resources via **AddResource.xlsx**

1. **Fill out all fields** on the spreadsheet for a given resource  
   1. Ensure every field is filled; even non‑required fields must be marked `"NULL"`.  
2. **Download the spreadsheet as CSV**.  
   1. For resources specifically, the names of the resource categories must either be changed manually or via `categoryReplacement.py`.  
3. **Import the data to the database** – column labels are automatically skipped.  
   1. For resource tags, `resourceTagID` will increment automatically; do not select it when importing that CSV.

---

## To‑Do

1. **Add “Profile Picture” to the partners page**  
   * The database table already has a field for a profile picture (essentially a logo). It currently has no practical application. Each entry on the partners page should have the option to display the partner’s logo.  

2. **Make partners more prominent on the page**  
   * At minimum, each partner box should extend to fill the whole width instead of being two columns like the resources.

3. **Link partners back to resources on the resource directory**  
   * This should include at least:  
     - The partner’s name  
     - Their logo  
     - A clickable portion that links to their website

---

If you have any questions and you aren't Ben Shuck, ask him. Or ask Prof. Madeira, he's smart. If we have somehow created an amalgamation that cannot be understood by another human, then feel free to shoot me a text.

### Owen Bacon
(330) 429-1794