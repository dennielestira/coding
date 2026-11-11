from .hardware_curriculum import build_hardware_lessons
from .program_intermediate_curriculum import build_program_intermediate_lessons
from .programming_curriculum import build_program_lessons
from .curriculum import ADDITIONAL_LESSONS
from .models import LearningPath, Lesson, QuizQuestion
from .track_curriculum import TRACK_CONTEXT, build_track_lessons


def _ensure_program_topics():
    for item in build_program_lessons():
        path = LearningPath.objects.get(slug=item["path"])
        lesson_fields = {
            "path": path,
            "title": item["title"],
            "short_description": item["short_description"],
            "introduction": item["introduction"],
            "explanation": item["explanation"],
            "activity_type": item["activity_type"],
            "activity_prompt": item["activity_prompt"],
            "activity_choices": item["activity_choices"],
            "starter_code": item["starter_code"],
            "expected_keywords": item["expected_keywords"],
            "hint": item["hint"],
            "answer": item["answer"],
            "solution": item["solution"],
            "difficulty": item["difficulty"],
            "order": item["order"],
        }
        lesson, created = Lesson.objects.get_or_create(
            slug=item["slug"],
            defaults=lesson_fields,
        )
        if not created:
            for field, value in lesson_fields.items():
                setattr(lesson, field, value)
            lesson.save(update_fields=list(lesson_fields.keys()))

        for question_order, question_data in enumerate(item["quiz"]):
            question, created = QuizQuestion.objects.get_or_create(
                lesson=lesson,
                order=question_order,
                defaults=question_data,
            )
            if not created:
                for field, value in question_data.items():
                    setattr(question, field, value)
                question.save(update_fields=list(question_data.keys()))


def _ensure_hardware_topics():
    for item in build_hardware_lessons():
        path = LearningPath.objects.get(slug=item["path"])
        lesson_fields = {
            "path": path,
            "title": item["title"],
            "short_description": item["short_description"],
            "introduction": item["introduction"],
            "explanation": item["explanation"],
            "activity_type": item["activity_type"],
            "activity_prompt": item["activity_prompt"],
            "activity_choices": item["activity_choices"],
            "starter_code": item["starter_code"],
            "expected_keywords": item["expected_keywords"],
            "hint": item["hint"],
            "answer": item["answer"],
            "solution": item["solution"],
            "difficulty": item["difficulty"],
            "order": item["order"],
        }
        lesson, created = Lesson.objects.get_or_create(
            slug=item["slug"],
            defaults=lesson_fields,
        )
        if not created:
            for field, value in lesson_fields.items():
                setattr(lesson, field, value)
            lesson.save(update_fields=list(lesson_fields.keys()))

        for question_order, question_data in enumerate(item["quiz"]):
            question, created = QuizQuestion.objects.get_or_create(
                lesson=lesson,
                order=question_order,
                defaults=question_data,
            )
            if not created:
                for field, value in question_data.items():
                    setattr(question, field, value)
                question.save(update_fields=list(question_data.keys()))


def _save_seeded_lesson(item):
    path = LearningPath.objects.get(slug=item["path"])
    lesson_fields = {
        "path": path,
        "title": item["title"],
        "short_description": item["short_description"],
        "introduction": item["introduction"],
        "explanation": item["explanation"],
        "activity_type": item["activity_type"],
        "activity_prompt": item["activity_prompt"],
        "activity_choices": item.get("activity_choices", []),
        "starter_code": item.get("starter_code", ""),
        "expected_keywords": item.get("expected_keywords", []),
        "hint": item.get("hint", ""),
        "answer": item.get("answer", ""),
        "solution": item.get("solution", ""),
        "difficulty": item["difficulty"],
        "order": item["order"],
    }
    lesson, created = Lesson.objects.get_or_create(
        slug=item["slug"],
        defaults=lesson_fields,
    )
    if not created:
        for field, value in lesson_fields.items():
            setattr(lesson, field, value)
        lesson.save(update_fields=list(lesson_fields.keys()))

    for question_order, question_data in enumerate(item["quiz"]):
        question, created = QuizQuestion.objects.get_or_create(
            lesson=lesson,
            order=question_order,
            defaults=question_data,
        )
        if not created:
            for field, value in question_data.items():
                setattr(question, field, value)
            question.save(update_fields=list(question_data.keys()))


def _ensure_all_track_topics():
    for path in LearningPath.objects.filter(slug__in=TRACK_CONTEXT):
        beginner_count = path.lessons.filter(difficulty="Beginner").count()
        intermediate_count = path.lessons.filter(difficulty="Intermediate").count()
        for item in build_track_lessons(path):
            number = int(item["slug"].rsplit("-", 1)[-1])
            if item["difficulty"] == "Beginner" and number <= beginner_count:
                continue
            if item["difficulty"] == "Intermediate" and number <= intermediate_count:
                continue
            _save_seeded_lesson(item)


def _ensure_program_intermediate_topics():
    for item in build_program_intermediate_lessons():
        path = LearningPath.objects.get(slug=item["path"])
        number = int(item["slug"].rsplit("-", 1)[-1])
        if number <= path.lessons.filter(difficulty="Intermediate").count():
            continue
        _save_seeded_lesson(item)


def _ensure_additional_lessons():
    for item in ADDITIONAL_LESSONS:
        path = LearningPath.objects.get(slug=item["path"])
        lesson_fields = {
            "path": path,
            "title": item["title"],
            "short_description": item["short_description"],
            "introduction": item["introduction"],
            "explanation": item["explanation"],
            "activity_type": item["activity_type"],
            "activity_prompt": item["activity_prompt"],
            "activity_choices": item.get("activity_choices", []),
            "starter_code": item.get("starter_code", ""),
            "expected_keywords": item.get("expected_keywords", []),
            "hint": item.get("hint", ""),
            "answer": item.get("answer", ""),
            "solution": item.get("solution", ""),
            "difficulty": item["difficulty"],
            "order": item["order"],
        }
        lesson, created = Lesson.objects.get_or_create(
            slug=item["slug"],
            defaults=lesson_fields,
        )
        if not created:
            for field, value in lesson_fields.items():
                setattr(lesson, field, value)
            lesson.save(update_fields=list(lesson_fields.keys()))

        for question_order, question_data in enumerate(item["quiz"]):
            question, created = QuizQuestion.objects.get_or_create(
                lesson=lesson,
                order=question_order,
                defaults=question_data,
            )
            if not created:
                for field, value in question_data.items():
                    setattr(question, field, value)
                question.save(update_fields=list(question_data.keys()))


def _ensure_existing_knowledge_checks():
    questions = {
        "basic-html-page": {
            "question": "What do opening and closing HTML tags do?",
            "options": [
                "Mark the start and end of an element",
                "Connect the page to a database",
                "Set the computer's display resolution",
            ],
            "correct_index": 0,
            "explanation": "Most HTML elements use a start tag and an end tag around their content.",
        },
        "computer-wont-turn-on": {
            "question": "When should you inspect internal components?",
            "options": [
                "After external power checks and safe preparation",
                "Before checking the power outlet",
                "While the computer is connected to power",
            ],
            "correct_index": 0,
            "explanation": "Start with simple external checks and follow safe service procedures before internal work.",
        },
        "cpu-and-ram-basics": {
            "question": "Which component keeps data when the computer is turned off?",
            "options": ["An SSD or HDD", "RAM", "The CPU cache only"],
            "correct_index": 0,
            "explanation": "An SSD or HDD is persistent storage; RAM is temporary working memory.",
        },
        "understanding-ip-addresses": {
            "question": "What is one way a device can receive its IP configuration?",
            "options": ["Automatically from DHCP", "From the monitor", "By changing its keyboard layout"],
            "correct_index": 0,
            "explanation": "DHCP can automatically provide an IP address and related network settings.",
        },
        "strong-password-habits": {
            "question": "What should you do if you suspect an account password was exposed?",
            "options": [
                "Change it using the official service and report the incident",
                "Reuse it on another account",
                "Send it to coworkers for safekeeping",
            ],
            "correct_index": 0,
            "explanation": "Use the official account recovery process and follow your organization's incident reporting guidance.",
        },
    }

    for slug, question_data in questions.items():
        lesson = Lesson.objects.filter(slug=slug).first()
        if lesson is not None:
            QuizQuestion.objects.update_or_create(
                lesson=lesson,
                order=2,
                defaults=question_data,
            )


def _ensure_python_variables_lesson():
    path = LearningPath.objects.filter(slug="python").first()
    if path is None:
        return

    lesson, _ = Lesson.objects.get_or_create(
        slug="python-variables",
        defaults={
            "path": path,
            "title": "Python: Variables",
            "short_description": "Store a name in a variable and print its value.",
            "introduction": "A variable is a named place to store information while a program runs. This lesson practices storing a piece of text and displaying it.",
            "explanation": "A variable gives a value a reusable name. Use an assignment to store text, then pass the variable to Python's output function to display its current value. Text values need quotation marks; a variable reference does not. This makes it easy to update information in one place and reuse it.",
            "activity_type": "code",
            "activity_prompt": "Create a variable called name, store your name in it, then print the variable.",
            "starter_code": "# Create a variable called name, then print it.",
            "expected_keywords": ["name", "print"],
            "hint": "Assign a quoted text value to name, then call print(name) on a separate line.",
            "answer": "name = \"Alex\"\nprint(name)",
            "solution": "name = \"Alex\"\nprint(name)",
            "difficulty": "Beginner",
            "order": 2,
        },
    )
    lesson.explanation = (
        "A variable gives a value a reusable name. Use an assignment to store text, "
        "then pass the variable to Python's output function to display its current value. "
        "Text values need quotation marks; a variable reference does not. This makes it "
        "easy to update information in one place and reuse it."
    )
    lesson.save(update_fields=["explanation"])
    questions = [
        {
            "question": "What happens when you assign a text value to a variable?",
            "options": [
                "Stores the text Alex in the variable name",
                "Prints the word name",
                "Creates a new Python function",
            ],
            "correct_index": 0,
            "explanation": "The assignment binds the text value to the variable name so it can be reused.",
        },
        {
            "question": "What does Python's print function display when you pass it a variable?",
            "options": [
                "The value currently stored in name",
                "Always the word name",
                "The variable's memory address",
            ],
            "correct_index": 0,
            "explanation": "Without quotes, name refers to the variable, so print displays its current value.",
        },
        {
            "question": "If you change the value to \"Sam\", what should print(name) display?",
            "options": ["Sam", "Alex", "name"],
            "correct_index": 0,
            "explanation": "The print statement reads the current value, so changing the assignment changes the output.",
        },
    ]
    for order, question in enumerate(questions):
        quiz_question, _ = QuizQuestion.objects.get_or_create(
            lesson=lesson,
            order=order,
            defaults=question,
        )
        for field, value in question.items():
            setattr(quiz_question, field, value)
        quiz_question.save(update_fields=list(question.keys()))


def seed_database():
    if LearningPath.objects.exists():
        _ensure_python_variables_lesson()
        _ensure_additional_lessons()
        _ensure_existing_knowledge_checks()
        _ensure_program_topics()
        _ensure_hardware_topics()
        _ensure_all_track_topics()
        _ensure_program_intermediate_topics()
        return

    paths = [
        {"title": "Python", "slug": "python", "category": "programming", "description": "Learn core syntax, variables, inputs, loops, and functions in a beginner-friendly path.", "icon": "bi-code-slash"},
        {"title": "HTML", "slug": "html", "category": "programming", "description": "Build page structure, headings, forms, lists, and semantic layout with HTML.", "icon": "bi-filetype-html"},
        {"title": "CSS", "slug": "css", "category": "programming", "description": "Style pages using colors, spacing, layout, and responsive design techniques.", "icon": "bi-palette"},
        {"title": "JavaScript", "slug": "javascript", "category": "programming", "description": "Practice interaction, variables, conditionals, and user events with JavaScript.", "icon": "bi-filetype-js"},
        {"title": "SQL", "slug": "sql", "category": "programming", "description": "Query tables, filter data, and use basic joins to understand databases.", "icon": "bi-database"},
        {"title": "PHP", "slug": "php", "category": "programming", "description": "Learn web logic, forms, and server-side scripts with beginner-friendly examples.", "icon": "bi-filetype-php"},
        {"title": "Basic Linux Commands", "slug": "linux-commands", "category": "programming", "description": "Navigate files, use shell commands, and practice common Linux tasks.", "icon": "bi-terminal"},
        {"title": "Git and GitHub", "slug": "git-and-github", "category": "programming", "description": "Track changes, collaborate with others, and understand the Git workflow.", "icon": "bi-git"},
        {"title": "Computer Hardware", "slug": "computer-hardware", "category": "hardware", "description": "Understand CPUs, RAM, storage, power supply, and safe component handling.", "icon": "bi-cpu"},
        {"title": "Operating Systems", "slug": "operating-systems", "category": "it_support", "description": "Learn how Windows, macOS, and Linux manage files, users, and device drivers.", "icon": "bi-laptop"},
        {"title": "Windows Troubleshooting", "slug": "windows-troubleshooting", "category": "it_support", "description": "Identify common Windows issues such as login errors, blue screens, and startup problems.", "icon": "bi-tools"},
        {"title": "Networking Fundamentals", "slug": "networking-fundamentals", "category": "networking", "description": "Master IP addresses, subnets, gateways, and everyday connectivity problems.", "icon": "bi-router"},
        {"title": "Basic Linux Troubleshooting", "slug": "linux-troubleshooting", "category": "it_support", "description": "Diagnose package issues, permission errors, and common Linux service problems.", "icon": "bi-terminal-fill"},
        {"title": "Software Installation and Configuration", "slug": "software-installation", "category": "it_support", "description": "Install, configure, and troubleshoot common software applications safely.", "icon": "bi-install"},
        {"title": "Printer Troubleshooting", "slug": "printer-troubleshooting", "category": "it_support", "description": "Check queues, connectivity, drivers, and supply levels to solve printer issues.", "icon": "bi-printer"},
        {"title": "Computer Maintenance", "slug": "computer-maintenance", "category": "hardware", "description": "Keep devices healthy with updates, cleaning practices, backups, and preventive checks.", "icon": "bi-wrench"},
        {"title": "IT Help Desk and Customer Support", "slug": "help-desk-support", "category": "it_support", "description": "Practice communication, triage, ticket handling, and customer-ready support steps.", "icon": "bi-headset"},
        {"title": "Basic Cybersecurity and Security Awareness", "slug": "cybersecurity-awareness", "category": "security", "description": "Recognize phishing, protect passwords, and apply safe habits for online security.", "icon": "bi-shield-lock"},
    ]

    created_paths = {}
    for item in paths:
        created_paths[item["slug"]] = LearningPath.objects.create(
            title=item["title"],
            slug=item["slug"],
            category=item["category"],
            description=item["description"],
            icon=item["icon"],
            order=1,
        )

    lesson_data = [
        {
            "path": "python",
            "title": "Your First Python Program",
            "slug": "first-python-program",
            "short_description": "Learn how to display output and understand the basic structure of a Python script.",
            "introduction": "Python is a beginner-friendly programming language used in automation, data analysis, web development, and scripting. In this lesson, you will write your first program to display a message to the screen.",
            "explanation": "The print() function is one of the most important tools in Python. It sends text to the console, letting you check values and steps in a program. This is useful for debugging and simple output in training exercises.",
            "activity_type": "code",
            "activity_prompt": "Write a Python program that prints a welcome message for an IT learner.",
            "starter_code": "print(\"Hello, IT student!\")",
            "expected_keywords": ["print", "hello", "it"],
            "hint": "Use the print() function and include a short message such as 'Hello, IT student!'.",
            "answer": "print(\"Hello, IT student!\")",
            "solution": "print(\"Hello, IT student!\")\nprint(\"Welcome to IT Skills Academy!\")",
            "difficulty": "Beginner",
            "order": 1,
            "quiz": [
                {
                    "question": "What does the print() function do?",
                    "options": ["Displays text in the console", "Turns off the computer", "Deletes a file"],
                    "correct_index": 0,
                    "explanation": "print() shows information in the terminal or console so the user can see the output.",
                },
                {
                    "question": "Which of these is the correct Python syntax for a greeting?",
                    "options": ["print('Hello')", "echo 'Hello'", "show('Hello')"],
                    "correct_index": 0,
                    "explanation": "Python uses print() to display content to the console.",
                },
                {
                    "question": "Why is print() useful for beginners?",
                    "options": ["It helps check output from code", "It changes the language version", "It installs packages"],
                    "correct_index": 0,
                    "explanation": "print() allows beginners to see values and verify that their program is working as expected.",
                },
            ],
        },
        {
            "path": "html",
            "title": "Build a Basic HTML Page",
            "slug": "basic-html-page",
            "short_description": "Create a simple webpage structure with semantic headings and a paragraph.",
            "introduction": "HTML is the foundation of the web. It describes the structure of a page using elements such as headings, paragraphs, and links.",
            "explanation": "A browser reads HTML tags to decide how content should be displayed. For example, <h1> creates a main heading and <p> creates a paragraph. HTML is often the first skill a web developer learns.",
            "activity_type": "code",
            "activity_prompt": "Create a basic HTML page with a heading and a short paragraph.",
            "starter_code": "<h1>Welcome</h1>\n<p>This is my first webpage.</p>",
            "expected_keywords": ["<h1>", "<p>", "welcome"],
            "hint": "Use a heading tag and a paragraph tag, then add text inside them.",
            "answer": "<h1>Welcome</h1>\n<p>This is my first webpage.</p>",
            "solution": "<h1>Welcome</h1>\n<p>This is my first webpage.</p>",
            "difficulty": "Beginner",
            "order": 1,
            "quiz": [
                {
                    "question": "What does HTML stand for?",
                    "options": ["HyperText Markup Language", "Home Tool Markup Language", "High Text Management Language"],
                    "correct_index": 0,
                    "explanation": "HTML is the markup language used to structure web pages.",
                },
                {
                    "question": "Which tag is used for the main page heading?",
                    "options": ["<h1>", "<header>", "<title>"],
                    "correct_index": 0,
                    "explanation": "<h1> is the largest heading tag and usually marks the main topic of a web page.",
                },
            ],
        },
        {
            "path": "windows-troubleshooting",
            "title": "Computer Won't Turn On",
            "slug": "computer-wont-turn-on",
            "short_description": "Practice the first steps to troubleshoot a PC that won't power on.",
            "introduction": "When a computer does not turn on, the safest first move is to check the power path before opening the case. A good technician checks simple items first and then works toward deeper hardware issues.",
            "explanation": "The most common causes are a loose power cable, no power at the outlet, a tripped wall switch, or a faulty power supply. Diagnosing in order can save time and prevent unnecessary repairs.",
            "activity_type": "support",
            "activity_prompt": "The computer is completely dead. What should the technician check first?",
            "activity_choices": ["Check the power cable and outlet first", "Reinstall the operating system", "Replace the RAM immediately", "Ignore the issue and restart later"],
            "hint": "Start from the easiest and most common external power checks, not the internal components.",
            "answer": "Check the power cable and outlet first",
            "solution": "The first step is to verify the power source: the power cable is firmly connected, the outlet works, and the power strip or surge protector is on. Only after that should you inspect power buttons, LEDs, and internal components such as the PSU.",
            "difficulty": "Beginner",
            "order": 1,
            "quiz": [
                {
                    "question": "What should you check before opening the computer case?",
                    "options": ["Power cable and wall outlet", "CPU fan speed", "Hard drive partition", "Operating system license"],
                    "correct_index": 0,
                    "explanation": "External power checks are the fastest and safest place to begin.",
                },
                {
                    "question": "Why is checking simple power issues first important?",
                    "options": ["It is fast, safe, and often solves the problem", "It is the only method allowed by the BIOS", "It avoids the need to use a screwdriver"],
                    "correct_index": 0,
                    "explanation": "Many no-power issues are caused by loose cables or absent power, which are easy to confirm before deeper troubleshooting.",
                },
            ],
        },
        {
            "path": "computer-hardware",
            "title": "CPU and RAM Basics",
            "slug": "cpu-and-ram-basics",
            "short_description": "Understand the two most important parts that influence how a computer runs.",
            "introduction": "The central processing unit, or CPU, handles instructions, while RAM stores data the system needs right now. Together, they determine how quickly and smoothly a computer runs tasks.",
            "explanation": "A CPU is like the brain of the computer. RAM is short-term memory. If a system has too little RAM, it may slow down or freeze. If the CPU has a problem, the machine may behave oddly or fail to boot.",
            "activity_type": "concept",
            "activity_prompt": "What is the main purpose of RAM in a computer?",
            "activity_choices": ["To store files permanently", "To temporarily hold active data for fast access", "To connect the monitor to the CPU", "To generate electricity"],
            "hint": "Think of RAM as temporary workspace for active tasks, not long-term storage.",
            "answer": "To temporarily hold active data for fast access",
            "solution": "RAM stores the files and instructions the operating system and programs are actively using. It is fast, but it is temporary. Permanent storage such as an SSD or HDD keeps data even when the computer is off.",
            "difficulty": "Beginner",
            "order": 1,
            "quiz": [
                {
                    "question": "What does the CPU do?",
                    "options": ["Processes instructions", "Saves data permanently", "Stores Wi-Fi passwords", "Controls printer paper"],
                    "correct_index": 0,
                    "explanation": "The CPU executes instructions and performs calculations.",
                },
                {
                    "question": "Which component is more like temporary working memory?",
                    "options": ["RAM", "SSD", "Motherboard", "Power cable"],
                    "correct_index": 0,
                    "explanation": "RAM keeps active data near the CPU for quick access while the computer is running.",
                },
            ],
        },
        {
            "path": "networking-fundamentals",
            "title": "Understanding IP Addresses",
            "slug": "understanding-ip-addresses",
            "short_description": "Learn how devices use IP addresses to communicate on a network.",
            "introduction": "Every device on a network needs an address so it can send and receive information. IP addresses work a bit like mailing addresses for data.",
            "explanation": "A device with an IP address can be reached on the network. It may be assigned automatically by DHCP or manually by an administrator. When a device cannot reach the network, problems often involve the IP address, subnet mask, or gateway.",
            "activity_type": "support",
            "activity_prompt": "A user cannot connect to the network. What should you check first?",
            "activity_choices": ["Check whether the device has a valid IP address and is connected to the network", "Reinstall the browser", "Install a new keyboard", "Restart the printer"],
            "hint": "Before troubleshooting applications, confirm the device is connected and properly configured on the network.",
            "answer": "Check whether the device has a valid IP address and is connected to the network",
            "solution": "Networking starts with connectivity. If the device has no IP address, the wrong subnet, or no link status, then applications and internet access may fail even though the user thinks the service is okay.",
            "difficulty": "Beginner",
            "order": 1,
            "quiz": [
                {
                    "question": "What does an IP address help a device do?",
                    "options": ["Identify itself on a network", "Store web pages", "Charge a battery", "Create a Wi-Fi password"],
                    "correct_index": 0,
                    "explanation": "An IP address identifies a device on a network so data can be sent to the right place.",
                },
                {
                    "question": "What is a common network issue?",
                    "options": ["No IP address or bad connection", "A missing keyboard driver", "An empty recycle bin", "No audio card"],
                    "correct_index": 0,
                    "explanation": "Network problems often involve connectivity, DHCP, or misconfigured addressing rather than the application itself.",
                },
            ],
        },
        {
            "path": "cybersecurity-awareness",
            "title": "Strong Password Habits",
            "slug": "strong-password-habits",
            "short_description": "Learn how to protect accounts with strong, memorable passwords and safe habits.",
            "introduction": "Cybersecurity begins with simple habits. A weak password can allow attackers to access bank accounts, school accounts, and personal files.",
            "explanation": "Strong passwords are long, unique, and not reused across accounts. A password manager can help store them securely. Avoid sharing passwords or clicking suspicious links in emails.",
            "activity_type": "code",
            "activity_prompt": "Create a short password policy example that encourages secure habits.",
            "starter_code": "Use at least 12 characters and never reuse passwords.",
            "expected_keywords": ["12", "never", "reuse", "password"],
            "hint": "Describe a simple policy that includes length and uniqueness.",
            "answer": "Use at least 12 characters and never reuse passwords.",
            "solution": "Use a unique password with at least 12 characters, including a mix of letters, numbers, and symbols. Never reuse the same password across accounts and do not send it over email.",
            "difficulty": "Beginner",
            "order": 1,
            "quiz": [
                {
                    "question": "Why should passwords be unique?",
                    "options": ["So one breach does not affect every account", "Because the computer asks for it", "Because every password must be short", "Because browsers require it"],
                    "correct_index": 0,
                    "explanation": "Unique passwords reduce the risk that a single compromised account exposes several services.",
                },
                {
                    "question": "What is a common cybersecurity risk?",
                    "options": ["Phishing emails and fake links", "Using too many fonts", "Typing in uppercase letters", "Updating software too often"],
                    "correct_index": 0,
                    "explanation": "Phishing is when attackers trick users into giving up passwords or personal information.",
                },
            ],
        },
    ]

    for item in lesson_data:
        path = created_paths[item["path"]]
        lesson = Lesson.objects.create(
            path=path,
            title=item["title"],
            slug=item["slug"],
            short_description=item["short_description"],
            introduction=item["introduction"],
            explanation=item["explanation"],
            activity_type=item["activity_type"],
            activity_prompt=item["activity_prompt"],
            activity_choices=item.get("activity_choices", []),
            starter_code=item.get("starter_code", ""),
            expected_keywords=item.get("expected_keywords", []),
            hint=item.get("hint", ""),
            answer=item.get("answer", ""),
            solution=item.get("solution", ""),
            difficulty=item["difficulty"],
            order=item["order"],
        )
        for q_index, q_data in enumerate(item["quiz"]):
            QuizQuestion.objects.create(
                lesson=lesson,
                order=q_index,
                question=q_data["question"],
                options=q_data["options"],
                correct_index=q_data["correct_index"],
                explanation=q_data["explanation"],
            )
    _ensure_python_variables_lesson()
    _ensure_additional_lessons()
    _ensure_existing_knowledge_checks()
    _ensure_program_topics()
    _ensure_hardware_topics()
    _ensure_all_track_topics()
    _ensure_program_intermediate_topics()
