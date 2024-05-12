// Colleges data for matching colleges based on percentage and specialization
const collegesData = {
  "طب بشري": 82,
  "طب الأسنان": 79,
  "علاج طبيعي": 78,
  صيدلة: 78,
  "طب بيطري": 73,
  هندسة: 65,
  "علوم الحاسب": 62,
  "كلية تكنولوجيا العلوم الصحية وكليات التكنولوجيا الحيوية": 59,
  "فنون تطبيقية (الشعبة العلمية)": 59,
  "كلية العلوم الأساسية": 58,
  "الإعلام وفنون الاتصال (الشعبة الأدبية)": 55,
  "اللغات والترجمة": 55,
  "اقتصاد وعلوم سياسية": 55,
  "كليات الاقتصاد والإدارة": 55,
  زراعة: 55,
  آداب: 55,
  آثار: 55,
  تربية: 55,
  "سياحة وفنادق": 55,
  حقوق: 55,
  تمريض: 55,
  "علوم سنيمائية": 55,
};

// Colleges with their coordinates for finding the nearest college
const collegesCoordinates = {
  "International Academy - El Alamein": {
    latitude: 30.812425108622012,
    longitude: 28.929221544299974,
  },
  "King Salman International University": {
    latitude: 28.237790686879233,
    longitude: 33.64926962890776,
  },
  "Al-Jalalah University": {
    latitude: 29.433486474044066,
    longitude: 32.40276508531423,
  },
  "New Mansoura University": {
    latitude: 31.46734755656675,
    longitude: 31.456074360307362,
  },
  "Ismailia National University": {
    latitude: 30.585505392260647,
    longitude: 32.354599745662725,
  },
  "East Portsaid National University": {
    latitude: 31.020730208920604,
    longitude: 32.62685115057633,
  },
  "Benha  National University": {
    latitude: 30.245117102759714,
    longitude: 31.457472906929397,
  },
  "Helwan National University": {
    latitude: 29.872980652067906,
    longitude: 31.317419452589697,
  },
  "Beni-Suef National University": {
    latitude: 29.03486876722051,
    longitude: 31.121882120109884,
  },
  "Minia National University": {
    latitude: 28.07641914254702,
    longitude: 30.83577692087913,
  },
  "Assiut National University( ANU )": {
    latitude: 27.27449804017888,
    longitude: 31.275639691133634,
  },
  "Sohag University National": {
    latitude: 26.45244464143984,
    longitude: 31.66147480166755,
  },
};

// Function to calculate distance between two points (in kilometers)
function calculateDistance(lat1, lon1, lat2, lon2) {
  const R = 6371; // Radius of the earth in km
  const dLat = deg2rad(lat2 - lat1);
  const dLon = deg2rad(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.cos(deg2rad(lat1)) *
      Math.cos(deg2rad(lat2)) *
      Math.sin(dLon / 2) *
      Math.sin(dLon / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  const d = R * c; // Distance in km
  return d;
}

function deg2rad(deg) {
  return deg * (Math.PI / 180);
}

function findMatchingColleges() {
  const percentage = parseFloat(document.getElementById("percentage").value);
  const specialization = document.getElementById("specialization").value;
  const resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "";

  const matchingColleges = [];
  for (const [college, acceptancePercentage] of Object.entries(collegesData)) {
    if (percentage >= acceptancePercentage) {
      // Check if the college belongs to the selected specialization
      if (
        (specialization === "science" && isScienceCollege(college)) ||
        (specialization === "mathematics" && isMathematicsCollege(college)) ||
        (specialization === "literature" && isLiteratureCollege(college))
      ) {
        matchingColleges.push(college);
      }
    }
  }

  if (matchingColleges.length > 0) {
    const list = document.createElement("ul");
    matchingColleges.forEach((college) => {
      const listItem = document.createElement("li");
      listItem.textContent = college;
      list.appendChild(listItem);
    });
    resultsDiv.appendChild(list);
  } else {
    resultsDiv.textContent =
      "No suitable colleges found for your percentage and specialization.";
  }
}

function findNearestCollege() {
  const userGovernorate = document.getElementById("governorate").value.trim();

  // Coordinates of the user's governorate
  let userLocation = null;
  switch (userGovernorate.toLowerCase()) {
    // Add more cases for other governorates if needed
    case "cairo":
      userLocation = { latitude: 30.0444, longitude: 31.2357 };
      break;
    case "alexandria":
      userLocation = { latitude: 31.2001, longitude: 29.9187 };
      break;
    case "ismailia":
      userLocation = { latitude: 30.6043, longitude: 32.2723 };
      break;
    case "aswan":
      userLocation = { latitude: 24.0889, longitude: 32.8998 };
      break;
    case "asyut":
      userLocation = { latitude: 27.1826, longitude: 31.1718 };
      break;
    case "luxor":
      userLocation = { latitude: 25.6872, longitude: 32.6396 };
      break;
    case "port said":
      userLocation = { latitude: 31.2565, longitude: 32.284 };
      break;
    case "red sea":
      userLocation = { latitude: 26.58, longitude: 33.51 };
      break;
    case "south sinai":
      userLocation = { latitude: 28.2423, longitude: 34.1771 };
      break;
    case "giza":
      userLocation = { latitude: 30.0131, longitude: 31.2089 };
      break;
    case "damietta":
      userLocation = { latitude: 31.4165, longitude: 31.8133 };
      break;
    case "dakahlia":
      userLocation = { latitude: 31.0359, longitude: 31.3807 };
      break;
    case "sohag":
      userLocation = { latitude: 26.5569, longitude: 31.6959 };
      break;
    case "suez":
      userLocation = { latitude: 29.9737, longitude: 32.5263 };
      break;
    case "mansoura":
      userLocation = { latitude: 31.0419, longitude: 31.3785 };
      break;
    case "ismailia":
      userLocation = { latitude: 30.6043, longitude: 32.2723 };
      break;
    case "qena":
      userLocation = { latitude: 26.1644, longitude: 32.7267 };
      break;
    case "kafr el-sheikh":
      userLocation = { latitude: 31.1081, longitude: 30.941 };
      break;
    case "matrouh":
      userLocation = { latitude: 29.4714, longitude: 25.6732 };
      break;
    case "monufia":
      userLocation = { latitude: 30.4694, longitude: 31.1844 };
      break;
    case "menoufia":
      userLocation = { latitude: 30.4148, longitude: 30.8071 };
      break;
    case "beni suef":
      userLocation = { latitude: 29.0744, longitude: 31.097 };
      break;
    case "beheira":
      userLocation = { latitude: 30.574, longitude: 30.894 };
      break;
    case "faiyum":
      userLocation = { latitude: 29.3084, longitude: 30.8428 };
      break;
    case "gharbia":
      userLocation = { latitude: 30.6173, longitude: 30.7237 };
      break;
    case "minya":
      userLocation = { latitude: 28.1199, longitude: 30.7503 };
      break;
    case "new valley":
      userLocation = { latitude: 25.6785, longitude: 28.2616 };
      break;
    case "north sinai":
      userLocation = { latitude: 30.5737, longitude: 33.0086 };
      break;
    case "sohag":
      userLocation = { latitude: 26.5569, longitude: 31.6959 };
      break;
    case "qalyubia":
      userLocation = { latitude: 30.409, longitude: 31.136 };
      break;
    // Add more cases for other governorates if needed
    default:
      alert("Governorate not found!");
      return;
  }

  let nearestCollege = null;
  let shortestDistance = Infinity;

  // Calculate distance to each college
  for (const college in collegesCoordinates) {
    const collegeLocation = collegesCoordinates[college];
    const distance = calculateDistance(
      userLocation.latitude,
      userLocation.longitude,
      collegeLocation.latitude,
      collegeLocation.longitude
    );
    if (distance < shortestDistance) {
      shortestDistance = distance;
      nearestCollege = college;
    }
  }

  // Display the result
  const resultElement = document.getElementById("result");
  if (nearestCollege) {
    resultElement.textContent = `The nearest college to ${userGovernorate} is: ${nearestCollege}`;
  } else {
    resultElement.textContent = "No college found!";
  }
}

function isScienceCollege(college) {
  const scienceColleges = [
    "تمريض",
    "حقوق",
    "زراعة",
    "اللغات والترجمة",
    "كلية العلوم الأساسية",
    "فنون تطبيقية (الشعبة العلمية)",
    "كلية تكنولوجيا العلوم الصحية وكليات التكنولوجيا الحيوية",
    "طب بيطري",
    "علاج طبيعي",
    "صيدلة",
    "طب بشري",
    "طب الأسنان",
    "علم الحاسب",
  ];
  return scienceColleges.includes(college);
}

function isMathematicsCollege(college) {
  const mathematicsColleges = [
    "آداب",
    "حقوق",
    "زراعة",
    "اللغات والترجمة",
    "كلية العلوم الأساسية",
    "فنون تطبيقية (الشعبة العلمية)",
    "هندسة",
    "كلية العلوم الأساسية",
  ];
  return mathematicsColleges.includes(college);
}

function isLiteratureCollege(college) {
  const literatureColleges = [
    "حقوق",
    "سياحة وفنادق",
    "تربية",
    "آثار",
    "آداب",
    "زراعة",
    "كليات الاقتصاد والإدارة",
    "اقتصاد وعلوم سياسية",
    "اللغات والترجمة",
    "آداب",
    "الإعلام وفنون الاتصال (الشعبة الأدبية)",
  ];
  return literatureColleges.includes(college);
}
