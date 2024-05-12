const collegesData = {
  "طب بشري": 82,
  "طب الأسنان": 79,
  "علاج طبيعي": 78,
  "صيدلة": 78,
  "طب بيطري": 73,
  "هندسة": 65,
  "علوم الحاسب": 62,
  "كلية تكنولوجيا العلوم الصحية وكليات التكنولوجيا الحيوية": 59,
  "فنون تطبيقية (الشعبة العلمية)": 59,
  "كلية العلوم الأساسية": 58,
  "الإعلام وفنون الاتصال (الشعبة الأدبية)": 55,
  "اللغات والترجمة": 55,
  "اقتصاد وعلوم سياسية": 55,
  "كليات الاقتصاد والإدارة": 55,
  "زراعة": 55,
  "آداب": 55,
  "آثار": 55,
  "تربية": 55,
  "سياحة وفنادق": 55,
  "حقوق": 55,
  "تمريض": 55,
  "علوم سنيمائية": 55
};

function findMatchingColleges() {
  const percentage = parseFloat(document.getElementById("percentage").value);
  const specialization = document.getElementById("specialization").value;
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  const matchingColleges = [];
  for (const [college, acceptancePercentage] of Object.entries(collegesData)) {
    if (percentage >= acceptancePercentage) {
      // Check if the college belongs to the selected specialization
      if ((specialization === 'science' && isScienceCollege(college)) ||
          (specialization === 'mathematics' && isMathematicsCollege(college)) ||
          (specialization === 'literature' && isLiteratureCollege(college))) {
        matchingColleges.push(college);
      }
    }
  }

  if (matchingColleges.length > 0) {
    const list = document.createElement("ul");
    matchingColleges.forEach(college => {
      const listItem = document.createElement("li");
      listItem.textContent = college;
      list.appendChild(listItem);
    });
    resultsDiv.appendChild(list);
  } else {
    resultsDiv.textContent = "No suitable colleges found for your percentage and specialization.";
  }
}

function isScienceCollege(college) {
  
  const scienceColleges = ["تمريض","حقوق","زراعة","اللغات والترجمة","كلية العلوم الأساسية","فنون تطبيقية (الشعبة العلمية)","كلية تكنولوجيا العلوم الصحية وكليات التكنولوجيا الحيوية","طب بيطري","علاج طبيعي","صيدلة","طب بشري", "طب الأسنان", "علم الحاسب"];
  return scienceColleges.includes(college);
}

function isMathematicsCollege(college) {
 
  const mathematicsColleges = ["آداب","حقوق","زراعة","اللغات والترجمة","كلية العلوم الأساسية","فنون تطبيقية (الشعبة العلمية)","هندسة", "كلية العلوم الأساسية"];
  return mathematicsColleges.includes(college);
}

function isLiteratureCollege(college) {
 
  const literatureColleges = ["حقوق","سياحة وفنادق","تربية","آثار","آداب","زراعة","كليات الاقتصاد والإدارة","اقتصاد وعلوم سياسية","اللغات والترجمة","آداب", "الإعلام وفنون الاتصال (الشعبة الأدبية)"];
  return literatureColleges.includes(college);
}
