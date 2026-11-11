BEGINNER_CHECKPOINTS = [
    "Identify the main parts and purpose",
    "Learn the key terms",
    "Check the normal status indicators",
    "Gather symptoms and user impact",
    "Read messages and error details",
    "Check connections and power safely",
    "Review settings before changing them",
    "Understand accounts and access",
    "Check available storage and resources",
    "Review updates and recent changes",
    "Use a low-risk diagnostic check",
    "Compare the issue with expected behavior",
    "Change one thing at a time",
    "Protect data before repair work",
    "Follow approved safety procedures",
    "Verify the result with the user",
    "Record findings in a clear ticket",
    "Know when to escalate a problem",
    "Review a common fault scenario",
    "Practice a complete troubleshooting sequence",
]

INTERMEDIATE_CHECKPOINTS = [
    "Compare current behavior with a known baseline",
    "Correlate symptoms with system logs",
    "Isolate one possible cause at a time",
    "Choose a controlled diagnostic test",
    "Assess compatibility and dependencies",
    "Plan a rollback before a risky change",
    "Interpret diagnostic results and limits",
    "Prioritize a problem by impact and urgency",
    "Escalate with evidence and actions already tried",
    "Verify a fix and document the outcome",
]

TRACK_CONTEXT = {
    "operating-systems": {
        "context": "Operating systems manage users, files, applications, device drivers, and computer resources.",
        "action": "Confirm the operating system, user scope, and relevant system status before changing settings.",
        "type": "concept",
    },
    "windows-troubleshooting": {
        "context": "Windows troubleshooting starts with the reported symptoms, scope, recent changes, and safe built-in diagnostics.",
        "action": "Ask when the issue began, record the exact message, and inspect the relevant Windows status before changing settings.",
        "type": "support",
    },
    "networking-fundamentals": {
        "context": "Networking depends on links, IP configuration, gateways, DNS, and the services users need to reach.",
        "action": "Check the physical or Wi-Fi link, IP configuration, and gateway in order, changing one variable at a time.",
        "type": "support",
    },
    "linux-troubleshooting": {
        "context": "Linux troubleshooting uses focused commands to inspect logs, services, permissions, processes, and storage.",
        "action": "Confirm the exact path or service and inspect status with a read-only command before making a privileged change.",
        "type": "support",
    },
    "software-installation": {
        "context": "Software installation requires an approved source, compatible version, authorization, licensing, and a verification plan.",
        "action": "Confirm the software is approved and compatible, then use a verified source and keep security protections enabled.",
        "type": "support",
    },
    "printer-troubleshooting": {
        "context": "Printer support checks power, connectivity, device status, supplies, queues, and drivers in a practical sequence.",
        "action": "Check printer status and connectivity, then review the queue without deleting another user's jobs.",
        "type": "support",
    },
    "computer-maintenance": {
        "context": "Preventive maintenance includes safe cleaning, backups, approved updates, airflow, and careful hardware handling.",
        "action": "Protect user data, power down and disconnect before cleaning, and follow the manufacturer's maintenance guide.",
        "type": "concept",
    },
    "help-desk-support": {
        "context": "Help desk work combines respectful communication, clear ticket notes, triage, follow-up, and escalation.",
        "action": "Acknowledge the user's impact, ask a focused question, and record the facts before proposing a change.",
        "type": "support",
    },
    "cybersecurity-awareness": {
        "context": "Security awareness protects accounts and devices through careful verification, reporting, and least-privilege habits.",
        "action": "Do not share credentials or follow an unexpected link; verify through a known channel and report concerns.",
        "type": "support",
    },
}


def build_track_lessons(path):
    settings = TRACK_CONTEXT[path.slug]
    track_name = path.title
    for level, topics, start_order in (
        ("Beginner", BEGINNER_CHECKPOINTS, 2),
        ("Intermediate", INTERMEDIATE_CHECKPOINTS, 21),
    ):
        for offset, topic in enumerate(topics):
            number = offset + 1
            order = start_order + offset
            answer = settings["action"]
            prompt = (
                f"Practice: {topic.lower()} in {track_name}. "
                "Which action is the best next step?"
            )
            wrong_options = [
                "Make several unrelated changes without recording the original settings.",
                "Delete user data or disable protections before checking the issue.",
            ]
            correct_index = (order + len(path.slug)) % 3
            options = wrong_options.copy()
            options.insert(correct_index, answer)
            questions = [
                {
                    "question": f"What is the focus of {track_name} topic {number} ({level.lower()})?",
                    "options": [
                        f"{topic} using {settings['context'].lower()}",
                        "Changing unrelated settings without checking the problem.",
                        "Skipping verification and user communication.",
                    ],
                    "correct_index": 0,
                    "explanation": f"This topic focuses on {topic.lower()}. {settings['context']}",
                },
                {
                    "question": f"What is a safe approach to {topic.lower()}?",
                    "options": options,
                    "correct_index": correct_index,
                    "explanation": answer,
                },
                {
                    "question": "What should happen after an approved troubleshooting change?",
                    "options": [
                        "Verify the result, record it, and tell the user what changed.",
                        "Make additional unrelated changes without testing.",
                        "Delete the ticket before confirming the issue is resolved.",
                    ],
                    "correct_index": 0,
                    "explanation": "Verification and clear notes show whether the change solved the reported issue.",
                },
            ]
            slug = f"{path.slug}-{level.lower()}-{number:02}"
            yield {
                "path": path.slug,
                "title": f"{level}: {topic}",
                "slug": slug,
                "short_description": f"Practice {topic.lower()} in {track_name.lower()}.",
                "introduction": (
                    f"This {level.lower()} lesson practices {topic.lower()}. "
                    f"{settings['context']} Use a safe, repeatable process and avoid "
                    "making changes before gathering relevant evidence."
                ),
                "explanation": (
                    f"{topic} is part of {track_name.lower()}. {settings['context']} "
                    "Start with a clear symptom and scope, use a low-risk diagnostic, "
                    "change one thing at a time, and verify the outcome."
                ),
                "activity_type": settings["type"],
                "activity_prompt": prompt,
                "activity_choices": options,
                "starter_code": "",
                "expected_keywords": [],
                "hint": "Choose the response that gathers evidence and follows an approved, low-risk process.",
                "answer": answer,
                "solution": (
                    f"The best answer is: {answer} "
                    "Avoid unrelated changes, protect user data, and verify the outcome before closing the ticket."
                ),
                "difficulty": level,
                "order": order,
                "quiz": questions,
            }
