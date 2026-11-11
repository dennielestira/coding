def _quiz_question(prompt, answer, wrong_answers, explanation):
    options = list(wrong_answers)
    correct_index = sum(map(ord, prompt)) % (len(options) + 1)
    options.insert(correct_index, answer)
    return {
        "question": prompt,
        "options": options,
        "correct_index": correct_index,
        "explanation": explanation,
    }


EXERCISES = {
    "python": [
        ("Build a List Comprehension", "List comprehensions create a new list by transforming each item.", "Create a squares list from numbers and print it.", "numbers = [1, 2, 3]\nsquares = [number ** 2 for number in numbers]\nprint(squares)", ["squares", "for", "**", "print"]),
        ("Sort Records by a Key", "A key function lets sorted() order records using a selected field.", "Sort the devices by name using sorted() and a lambda key.", 'devices = [{"name": "Mouse"}, {"name": "Keyboard"}]\nordered = sorted(devices, key=lambda device: device["name"])', ["sorted", "key", "lambda", "name"]),
        ("Use a Dictionary Default", "dict.get() returns a fallback value when a key is missing.", "Read the owner from a ticket dictionary and use Unknown when absent.", 'ticket = {"status": "Open"}\nowner = ticket.get("owner", "Unknown")', ["ticket", ".get(", "owner", "Unknown"]),
        ("Process Items with enumerate", "enumerate() provides each item and its index while looping.", "Print each device with a numbered index starting from 1.", 'devices = ["Laptop", "Monitor"]\nfor index, device in enumerate(devices, start=1):\n    print(index, device)', ["enumerate", "start=1", "for", "print"]),
        ("Use a Function Default", "A default parameter value makes an argument optional for a function caller.", "Define greet with a default name of Guest and return a greeting.", 'def greet(name="Guest"):\n    return f"Hello, {name}"', ["def greet", "Guest", "return"]),
        ("Handle Specific Input Errors", "Catching a specific exception handles an expected failure without hiding unrelated programming errors.", "Convert user text to an integer and handle ValueError with a clear message.", 'try:\n    count = int("12")\nexcept ValueError:\n    print("Enter a whole number")', ["try", "int(", "except ValueError", "print"]),
        ("Read a File Safely", "The with statement closes a file automatically after its block finishes.", "Open notes.txt as UTF-8 text and read its contents using with.", 'with open("notes.txt", encoding="utf-8") as file:\n    contents = file.read()', ["with open", "encoding", "as file", "read"]),
        ("Work with JSON Data", "The json module converts JSON text into Python values and Python values into JSON text.", "Import json, parse a JSON string, and read its name field.", 'import json\nrecord = json.loads(\'{"name": "Ari"}\')\nprint(record["name"])', ["import json", "json.loads", "name", "print"]),
        ("Create a Small Class", "A class groups data and behavior for objects that share the same structure.", "Create a Device class that stores a name passed to its initializer.", "class Device:\n    def __init__(self, name):\n        self.name = name", ["class Device", "__init__", "self.name"]),
        ("Test a Function Result", "A focused assertion checks that a function returns the expected value.", "Write a double function and assert that double(4) equals 8.", "def double(number):\n    return number * 2\n\nassert double(4) == 8", ["def double", "return", "assert", "== 8"]),
    ],
    "html": [
        ("Build an Accessible Form Group", "fieldset and legend group related controls and give them a shared label.", "Create a fieldset and legend for contact preferences, then add an email checkbox.", '<fieldset>\n  <legend>Contact preferences</legend>\n  <label><input type="checkbox" name="email"> Email</label>\n</fieldset>', ["<fieldset>", "<legend>", "type=\"checkbox\"", "Email"]),
        ("Add Table Header Scope", "The scope attribute clarifies which cells a table heading describes.", "Create a table column heading for Device with scope set to col.", '<table><tr><th scope="col">Device</th></tr></table>', ["<th", "scope=\"col\"", "Device"]),
        ("Provide Responsive Images", "srcset allows a browser to choose an appropriate image source for the display.", "Use an img element with srcset and useful alternative text.", '<img src="desk.png" srcset="desk-large.png 2x" alt="Desktop computer on a desk">', ["<img", "srcset", "alt="]),
        ("Group Related Inputs", "A fieldset and legend make a related group of form inputs easier to understand.", "Group two radio options under the legend Support channel.", '<fieldset>\n  <legend>Support channel</legend>\n  <label><input type="radio" name="channel" value="email"> Email</label>\n  <label><input type="radio" name="channel" value="chat"> Chat</label>\n</fieldset>', ["<fieldset>", "<legend>", "type=\"radio\"", "name=\"channel\""]),
        ("Show Completion Progress", "The progress element communicates completion of a task with a value and maximum.", "Show 3 of 5 setup steps using a progress element.", '<progress value="3" max="5">3 of 5</progress>', ["<progress", "value=\"3\"", "max=\"5\""]),
        ("Represent a Time or Date", "The time element can expose a machine-readable datetime along with readable text.", "Mark 9 AM on November 11, 2026 with a time element.", '<time datetime="2026-11-11T09:00">9 AM, November 11</time>', ["<time", "datetime=", "2026-11-11"]),
        ("Add Expandable Details", "details and summary create a native disclosure widget for optional supporting information.", "Create a details element whose summary is More information.", "<details>\n  <summary>More information</summary>\n  <p>Additional help text.</p>\n</details>", ["<details>", "<summary>", "</details>"]),
        ("Use a Download Link", "The download attribute can indicate that a linked resource should be downloaded.", "Link to guide.pdf with descriptive text and a download attribute.", '<a href="/files/guide.pdf" download>Download the setup guide</a>', ["href=", "download", "setup guide"]),
        ("Add a Figure Caption", "figure and figcaption associate a caption with an image, diagram, or other referenced content.", "Wrap an image and a descriptive caption in a figure.", "<figure>\n  <img src=\"ports.png\" alt=\"Common computer ports\">\n  <figcaption>Ports on the laptop</figcaption>\n</figure>", ["<figure>", "<figcaption>", "alt="]),
        ("Use Language Metadata", "The lang attribute helps browsers and assistive technology interpret page language.", "Set the document language to English on the html element.", '<html lang="en">', ["<html", "lang=\"en\""]),
    ],
    "css": [
        ("Build a Responsive Grid", "CSS Grid with minmax() and auto-fit can adapt the number of columns to available space.", "Create a grid of cards that fits columns at least 16rem wide.", ".cards {\n  display: grid;\n  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));\n}", ["display: grid", "auto-fit", "minmax(16rem", "1fr"]),
        ("Scale a Heading with clamp", "clamp() sets a fluid value with a minimum and maximum.", "Set h1 font size to scale between 2rem and 4rem.", "h1 {\n  font-size: clamp(2rem, 5vw, 4rem);\n}", ["font-size", "clamp(", "2rem", "4rem"]),
        ("Respect Reduced Motion", "The prefers-reduced-motion media feature lets a page reduce animation for users who request it.", "Disable smooth scrolling when reduced motion is preferred.", "@media (prefers-reduced-motion: reduce) {\n  html { scroll-behavior: auto; }\n}", ["@media", "prefers-reduced-motion", "scroll-behavior: auto"]),
        ("Add a Visible Focus Style", ":focus-visible provides a clear keyboard focus indicator without relying only on pointer hover.", "Give focused buttons a visible outline.", "button:focus-visible {\n  outline: 3px solid #2563eb;\n  outline-offset: 2px;\n}", [":focus-visible", "outline:", "outline-offset"]),
        ("Use a Container Query", "Container queries style a component according to its container size rather than the whole viewport.", "When .panel is at least 40rem wide, display .panel-content as two columns.", "@container (min-width: 40rem) {\n  .panel-content { display: grid; grid-template-columns: 1fr 1fr; }\n}", ["@container", "min-width: 40rem", "grid-template-columns"]),
        ("Create a Sticky Header", "Sticky positioning keeps an element in view after it reaches a specified scroll offset.", "Keep the site header at the top while scrolling.", "header {\n  position: sticky;\n  top: 0;\n  z-index: 10;\n}", ["position: sticky", "top: 0", "z-index"]),
        ("Use a CSS Custom Property", "Custom properties store reusable values and can be overridden for themes or components.", "Define a spacing variable on :root and use it for card padding.", ":root { --space-card: 1.25rem; }\n.card { padding: var(--space-card); }", ["--space-card", "var(--space-card)", "padding"]),
        ("Style a Component State", "Attribute selectors can style controls based on state or semantic attributes.", "Style a disabled button so it looks unavailable and cannot appear clickable.", "button:disabled {\n  opacity: 0.55;\n  cursor: not-allowed;\n}", ["button:disabled", "opacity", "cursor: not-allowed"]),
        ("Use a Layered Cascade", "@layer provides an explicit ordering for groups of CSS rules in the cascade.", "Create a components layer and add a .card rule inside it.", "@layer components {\n  .card { border-radius: 0.75rem; }\n}", ["@layer components", ".card", "border-radius"]),
        ("Add a Print Style", "A print media query can remove controls and simplify content for paper.", "Hide .navigation when the page is printed.", "@media print {\n  .navigation { display: none; }\n}", ["@media print", ".navigation", "display: none"]),
    ],
    "javascript": [
        ("Destructure an Object", "Destructuring assigns object properties to local variables using a concise syntax.", "Read the status property from a ticket object using destructuring.", 'const ticket = { status: "Open" };\nconst { status } = ticket;\nconsole.log(status);', ["ticket", "const { status }", "console.log"]),
        ("Use Optional Chaining", "Optional chaining safely reads a nested property when an earlier value may be null or undefined.", "Read city from a possibly missing user address.", "const city = user?.address?.city;", ["user?.address?.city", "const city"]),
        ("Use Nullish Coalescing", "The nullish coalescing operator supplies a fallback only for null or undefined values.", "Set displayName to the name or use Guest when name is missing.", 'const displayName = user.name ?? "Guest";', ["??", "Guest", "displayName"]),
        ("Create a Reusable Module", "ES modules let code export and import reusable values or functions across files.", "Export a formatStatus function from a JavaScript module.", 'export function formatStatus(status) {\n  return `Status: ${status}`;\n}', ["export function", "formatStatus", "return"]),
        ("Handle a Promise with async/await", "async functions and await provide a readable way to work with promise results.", "Write an async function that awaits a promise containing a status.", 'async function loadStatus() {\n  const status = await Promise.resolve("ready");\n  return status;\n}', ["async function", "await", "Promise.resolve", "return"]),
        ("Validate a Form Value", "Client-side checks can improve feedback, but important validation must also happen on the server.", "Check that an email input is not empty before continuing.", 'const email = document.querySelector("#email").value.trim();\nif (email.length > 0) {\n  console.log("Email provided");\n}', ["querySelector", ".value.trim()", "if", "length"]),
        ("Update a List in the DOM", "Creating elements with DOM methods and textContent avoids interpreting dynamic content as HTML.", "Create a list item, set its text with textContent, and add it to #results.", 'const item = document.createElement("li");\nitem.textContent = "Ready";\ndocument.querySelector("#results").append(item);', ["createElement", "textContent", "append"]),
        ("Use a Map for Keyed Data", "Map stores key-value pairs and provides methods such as set() and get().", "Store a device status in a Map and read it back by key.", 'const statuses = new Map();\nstatuses.set("printer", "online");\nconsole.log(statuses.get("printer"));', ["new Map", ".set(", ".get("]),
        ("Write a Small Unit Check", "A test checks expected behavior so later changes can be reviewed with confidence.", "Write a simple assertion that add(2, 3) returns 5.", "function add(a, b) { return a + b; }\nconsole.assert(add(2, 3) === 5);", ["function add", "console.assert", "=== 5"]),
        ("Handle a Failed Fetch", "Network requests can fail; check response status and handle errors rather than assuming success.", "Fetch /api/status and catch a network error.", 'fetch("/api/status")\n  .then(response => response.json())\n  .catch(error => console.error("Request failed", error));', ["fetch(", ".then(", ".catch(", "console.error"]),
    ],
    "sql": [
        ("Join Tickets to Requesters", "A join combines related rows using keys from each table.", "Select ticket subject and requester name by joining requester_id to users.id.", "SELECT tickets.subject, users.name\nFROM tickets\nJOIN users ON tickets.requester_id = users.id;", ["JOIN users", "requester_id", "users.id"]),
        ("Summarize by Status", "GROUP BY makes one result group per value, and aggregate functions summarize each group.", "Count tickets per status.", "SELECT status, COUNT(*)\nFROM tickets\nGROUP BY status;", ["COUNT(*)", "GROUP BY", "status"]),
        ("Filter Aggregate Results", "HAVING filters groups after GROUP BY has calculated aggregates.", "Show statuses with more than five tickets.", "SELECT status, COUNT(*)\nFROM tickets\nGROUP BY status\nHAVING COUNT(*) > 5;", ["GROUP BY", "HAVING", "COUNT(*) > 5"]),
        ("Use a CASE Expression", "CASE returns a value based on conditions and can create readable categories in query output.", "Label tickets as Urgent when priority is High, otherwise Standard.", "SELECT CASE WHEN priority = 'High' THEN 'Urgent' ELSE 'Standard' END AS urgency\nFROM tickets;", ["CASE", "WHEN", "ELSE", "END"]),
        ("Query with a Subquery", "A subquery uses the result of one query inside another query.", "Select tickets whose requester_id appears in the active users query.", "SELECT id FROM tickets\nWHERE requester_id IN (SELECT id FROM users WHERE active = 1);", ["IN (SELECT", "requester_id", "active = 1"]),
        ("Use a Common Table Expression", "A CTE names a temporary query result to make a larger query easier to read.", "Use a CTE named open_tickets to select open ticket IDs.", "WITH open_tickets AS (\n  SELECT id FROM tickets WHERE status = 'Open'\n)\nSELECT id FROM open_tickets;", ["WITH open_tickets", "SELECT id", "FROM open_tickets"]),
        ("Prevent Duplicate Values", "A UNIQUE constraint prevents duplicate values in a column or combination of columns.", "Create a unique index on users.email.", "CREATE UNIQUE INDEX idx_users_email ON users (email);", ["CREATE UNIQUE INDEX", "users", "email"]),
        ("Use a Transaction Safely", "A transaction groups statements so they can be committed together or rolled back.", "Begin a transaction, update one ticket, and commit.", "BEGIN;\nUPDATE tickets SET status = 'Closed' WHERE id = 12;\nCOMMIT;", ["BEGIN", "UPDATE tickets", "COMMIT"]),
        ("Filter with EXISTS", "EXISTS checks whether a subquery returns any rows and is useful for related-record checks.", "Find users who have at least one ticket.", "SELECT users.id FROM users\nWHERE EXISTS (SELECT 1 FROM tickets WHERE tickets.requester_id = users.id);", ["EXISTS", "requester_id", "SELECT 1"]),
        ("Review a Query Plan", "A query plan explains how a database intends to run a query; syntax differs by database engine.", "Show the query plan for a ticket status filter using SQLite syntax.", "EXPLAIN QUERY PLAN SELECT id FROM tickets WHERE status = 'Open';", ["EXPLAIN QUERY PLAN", "SELECT", "WHERE status"]),
    ],
    "php": [
        ("Use a Typed Function", "Parameter and return types document expectations and help detect incorrect values.", "Define a function that accepts an integer and returns an integer doubled.", "<?php\nfunction doubleValue(int $number): int {\n    return $number * 2;\n}", ["function doubleValue", "int $number", ": int", "return"]),
        ("Validate an Email", "Validation checks whether user input has the expected format before processing.", "<?php\n$email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);\nif ($email === false || $email === null) {\n    echo 'Enter a valid email';\n}", "Validate a posted email with filter_input and FILTER_VALIDATE_EMAIL.", ["filter_input", "INPUT_POST", "FILTER_VALIDATE_EMAIL"]),
        ("Escape Output for HTML", "Escaping user-provided text before placing it in HTML prevents the browser from treating it as markup.", "Output a name safely using htmlspecialchars with UTF-8.", "<?php\necho htmlspecialchars($name, ENT_QUOTES, 'UTF-8');", ["htmlspecialchars", "ENT_QUOTES", "UTF-8"]),
        ("Use a PDO Prepared Statement", "Prepared statements separate SQL structure from values and are the preferred way to pass user data into a query.", "Prepare a user lookup by email with a named parameter and execute it.", '$statement = $pdo->prepare("SELECT id FROM users WHERE email = :email");\n$statement->execute(["email" => $email]);', ["prepare(", ":email", "execute("]),
        ("Handle an Optional Form Field", "Null coalescing provides a fallback when a submitted form field is absent.", "Read an optional category field and default it to General.", "$category = $_POST['category'] ?? 'General';", ["$_POST", "??", "General"]),
        ("Catch a Specific Exception", "Catching an expected exception makes an error path explicit while avoiding broad, silent failure handling.", "<?php\ntry {\n    $result = performTask();\n} catch (RuntimeException $error) {\n    error_log($error->getMessage());\n}", "Catch RuntimeException and log its message.", ["try", "catch (RuntimeException", "error_log"]),
        ("Encode a JSON Response", "JSON encoding prepares structured data for an API response; check encoding errors in production code.", "<?php\nheader('Content-Type: application/json');\necho json_encode(['status' => 'ok']);", "Set a JSON content type and encode a status value.", ["Content-Type: application/json", "json_encode", "status"]),
        ("Use a DateTime Object", "DateTime objects provide explicit operations for representing and formatting dates.", "<?php\n$date = new DateTimeImmutable('now');\necho $date->format('Y-m-d');", "Create a DateTimeImmutable and format the date as year-month-day.", ["DateTimeImmutable", "->format", "Y-m-d"]),
        ("Read a File with a Clear Error Path", "File operations can fail, so check the result and report an explicit error rather than assuming success.", "<?php\n$content = file_get_contents('notes.txt');\nif ($content === false) {\n    throw new RuntimeException('Could not read notes');\n}", "Read notes.txt and check for a false result.", ["file_get_contents", "=== false", "RuntimeException"]),
        ("Organize Code in a Namespace", "Namespaces group related PHP classes and reduce naming collisions.", "<?php\nnamespace Academy\\Support;\n\nclass TicketFormatter {\n}", "Declare the Academy Support namespace and a TicketFormatter class.", ["namespace", "Academy", "class TicketFormatter"]),
    ],
    "linux-commands": [
        ("Find Recent Log Errors", "Combining find and grep can locate a pattern in selected log files; use a focused directory.", "Search /var/log for the word error in .log files.", "find /var/log -type f -name '*.log' -exec grep -i 'error' {} +", ["find /var/log", "-name '*.log'", "grep -i"]),
        ("Inspect a Service", "systemctl status reports whether a systemd service is active and includes recent status information.", "Check the status of the ssh service without changing it.", "systemctl status ssh", ["systemctl", "status", "ssh"]),
        ("Read Recent Service Logs", "journalctl can show logs for a specific service; limiting output keeps investigation focused.", "Show the latest 50 lines for the ssh service.", "journalctl -u ssh -n 50", ["journalctl", "-u ssh", "-n 50"]),
        ("Check Network Addresses", "ip address displays interfaces and assigned addresses, providing a read-only connectivity diagnostic.", "List IP addresses for network interfaces.", "ip address show", ["ip", "address", "show"]),
        ("Check Routes", "The route table helps identify the next hop a system uses for network traffic.", "Show the current IP route table.", "ip route show", ["ip", "route", "show"]),
        ("Check Disk Usage by Folder", "du estimates disk usage for files and directories; a summary helps identify large locations.", "Show a human-readable summary of /var/log disk usage.", "du -sh /var/log", ["du", "-sh", "/var/log"]),
        ("Find Large Files", "A targeted find command can locate large files for review before any cleanup is considered.", "Find regular files larger than 100 MB under /var.", "find /var -type f -size +100M -print", ["find /var", "-type f", "-size +100M"]),
        ("Inspect Running Processes", "ps can filter a process listing to help find a named service or application.", "Search the process list for ssh using a readable command.", "ps aux | grep '[s]sh'", ["ps aux", "|", "grep", "ssh"]),
        ("Check Package Updates", "Package manager commands can inspect update availability; use the distribution's approved workflow before installing.", "For Debian-based systems, refresh package metadata without installing packages.", "sudo apt update", ["apt", "update"]),
        ("Archive a Directory", "tar can package files for transfer or backup. Review paths and archive destinations before creating an archive.", "Create a compressed archive named logs.tar.gz from the logs directory.", "tar -czf logs.tar.gz logs/", ["tar", "-czf", "logs.tar.gz", "logs/"]),
    ],
    "git-and-github": [
        ("Review a Pull Request Diff", "A diff review checks the actual changes before they are shared or merged.", "Show the differences between the current branch and main.", "git diff main...HEAD", ["git diff", "main...HEAD"]),
        ("Stash Work Temporarily", "git stash saves uncommitted changes temporarily so the working tree can be used for another task.", "Stash tracked and untracked changes with a descriptive message.", 'git stash push -u -m "work in progress"', ["git stash push", "-u", "-m"]),
        ("Restore a Staged File", "git restore --staged unstages a file while leaving its working-tree changes intact.", "Unstage config.txt without discarding its edits.", "git restore --staged config.txt", ["git restore", "--staged", "config.txt"]),
        ("Fetch and Review Remote Branches", "Fetching updates remote references without merging them, allowing review before integration.", "Fetch updates from origin and list remote branches.", "git fetch origin\ngit branch -r", ["git fetch origin", "git branch -r"]),
        ("Compare Commit Changes", "git show displays a commit and its changes, which helps inspect a specific saved snapshot.", "Show the latest commit and its diff.", "git show --stat HEAD", ["git show", "--stat", "HEAD"]),
        ("Track a Release Tag", "Tags name a specific commit and are commonly used to mark releases.", "Create an annotated release tag named v2.0.0.", 'git tag -a v2.0.0 -m "Release 2.0.0"', ["git tag -a", "v2.0.0", "-m"]),
        ("Resolve a Merge Conflict Safely", "A conflict requires reviewing both versions and editing the file to the intended result before staging the resolution.", "After resolving a conflict in guide.md, stage only that file.", "git add guide.md", ["git add", "guide.md"]),
        ("Set a Local Branch Upstream", "An upstream links a local branch to its remote counterpart for convenient status and push operations.", "Push feature/help-page and set origin as its upstream.", "git push --set-upstream origin feature/help-page", ["git push", "--set-upstream", "origin", "feature/help-page"]),
        ("Ignore Local Build Output", "Ignore patterns keep generated or local-only files out of version control.", "Add build output and local environment settings to .gitignore.", "build/\n.env", ["build/", ".env"]),
        ("Verify the Working Tree Before a Commit", "Reviewing status and staged diffs helps keep a commit focused and avoids including unrelated files.", "Show status and review the staged diff before committing.", "git status\ngit diff --staged", ["git status", "git diff --staged"]),
    ],
}


def build_program_intermediate_lessons():
    for path_slug, exercises in EXERCISES.items():
        starter_code = {
            "python": "# Complete the intermediate activity",
            "html": "<!-- Complete the intermediate activity -->",
            "css": "/* Complete the intermediate activity */",
            "javascript": "// Complete the intermediate activity",
            "sql": "-- Complete the intermediate activity",
            "php": "<?php\n// Complete the intermediate activity",
            "linux-commands": "# Complete the intermediate activity",
            "git-and-github": "# Complete the intermediate activity",
        }[path_slug]
        for offset, (title, explanation, prompt, solution, keywords) in enumerate(exercises):
            number = offset + 1
            quiz = [
                _quiz_question(
                    f"What is the main purpose of {title.lower()}?",
                    explanation,
                    [
                        "It removes the need to review the result.",
                        "It changes unrelated system settings automatically.",
                    ],
                    explanation,
                ),
                _quiz_question(
                    f"What should you do for {title.lower()}?",
                    prompt,
                    [
                        "Skip the requested change and ignore the result.",
                        "Make unrelated edits without checking them.",
                    ],
                    f"The task is: {prompt}",
                ),
                _quiz_question(
                    "What is a good habit for intermediate practice?",
                    "Test the change and review the result before continuing.",
                    [
                        "Assume the first draft is correct without checking.",
                        "Hide all errors instead of understanding them.",
                    ],
                    "Testing a focused change helps identify problems early.",
                ),
            ]
            yield {
                "path": path_slug,
                "title": f"Intermediate: {title}",
                "slug": f"{path_slug}-intermediate-{number:02}",
                "short_description": explanation,
                "introduction": explanation,
                "explanation": explanation,
                "activity_type": "code",
                "activity_prompt": prompt,
                "activity_choices": [],
                "starter_code": starter_code,
                "expected_keywords": keywords,
                "hint": "Break the task into steps and check the syntax for this language.",
                "answer": solution,
                "solution": solution,
                "difficulty": "Intermediate",
                "order": 20 + number,
                "quiz": quiz,
            }
