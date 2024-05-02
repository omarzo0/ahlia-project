function evaluateQuiz() {
  const answers = {
    majors: {
      humanities: 0,
      scienceHealth: 0,
      stem: 0,
      socialSciences: 0,
      business: 0,
    },
    personalTraits: {
      humanities: "Analytical",
      scienceHealth: "Creative",
      stem: "Inquisitive",
      socialSciences: "Compassionate",
      business: "Persuasive",
    },
    careerAspirations: {
      humanities: "Researcher/Writer",
      scienceHealth: "Scientist/Health Professional",
      stem: "Engineer/Mathematician",
      socialSciences: "Historian/Social Scientist",
      business: "Entrepreneur/Business Leader",
    },
    leisurePreferences: {
      humanities: "Creative Expression",
      scienceHealth: "Entertainment/Gaming",
      stem: "Entrepreneurial Activities",
      socialSciences: "Social Engagement",
      business: "Intellectual Pursuits",
    },
    learningStyles: {
      humanities: "Reflective/Conceptual",
      scienceHealth: "Active/Experimental",
      stem: "Practical/Application-based",
      socialSciences: "Social/Interpersonal",
      business: "Logical/Strategic",
    },
  };

  // Retrieve user's answers
  const form = document.getElementById("quizForm");
  for (let i = 1; i <= 10; i++) {
    const questionName = "question" + i;
    const selectedAnswer = form.elements[questionName].value;
    // Increment the score for the chosen major
    switch (selectedAnswer) {
      case "a":
        answers.majors.humanities++;
        break;
      case "b":
        answers.majors.scienceHealth++;
        break;
      case "c":
        answers.majors.stem++;
        break;
      case "d":
        answers.majors.socialSciences++;
        break;
      case "e":
        answers.majors.business++;
        break;
      default:
        break;
    }
  }

  // Determine the major(s) with the highest score
  let maxScore = Math.max(...Object.values(answers.majors));
  let resultMajors = [];
  for (const major in answers.majors) {
    if (answers.majors[major] === maxScore) {
      resultMajors.push(major);
    }
  }

  // Get descriptions based on the chosen major(s)
  let resultPersonalTraits = resultMajors.map(
    (major) => answers.personalTraits[major]
  );
  let resultCareerAspirations = resultMajors.map(
    (major) => answers.careerAspirations[major]
  );
  let resultLeisurePreferences = resultMajors.map(
    (major) => answers.leisurePreferences[major]
  );
  let resultLearningStyles = resultMajors.map(
    (major) => answers.learningStyles[major]
  );

  // Display the results
  const resultDiv = document.getElementById("results");
  resultDiv.innerHTML =
    " Personal Traits: " +
    resultPersonalTraits.join(", ") +
    "<br>" +
    " Career Aspirations: " +
    resultCareerAspirations.join(", ") +
    "<br>" +
    " Leisure Preferences: " +
    resultLeisurePreferences.join(", ") +
    "<br>" +
    " Learning Styles: " +
    resultLearningStyles.join(", ") +
    "<br>" +
    " Majors of Interest: " +
    resultMajors.join(", ");
}
