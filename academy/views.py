import re
from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CodeSubmissionForm
from .models import LearningPath, Lesson

PROGRAMMING_EXAMPLES = {
    "python": ("Python: display a message", 'message = "Hello, learner!"\nprint(message)'),
    "html": ("HTML: add a paragraph", "<p>Welcome to the learning lab.</p>"),
    "css": ("CSS: style a paragraph", "p {\n  color: #3659d9;\n}"),
    "javascript": (
        "JavaScript: log a message",
        'const message = "Hello, learner!";\nconsole.log(message);',
    ),
    "sql": ("SQL: read a value", "SELECT 'Hello, learner!' AS message;"),
    "php": ("PHP: display a message", '<?php\n$message = "Hello, learner!";\necho $message;'),
    "linux-commands": ("Linux: inspect the current folder", "pwd\nls"),
    "git-and-github": ("Git: check your changes", "git status"),
}


def _session_state(request):
    state = request.session.get(
        "learning_state",
        {
            "completed": [],
            "activities": [],
            "attempts": [],
            "quiz_scores": {},
            "quiz_correct": {},
            "lesson_steps": {},
            "quiz_positions": {},
            "study_days": [],
        },
    )
    state.setdefault("completed", [])
    state.setdefault("activities", [])
    state.setdefault("attempts", [])
    state.setdefault("quiz_scores", {})
    state.setdefault("quiz_correct", {})
    state.setdefault("lesson_steps", {})
    state.setdefault("quiz_positions", {})
    state.setdefault("study_days", [])
    return state


def _record_study_day(state):
    today = timezone.localdate().isoformat()
    if today not in state["study_days"]:
        state["study_days"].append(today)


def _check_code_submission(lesson, submitted_code):
    if lesson.slug == "python-variables":
        assignment = re.search(
            r"""(?m)^\s*name\s*=\s*(['"])(.*?)\1\s*$""", submitted_code
        )
        prints_name = re.search(
            r"(?m)^\s*print\s*\(\s*name\s*\)\s*$", submitted_code
        )
        output = assignment.group(2) if assignment and prints_name else None
        missing = []
        if not assignment:
            missing.append('an assignment such as name = "Alex"')
        if not prints_name:
            missing.append("print(name)")
        return bool(output), output, missing

    normalized = " ".join(submitted_code.lower().split())
    expected_keywords = [keyword.lower() for keyword in lesson.expected_keywords]
    missing = [
        keyword
        for keyword, normalized_keyword in zip(lesson.expected_keywords, expected_keywords)
        if normalized_keyword not in normalized
    ]
    return bool(expected_keywords) and not missing, None, missing


def dashboard(request):
    paths = LearningPath.objects.order_by("category", "order")
    state = _session_state(request)
    valid_lesson_slugs = set(Lesson.objects.values_list("slug", flat=True))
    completed = set(state["completed"]) & valid_lesson_slugs
    total_lessons = len(valid_lesson_slugs)
    completed_lessons = len(completed)
    progress_percentage = round(completed_lessons / total_lessons * 100) if total_lessons else 0

    active_days = {
        date.fromisoformat(day)
        for day in state["study_days"]
        if day
    }
    streak = 0
    current_day = timezone.localdate()
    while current_day in active_days:
        streak += 1
        current_day -= timedelta(days=1)

    latest_score = state["quiz_scores"].get("latest")
    skill_score = latest_score["percentage"] if latest_score else None
    python_variables_lesson = Lesson.objects.filter(slug="python-variables").first()
    continue_lesson = (
        python_variables_lesson
        if python_variables_lesson and python_variables_lesson.slug not in completed
        else Lesson.objects.exclude(slug__in=completed).first() or Lesson.objects.first()
    )

    learning_tracks = [
        {
            "title": "Programming and Coding",
            "description": "Learn Python, HTML, CSS, JavaScript, SQL, and Git through short lessons and coding challenges.",
            "icon": "bi-code-slash",
            "theme": "track-programming",
            "paths": paths.filter(category="programming"),
            "goal": "Build coding skills",
        },
        {
            "title": "IT Support and Troubleshooting",
            "description": "Practice diagnosing computer problems, Windows errors, network issues, printer problems, and software installation.",
            "icon": "bi-tools",
            "theme": "track-support",
            "paths": paths.filter(category__in=["it_support", "security"]),
            "goal": "Build job-ready skills",
        },
        {
            "title": "Hardware and Networking",
            "description": "Learn computer components, maintenance, IP addresses, routers, switches, and basic networking.",
            "icon": "bi-cpu",
            "theme": "track-hardware",
            "paths": paths.filter(category__in=["hardware", "networking"]),
            "goal": "Build technical knowledge",
        },
    ]

    return render(
        request,
        "dashboard.html",
        {
            "learning_tracks": learning_tracks,
            "continue_lesson": continue_lesson,
            "total_lessons": total_lessons,
            "completed_lessons": completed_lessons,
            "progress_percentage": progress_percentage,
            "streak": streak,
            "skill_score": skill_score,
        },
    )


def reset_progress(request):
    if request.method != "POST":
        return redirect("dashboard")

    request.session.pop("learning_state", None)
    messages.success(request, "All lesson progress has been reset. You can start again.")
    return redirect("dashboard")


def path_index(request):
    paths = LearningPath.objects.order_by("category", "order")
    return render(request, "paths.html", {"paths": paths})


def path_detail(request, slug):
    path = get_object_or_404(LearningPath, slug=slug)
    lessons = path.lessons.all()
    completed_lessons = set(_session_state(request)["completed"])
    completed_count = sum(lesson.slug in completed_lessons for lesson in lessons)
    total_lessons = len(lessons)
    progress_percentage = (
        round(completed_count / total_lessons * 100) if total_lessons else 0
    )
    return render(
        request,
        "path_detail.html",
        {
            "path": path,
            "lessons": lessons,
            "completed_lessons": completed_lessons,
            "completed_count": completed_count,
            "progress_percentage": progress_percentage,
        },
    )


def lesson_detail(request, slug):
    lesson = get_object_or_404(Lesson, slug=slug)
    state = _session_state(request)
    example_lesson = None
    example_title = None
    example_code = None
    if lesson.activity_type == "code" and lesson.path.category == "programming":
        code_lessons = Lesson.objects.filter(
            path=lesson.path,
            activity_type="code",
        ).exclude(pk=lesson.pk)
        example_lesson = (
            code_lessons.filter(order__lt=lesson.order)
            .order_by("-order", "-title")
            .first()
        )
        if example_lesson is None:
            example_lesson = code_lessons.order_by("order", "title").first()
        if example_lesson:
            example_title = example_lesson.title
            example_code = example_lesson.solution
        else:
            example_title, example_code = PROGRAMMING_EXAMPLES.get(
                lesson.path.slug,
                (f"{lesson.path.title}: a small code example", lesson.starter_code),
            )
    quiz_questions = list(lesson.quiz_questions.all())
    current_step = state["lesson_steps"].get(lesson.slug, 1)
    if lesson.slug in state["completed"]:
        current_step = 6
    quiz_position = state["quiz_positions"].get(lesson.slug, 0)
    activity_feedback = None
    activity_passed = None
    activity_submitted = False
    expected_output = None
    activity_missing = []
    submitted_code = None
    quiz_summary = None
    quiz_submitted = False
    if current_step == 4:
        activity_passed = lesson.slug in state["activities"]

    if request.method == "POST":
        if "advance_step" in request.POST:
            requested_step = request.POST.get("advance_step")
            if (
                current_step in (1, 2)
                and requested_step == str(current_step)
            ):
                current_step += 1
                state["lesson_steps"][lesson.slug] = current_step
            elif current_step == 4 and requested_step == "4":
                current_step = 5 if quiz_questions else 6
                state["lesson_steps"][lesson.slug] = current_step
        elif "retry_activity" in request.POST and current_step in (4, 6):
            current_step = 3
            state["lesson_steps"][lesson.slug] = current_step
        elif current_step == 3 and "submission" in request.POST:
            activity_submitted = True
            if lesson.slug not in state["attempts"]:
                state["attempts"].append(lesson.slug)
            submitted_code = request.POST.get("submission", "")
            if lesson.activity_type == "code":
                activity_passed, expected_output, activity_missing = (
                    _check_code_submission(lesson, submitted_code)
                )
                if activity_passed:
                    activity_feedback = (
                        "Correct. Your code follows the instructions for this challenge."
                    )
                else:
                    activity_feedback = (
                        "Not quite yet. Compare your attempt with the instructions and hint, then try again."
                    )
            if activity_passed and lesson.slug not in state["activities"]:
                state["activities"].append(lesson.slug)

            current_step = 4
            state["lesson_steps"][lesson.slug] = current_step

        elif current_step == 3 and "diagnosis" in request.POST:
            activity_submitted = True
            if lesson.slug not in state["attempts"]:
                state["attempts"].append(lesson.slug)
            selected = request.POST.get("diagnosis", "")
            activity_passed = (
                selected in lesson.activity_choices
                and selected.strip().lower() == lesson.answer.strip().lower()
            )
            activity_feedback = (
                (
                    "Great work. You identified the right troubleshooting step."
                    if lesson.activity_type == "support"
                    else "Correct. You identified the key concept."
                )
                if activity_passed
                else (
                    "That is not the best next step. Review the investigation explanation and try again."
                    if lesson.activity_type == "support"
                    else "Not quite. Review the lesson and try another answer."
                )
            )
            if activity_passed and lesson.slug not in state["activities"]:
                state["activities"].append(lesson.slug)

            current_step = 4
            state["lesson_steps"][lesson.slug] = current_step

        if (
            current_step == 5
            and quiz_position < len(quiz_questions)
            and f"quiz_{quiz_questions[quiz_position].id}" in request.POST
        ):
            quiz_submitted = True
            question = quiz_questions[quiz_position]
            quiz_progress = state["quiz_correct"].setdefault(lesson.slug, {})
            question_key = str(question.id)
            selected_answer = request.POST.get(f"quiz_{question.id}")
            if selected_answer == question.options[question.correct_index]:
                quiz_progress[question_key] = selected_answer
            _record_study_day(state)
        elif current_step == 5 and "next_question" in request.POST:
            if quiz_position < len(quiz_questions):
                current_question = quiz_questions[quiz_position]
                saved_answer = state["quiz_correct"].get(lesson.slug, {}).get(
                    str(current_question.id)
                )
                if saved_answer:
                    if quiz_position + 1 < len(quiz_questions):
                        quiz_position += 1
                        state["quiz_positions"][lesson.slug] = quiz_position
                    else:
                        current_step = 6
                        state["lesson_steps"][lesson.slug] = current_step

        _record_study_day(state)
        request.session["learning_state"] = state
        request.session.modified = True

    quiz_progress = state["quiz_correct"].get(lesson.slug, {})
    quiz_items = []
    correct_count = 0
    active_question = (
        quiz_questions[quiz_position]
        if quiz_position < len(quiz_questions)
        else None
    )
    for question in quiz_questions:
        question_key = str(question.id)
        saved_answer = quiz_progress.get(question_key)
        was_already_correct = saved_answer is not None
        selected_answer = saved_answer if was_already_correct else None
        status = "correct" if was_already_correct else ""

        if quiz_submitted and question == active_question and not was_already_correct:
            selected_answer = request.POST.get(f"quiz_{question.id}")
            correct_option = question.options[question.correct_index]
            if selected_answer == correct_option:
                quiz_progress[question_key] = correct_option
                selected_answer = correct_option
                status = "correct"
            else:
                status = "wrong" if selected_answer else "missing"

        is_correct = status == "correct"
        if is_correct:
            correct_count += 1
        quiz_items.append(
            {
                "question": question,
                "selected_answer": selected_answer if is_correct else None,
                "status": status,
                "locked": is_correct,
                "explanation": question.explanation if is_correct else "",
            }
        )

    total_questions = len(quiz_questions)
    if total_questions:
        quiz_percentage = round((correct_count / total_questions) * 100)
        summary = {
            "score": correct_count,
            "total": total_questions,
            "percentage": quiz_percentage,
        }
        if quiz_submitted or correct_count:
            quiz_summary = summary
            state["quiz_scores"][lesson.slug] = quiz_summary
            state["quiz_scores"]["latest"] = quiz_summary
            request.session["learning_state"] = state
            request.session.modified = True

    completed = (
        current_step == 6
        and lesson.slug in state["activities"]
        and correct_count == total_questions
    )
    if completed and lesson.slug not in state["completed"]:
        state["completed"].append(lesson.slug)
        request.session["learning_state"] = state
        request.session.modified = True

    if current_step == 6 and completed:
        completion_status = "completed"
    elif current_step == 6:
        completion_status = "practice"
    else:
        completion_status = "in_progress"

    context = {
        "lesson": lesson,
        "example_lesson": example_lesson,
        "example_title": example_title,
        "example_code": example_code,
        "current_step": current_step,
        "activity_feedback": activity_feedback,
        "activity_passed": activity_passed,
        "activity_submitted": activity_submitted,
        "can_review_solution": current_step >= 4 or lesson.slug in state["attempts"],
        "activity_missing": activity_missing,
        "expected_output": expected_output,
        "submitted_code": submitted_code,
        "quiz_summary": quiz_summary,
        "quiz_questions": quiz_items,
        "active_quiz_item": (
            quiz_items[quiz_position] if quiz_position < len(quiz_items) else None
        ),
        "question_number": quiz_position + 1,
        "question_total": total_questions,
        "has_next_question": quiz_position + 1 < total_questions,
        "completion_status": completion_status,
        "quiz_submitted": quiz_submitted,
        "completed": completed,
    }
    return render(request, "lesson_detail.html", context)
