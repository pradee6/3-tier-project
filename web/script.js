let phone = "";

// Handle signup
document.getElementById("signupForm")?.addEventListener("submit", function (e) {
    e.preventDefault();
    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    phone = document.getElementById("phone").value.trim();
    const gender = document.getElementById("gender").value;
    const dob = document.getElementById("dob").value;

    // Normalize phone number by adding +91 if not present
    if (!phone.startsWith('+')) {
        if (phone.startsWith('0')) {
            phone = phone.substring(1);
        }
        phone = '+91' + phone;
    }

    fetch('http://13.40.94.202:5000/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password, phone, gender, dob })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("signupMessage").innerText = data.message;
        if (data.message === 'User registered successfully.') {
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Handle login
document.getElementById("loginForm")?.addEventListener("submit", function (e) {
    e.preventDefault();
    const email = document.getElementById("loginEmail").value;
    const password = document.getElementById("loginPassword").value;

    fetch('http://13.40.94.202:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',  // Include cookies in the request
        body: JSON.stringify({ email, password })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Log the entire response for debugging
        console.log('Current Cookies:', document.cookie); // Log cookies here
        document.getElementById("loginMessage").innerText = data.message;
        document.getElementById("loginMessage").classList.add("fade-in");

        if (data.message === 'Login successful.') {
            // Store user ID in local storage
            localStorage.setItem('userId', data.userId); // Ensure this line runs correctly

            // Debugging log to verify local storage
            console.log('Stored user ID in local storage:', localStorage.getItem('userId'));

            // Redirect to dashboard after successful login
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 2000); // Redirect after 2 seconds
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("loginMessage").innerText = 'Login failed. Please check your credentials.';
    });
});


// Handle OTP for reset password
document.getElementById("sendOtp")?.addEventListener("click", function () {
    let phoneNumber = document.getElementById("phone").value.trim();

    // Normalize phone number: Add +91 if not present
    if (!phoneNumber.startsWith('+')) {
        if (phoneNumber.startsWith('0')) {
            phoneNumber = phoneNumber.substring(1);  // Remove leading zero
        }
        phoneNumber = '+91' + phoneNumber;
    }

    console.log("Sending phone number:", phoneNumber);  // Debugging

    fetch('http://13.40.94.202:5000/send-otp', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: phoneNumber })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);  // Debugging response
        document.getElementById("resetMessage").innerText = data.message;
        document.getElementById("resetMessage").classList.add("fade-in");
        if (data.message === 'OTP sent to your registered email.') {
            document.getElementById("otpForm").style.display = "none";
            document.getElementById("resetForm").style.display = "block";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById("resetMessage").innerText = 'Failed to send OTP. Please try again.';
    });
});

// Handle password reset
document.getElementById("resetForm")?.addEventListener("submit", function (e) {
    e.preventDefault();
    const otp = document.getElementById("otp").value;
    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    let enteredPhone = document.getElementById("phone").value.trim();

    // Normalize phone number by adding +91 if not present
    if (!enteredPhone.startsWith('+')) {
        if (enteredPhone.startsWith('0')) {
            enteredPhone = enteredPhone.substring(1);
        }
        enteredPhone = '+91' + enteredPhone;
    }

    fetch('http://13.40.94.202:5000/reset-password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: enteredPhone, otp, newPassword, confirmPassword })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("resetMessage").innerText = data.message;
        if (data.message === 'Password reset successful.') {
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 2000);
        }
    })
    .catch(error => console.error('Error:', error));
});

// Dashboard functionalities
document.addEventListener('DOMContentLoaded', () => {
    const categories = {
        travelling: [
            { name: "MakeMyTrip", url: "https://www.makemytrip.com" },
            { name: "RedBus", url: "https://www.redbus.in" },
            { name: "Cleartrip", url: "https://www.cleartrip.com" },
            { name: "Yatra", url: "https://www.yatra.com" },
            { name: "Goibibo", url: "https://www.goibibo.com" },
            { name: "IRCTC", url: "https://www.irctc.co.in" },
            { name: "TravelTriangle", url: "https://www.traveltriangle.com" }
        ],
        streaming: [
            { name: "Netflix", url: "https://www.netflix.com" },
            { name: "Amazon Prime Video", url: "https://www.primevideo.com" },
            { name: "Disney+ Hotstar", url: "https://www.hotstar.com" },
            { name: "Sony Liv", url: "https://www.sonyliv.com" },
            { name: "ZEE5", url: "https://www.zee5.com" },
            { name: "MX Player", url: "https://www.mxplayer.in" },
            { name: "YouTube", url: "https://www.youtube.com" },
            { name: "Apple TV+", url: "https://tv.apple.com" },
            { name: "Spotify", url: "https://www.spotify.com" }
        ],
        shopping: [
            { name: "Amazon India", url: "https://www.amazon.in" },
            { name: "Flipkart", url: "https://www.flipkart.com" },
            { name: "Myntra", url: "https://www.myntra.com" },
            { name: "Ajio", url: "https://www.ajio.com" },
            { name: "Tata Cliq", url: "https://www.tatacliq.com" }
        ],
        adult: [
            { name: "Pornhub", url: "https://www.pornhub.com" },
            { name: "Xhamster", url: "https://www.xhamster.com" },
            { name: "Redtube", url: "https://www.redtube.com" },
            { name: "YouPorn", url: "https://www.youporn.com" },
            { name: "HQporner", url: "https://www.hqporner.com" },
            { name: "Teamskeet", url: "https://www.teamskeet.com" },
            { name: "Eporner", url: "https://www.eporner.com" }
        ],
        insurance: [
            { name: "PolicyBazaar", url: "https://www.policybazaar.com" },
            { name: "Acko", url: "https://www.acko.com" },
            { name: "InsuranceDekho", url: "https://www.insurancedekho.com" },
            { name: "SecureNow", url: "https://www.securenow.in" },
            { name: "Star Health", url: "https://www.starhealth.in" },
            { name: "Bharti AXA", url: "https://www.bharti-axa.com" }
        ],
        pharmacy: [
            { name: "Apollo Pharmacy", url: "https://www.apollopharmacy.in" },
            { name: "1mg", url: "https://www.1mg.com" },
            { name: "Netmeds", url: "https://www.netmeds.com" },
            { name: "PharmEasy", url: "https://www.pharmeasy.in" }
        ],
        food: [
            { name: "Zomato", url: "https://www.zomato.com" },
            { name: "Swiggy", url: "https://www.swiggy.com" },
            { name: "Domino's Pizza", url: "https://www.dominos.co.in" },
            { name: "FoodPanda", url: "https://www.foodpanda.com" },
            { name: "Uber Eats", url: "https://www.ubereats.com" }
        ],
        social: [
            { name: "Facebook", url: "https://www.facebook.com" },
            { name: "Instagram", url: "https://www.instagram.com" },
            { name: "Twitter", url: "https://www.twitter.com" },
            { name: "LinkedIn", url: "https://www.linkedin.com" },
            { name: "Snapchat", url: "https://www.snapchat.com" },
            { name: "TikTok", url: "https://www.tiktok.com" }
        ]
    };

    const websitesList = document.getElementById('websites-list');
    const aboutSection = document.getElementById('about-section');
    const feedbackSection = document.getElementById('feedback-section');
    const profileSection = document.getElementById('profile-section');
    const registeredNameElement = document.getElementById('registered-name');
    const welcomeMessage = document.getElementById('welcome-message');

    // Home Button Functionality
    document.getElementById('home-btn').addEventListener('click', () => {
        websitesList.innerHTML = '';
        welcomeMessage.style.display = 'block';
        aboutSection.classList.add('hidden');
        feedbackSection.classList.add('hidden');
        profileSection.classList.add('hidden');
        document.getElementById('categories-container').classList.remove('hidden');
        websitesList.classList.add('hidden');
    });

    // About Button Functionality
    document.getElementById('about-btn').addEventListener('click', () => {
        websitesList.innerHTML = '';
        welcomeMessage.style.display = 'none';
        aboutSection.classList.toggle('hidden');
        feedbackSection.classList.add('hidden');
        profileSection.classList.add('hidden');
        document.getElementById('categories-container').classList.add('hidden');
        websitesList.classList.add('hidden');
    });

    // Feedback Button Functionality
    document.getElementById('feedback-btn').addEventListener('click', () => {
        websitesList.innerHTML = '';
        welcomeMessage.style.display = 'none';
        feedbackSection.classList.toggle('hidden');
        aboutSection.classList.add('hidden');
        profileSection.classList.add('hidden');
        document.getElementById('categories-container').classList.add('hidden');
        websitesList.classList.add('hidden');
    });

   // Profile Button Functionality
   document.getElementById('show-profile-btn').addEventListener('click', () => {
    const profileSection = document.getElementById('profile-section');
    const registeredNameElement = document.getElementById('registered-name');
    const registeredDobElement = document.getElementById('registered-dob');
    const registeredPhoneElement = document.getElementById('registered-phone');

    // Toggle visibility and hide others
    websitesList.innerHTML = '';
    welcomeMessage.style.display = 'none';
    profileSection.classList.toggle('hidden');
    aboutSection.classList.add('hidden');
    feedbackSection.classList.add('hidden');
    document.getElementById('categories-container').classList.add('hidden');
    websitesList.classList.add('hidden');

    // Get user ID from local storage
    const userId = localStorage.getItem('userId');

    // Fetch user profile data directly
    fetch(`http://13.40.94.202:5000/get-profile/${userId}`, { // Use userId in the URL
        method: 'GET',
        credentials: 'include', // Include session data if necessary
    })
    .then(response => {
        if (!response.ok) {
            console.error('Network response was not ok:', response.status, response.statusText);
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            registeredNameElement.textContent = data.data.name;
            registeredDobElement.textContent = data.data.dob;
            registeredPhoneElement.textContent = data.data.phone;
        } else {
            console.error('Error fetching profile:', data.message);
            alert(data.message); // Show user-friendly error message
        }
    })
    .catch(error => {
        console.error('Error fetching profile:', error);
        alert('Failed to fetch profile. Please try again.'); // Show user-friendly error message
    });
});

    // Category Click Functionality
    document.querySelectorAll('.category-grid').forEach(category => {
        category.addEventListener('click', () => {
            const categoryName = category.dataset.category;
            websitesList.innerHTML = '';

            // Toggle the visibility of the websites list
            if (websitesList.classList.contains('hidden')) {
                if (categories[categoryName]) {
                    categories[categoryName].forEach(website => {
                        const link = document.createElement('a');
                        link.href = website.url;
                        link.target = "_blank";
                        link.textContent = website.name;
                        websitesList.appendChild(link);
                    });
                }
                websitesList.classList.remove('hidden');
            } else {
                websitesList.classList.add('hidden');
            }
        });
    });

    // Dark Mode Toggle
    document.getElementById('dark-mode-toggle').addEventListener('click', () => {
        document.body.classList.toggle('dark-mode');
    });

    // Handle feedback submission
    document.getElementById('feedback-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const message = document.getElementById('message').value;

    const feedbackData = { name, email, message };

    fetch('http://13.40.94.202:5000/submit-feedback', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(feedbackData)
    })
    .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
    })
    .then(data => {
        alert('Thank you for your feedback! We truly value your input and can\'t wait to review it.');
        document.getElementById('feedback-form').reset();
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
        alert('There was an error submitting your feedback. Please try again later.');
    });
});

    // Logout button functionality
    document.getElementById('logout-btn').addEventListener('click', () => {
        window.location.href = 'login.html';
    });
});