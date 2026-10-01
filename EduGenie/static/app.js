const task = document.getElementById("task");
const inputText = document.getElementById("inputText");
const submitBtn = document.getElementById("submitBtn");
const result = document.getElementById("result");
const status = document.getElementById("status");
const counter = document.getElementById("counter");

const endpoints = {
  qa: "/qa",
  explain: "/explain",
  quiz: "/quiz",
  summarize: "/summarize",
  learn: "/learn/recommendations",
};

const placeholders = {
  qa: "Example: Which is the largest ocean?",
  explain: "Example: Explain the Pythagoras theorem with a simple example.",
  quiz: "Paste a topic or passage to create 3 MCQs.",
  summarize: "Paste your educational notes or a long passage here.",
  learn: "Example: SQL, Python, machine learning, web development...",
};

task.addEventListener("change", () => {
  inputText.placeholder = placeholders[task.value];
  result.classList.add("hidden");
  status.textContent = "";
});

inputText.addEventListener("input", () => {
  counter.textContent = `${inputText.value.length} / 12000`;
});

submitBtn.addEventListener("click", async () => {
  const text = inputText.value.trim();
  if (!text) {
    status.textContent = "Please enter a question, topic, or passage.";
    return;
  }

  submitBtn.disabled = true;
  status.textContent = "Thinking...";
  result.classList.add("hidden");

  try {
    const response = await fetch(endpoints[task.value], {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "Request failed.");

    if (task.value === "quiz") {
      renderQuiz(data.questions);
    } else {
      renderText(data.result);
    }
    status.textContent = "Done.";
  } catch (error) {
    status.textContent = error.message || "Something went wrong.";
  } finally {
    submitBtn.disabled = false;
  }
});

function renderText(text) {
  result.innerHTML = `<h2>Result</h2><div>${escapeHtml(text).replace(/\n/g, "<br>")}</div>`;
  result.classList.remove("hidden");
}

function renderQuiz(questions) {
  result.innerHTML = `<h2>Quiz</h2>`;
  questions.forEach((item, index) => {
    const wrapper = document.createElement("div");
    wrapper.className = "quiz-item";
    wrapper.innerHTML = `<strong>${index + 1}. ${escapeHtml(item.question)}</strong><div class="quiz-options"></div><div class="feedback"></div>`;
    const options = wrapper.querySelector(".quiz-options");
    const feedback = wrapper.querySelector(".feedback");

    item.options.forEach(option => {
      const button = document.createElement("button");
      button.className = "quiz-option";
      button.textContent = option;
      button.addEventListener("click", () => {
        [...options.children].forEach(b => b.disabled = true);
        if (option === item.correct_answer) {
          button.classList.add("correct");
          feedback.textContent = `Correct! ${item.explanation}`;
        } else {
          button.classList.add("wrong");
          [...options.children].find(b => b.textContent === item.correct_answer)?.classList.add("correct");
          feedback.textContent = `Not quite. Correct answer: ${item.correct_answer}. ${item.explanation}`;
        }
      });
      options.appendChild(button);
    });
    result.appendChild(wrapper);
  });
  result.classList.remove("hidden");
}

function escapeHtml(value) {
  return value.replace(/[&<>'"]/g, ch => ({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;","\"":"&quot;"}[ch]));
}
