from django.test import TestCase
from django.urls import reverse

from .models import LearningPath, Lesson


class LearningLabTests(TestCase):
    def _open_activity_step(self, lesson):
        response = self.client.get(reverse("lesson_detail", args=[lesson.slug]))
        response = self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {"advance_step": "1"},
        )
        response = self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {"advance_step": "2"},
        )
        return response

    def _open_python_quiz_step(self, lesson):
        response = self._open_activity_step(lesson)
        response = self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {"submission": 'name = "Alex"\nprint(name)'},
        )
        return self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {"advance_step": "4"},
        )

    def test_dashboard_shows_three_learning_tracks(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Programming and Coding")
        self.assertContains(response, "IT Support and Troubleshooting")
        self.assertContains(response, "Hardware and Networking")
        self.assertEqual(len(response.context["learning_tracks"]), 3)

    def test_every_learning_path_has_lesson_content_and_three_quiz_questions(self):
        paths = LearningPath.objects.prefetch_related("lessons__quiz_questions")

        for path in paths:
            with self.subTest(path=path.slug):
                lessons = list(path.lessons.all())
                self.assertTrue(lessons)
                for lesson in lessons:
                    self.assertEqual(lesson.quiz_questions.count(), 3)

    def test_every_path_has_twenty_beginner_and_ten_intermediate_topics(self):
        paths = LearningPath.objects.prefetch_related("lessons__quiz_questions")
        self.assertEqual(paths.count(), 18)
        for path in paths:
            with self.subTest(path=path.slug):
                self.assertEqual(path.lessons.filter(difficulty="Beginner").count(), 20)
                self.assertEqual(path.lessons.filter(difficulty="Intermediate").count(), 10)
                for lesson in path.lessons.all():
                    self.assertEqual(lesson.quiz_questions.count(), 3)

    def test_computer_hardware_has_twenty_beginner_and_ten_intermediate_lessons(self):
        path = LearningPath.objects.get(slug="computer-hardware")
        lessons = path.lessons.all()

        self.assertEqual(lessons.count(), 30)
        self.assertEqual(lessons.filter(difficulty="Beginner").count(), 20)
        self.assertEqual(lessons.filter(difficulty="Intermediate").count(), 10)
        self.assertTrue(all(lesson.quiz_questions.count() == 3 for lesson in lessons))

    def test_fresh_quiz_visit_does_not_show_a_score_or_retry_summary(self):
        lesson = Lesson.objects.get(slug="python-variables")

        response = self.client.get(reverse("lesson_detail", args=[lesson.slug]))

        self.assertIsNone(response.context["quiz_summary"])
        self.assertNotContains(response, "Correct answers:")
        self.assertNotContains(response, "retry any missed questions")
        self.assertNotContains(response, "Step 5: Knowledge Check")

    def test_lesson_reveals_one_step_at_a_time_and_explains_after_activity_attempt(self):
        lesson = Lesson.objects.get(slug="python-variables")
        lesson_url = reverse("lesson_detail", args=[lesson.slug])

        response = self.client.get(lesson_url)
        self.assertContains(response, "Step 1: Topic Introduction")
        self.assertNotContains(response, "Learn the Concept")
        self.assertNotContains(response, "One correct solution:")

        response = self.client.post(lesson_url, {"advance_step": "1"})
        self.assertContains(response, "Step 2: Learn the Concept")
        self.assertNotContains(response, "Your Question or Practice")

        response = self.client.post(lesson_url, {"advance_step": "2"})
        self.assertContains(response, "Step 3: Your Question or Practice")
        self.assertNotContains(response, "Step 4: Answer and Explanation")
        self.assertNotContains(response, 'name = "Alex"')

        response = self.client.post(
            lesson_url,
            {"submission": 'name = "Alex"\nprint(name)'},
        )
        self.assertContains(response, "Step 4: Answer and Explanation")
        self.assertContains(response, "One correct solution:")
        self.assertNotContains(response, "Step 5: Knowledge Check")

        response = self.client.post(lesson_url, {"advance_step": "4"})
        self.assertContains(response, "Question 1 of 3")
        self.assertEqual(len(response.context["quiz_questions"]), 3)
        self.assertContains(response, "Check answer")
        self.assertNotContains(response, "Question 2 of 3")

    def test_quiz_keeps_correct_answers_and_allows_wrong_answers_to_retry(self):
        lesson = Lesson.objects.get(slug="python-variables")
        questions = list(lesson.quiz_questions.all())
        first_question, second_question, third_question = questions
        self._open_python_quiz_step(lesson)
        correct_first = first_question.options[first_question.correct_index]
        incorrect_second = second_question.options[
            (second_question.correct_index + 1) % len(second_question.options)
        ]

        first_response = self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {
                f"quiz_{first_question.id}": correct_first,
            },
        )
        self.assertEqual(first_response.context["quiz_summary"]["score"], 1)
        first_results = first_response.context["quiz_questions"]
        self.assertTrue(first_results[0]["locked"])
        self.assertNotContains(first_response, "Question 2 of 3")
        self.assertContains(first_response, "Correct — saved.")

        self.client.post(reverse("lesson_detail", args=[lesson.slug]), {"next_question": "1"})

        wrong_response = self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {
                f"quiz_{second_question.id}": incorrect_second,
            },
        )
        self.assertEqual(wrong_response.context["quiz_questions"][1]["status"], "wrong")
        self.assertNotContains(
            wrong_response,
            f"Correct — saved.</strong> {second_question.explanation}",
        )

        second_response = self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {f"quiz_{second_question.id}": second_question.options[second_question.correct_index]},
        )
        self.assertEqual(second_response.context["quiz_summary"]["score"], 2)
        self.client.post(reverse("lesson_detail", args=[lesson.slug]), {"next_question": "1"})
        third_response = self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {f"quiz_{third_question.id}": third_question.options[third_question.correct_index]},
        )
        self.assertEqual(third_response.context["quiz_summary"]["score"], 3)
        self.assertTrue(all(item["locked"] for item in third_response.context["quiz_questions"]))
        self.assertEqual(
            self.client.session["learning_state"]["quiz_correct"][lesson.slug][str(first_question.id)],
            correct_first,
        )
        self.assertContains(third_response, "Correct — saved.")
        completion_response = self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {"next_question": "1"},
        )
        self.assertContains(completion_response, "Lesson completed")
        self.assertEqual(completion_response.context["current_step"], 6)

    def test_reset_all_lessons_clears_session_progress_and_quiz_answers(self):
        session = self.client.session
        session["learning_state"] = {
            "completed": ["python-variables"],
            "activities": ["python-variables"],
            "attempts": ["python-variables"],
            "quiz_scores": {"latest": {"percentage": 100}},
            "quiz_correct": {"python-variables": {"1": "right"}},
            "study_days": ["2026-11-11"],
        }
        session.save()

        response = self.client.post(reverse("reset_progress"), follow=True)

        self.assertEqual(response.redirect_chain, [(reverse("dashboard"), 302)])
        self.assertNotIn("learning_state", self.client.session)
        self.assertContains(response, "All lesson progress has been reset")

    def test_code_submission_feedback_uses_red_for_missing_and_green_for_pass(self):
        lesson_url = reverse("lesson_detail", args=["css-style-heading"])
        lesson = Lesson.objects.get(slug="css-style-heading")
        self._open_activity_step(lesson)

        failed_response = self.client.post(
            lesson_url,
            {"submission": "h1 { color: red; }"},
        )
        self.assertContains(failed_response, "code-check-error")
        self.assertContains(failed_response, "code-feedback-error")
        self.assertContains(failed_response, "<code>blue</code>", html=True)

        self.client.post(lesson_url, {"retry_activity": "1"})
        passed_response = self.client.post(
            lesson_url,
            {"submission": "h1 { color: blue; }"},
        )
        self.assertContains(passed_response, "code-check-success")
        self.assertContains(passed_response, "code-feedback-success")

    def test_new_coding_lesson_checks_submission_without_running_it(self):
        lesson_url = reverse("lesson_detail", args=["javascript-message-variable"])
        lesson = Lesson.objects.get(slug="javascript-message-variable")
        response = self._open_activity_step(lesson)

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "One correct solution:")

        response = self.client.post(
            lesson_url,
            {"submission": 'const message = "Hello, learner!";\nconsole.log(message);'},
        )

        self.assertContains(response, "Correct. Your code follows the instructions")
        self.assertContains(response, "One correct solution:")
        self.assertContains(response, "Code is not executed on the server")

    def test_new_support_lesson_reveals_solution_after_attempt(self):
        lesson_url = reverse("lesson_detail", args=["printer-check-queue"])
        lesson = Lesson.objects.get(slug="printer-check-queue")
        response = self._open_activity_step(lesson)

        self.assertNotContains(response, "Open the printer queue")

        response = self.client.post(
            lesson_url,
            {"diagnosis": "Review the print queue and printer status before changing jobs"},
        )

        self.assertContains(response, "Correct answer:")
        self.assertContains(response, "Open the printer queue")

    def test_variable_solution_is_hidden_until_activity_attempt(self):
        lesson = Lesson.objects.get(slug="python-variables")
        response = self._open_activity_step(lesson)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Expected output")
        self.assertNotContains(response, 'name = "Alex"')
        self.assertNotContains(response, "One correct solution:")
        self.assertNotContains(response, "data-solution=")
        self.assertNotContains(response, "Show Solution")

    def test_variable_challenge_and_quiz_complete_lesson(self):
        lesson = Lesson.objects.get(slug="python-variables")
        lesson_url = reverse("lesson_detail", args=[lesson.slug])
        self._open_activity_step(lesson)

        activity_response = self.client.post(
            lesson_url,
            {"submission": 'name = "Alex"\nprint(name)'},
        )

        self.assertContains(activity_response, "Correct. Your code follows the instructions")
        self.assertContains(activity_response, "<pre class=\"console-output mb-0\">Alex</pre>", html=True)
        self.assertContains(activity_response, "One correct solution:")
        self.assertEqual(
            activity_response.context["submitted_code"],
            'name = "Alex"\nprint(name)',
        )

        self.client.post(lesson_url, {"advance_step": "4"})
        for question in lesson.quiz_questions.all():
            quiz_response = self.client.post(
                lesson_url,
                {f"quiz_{question.id}": question.options[question.correct_index]},
            )
            self.client.post(lesson_url, {"next_question": "1"})
        self.assertContains(quiz_response, "Correct answers so far:</strong> 3/3")
        self.assertContains(self.client.get(lesson_url), "Lesson completed")
        self.assertEqual(
            self.client.session["learning_state"]["completed"],
            ["python-variables"],
        )

    def test_wrong_variable_activity_does_not_pass(self):
        lesson = Lesson.objects.get(slug="python-variables")
        self._open_activity_step(lesson)
        response = self.client.post(
            reverse("lesson_detail", args=[lesson.slug]),
            {"submission": 'name = "Alex"\nprint("name")'},
        )

        self.assertContains(response, "Not quite yet")
        self.assertContains(response, "Common mistake")
        self.assertNotIn(
            "python-variables",
            self.client.session.get("learning_state", {}).get("activities", []),
        )

    def test_support_solution_is_revealed_after_investigation_attempt(self):
        lesson_url = reverse("lesson_detail", args=["computer-wont-turn-on"])
        lesson = Lesson.objects.get(slug="computer-wont-turn-on")
        response = self._open_activity_step(lesson)
        self.assertNotContains(response, "The first step is to verify the power source")

        response = self.client.post(
            lesson_url,
            {"diagnosis": "Reinstall the operating system"},
        )
        self.assertContains(response, "That is not the best next step")
        self.assertContains(response, "The first step is to verify the power source")

        self.client.post(lesson_url, {"retry_activity": "1"})
        response = self.client.post(
            lesson_url,
            {"diagnosis": "Check the power cable and outlet first"},
        )
        self.assertContains(response, "Great work. You identified the right troubleshooting step")
