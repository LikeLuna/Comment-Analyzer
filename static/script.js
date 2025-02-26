
//  ALl the variables stored to be used later
let aboutBtn=document.querySelector(".about-btn")
let closeBtn=document.querySelector(".close-icon")
let body=document.querySelector("body")
let slider = document.querySelector(".slider");
let content=document.querySelectorAll(".content")
let displayOpt=document.querySelector(".options h2")
let inputSearch=document.querySelector("input")
let searchBtn=document.querySelector(".search-icon")
let chartDiv = document.querySelector(".chart"); 
let resultBox=document.querySelector(".results");



// ---------------------about -----------------------------
//  Timeline for little animations on slider
let tl=gsap.timeline()

tl.from(".slider",{
    right:"-100%",
    duration:0.5,

})
tl.pause()

//  Animation for about button and text
aboutBtn.addEventListener("click",(event)=>{
    event.stopPropagation();
    tl.play()
})
closeBtn.addEventListener("click",()=>{
    tl.reverse()
})
body.addEventListener("click", (event) => {
    // Check if the clicked element is NOT inside the slider or the about button
    if (!slider.contains(event.target) && !aboutBtn.contains(event.target)) {
        tl.reverse();
    }
});





// holding value for each input placeholders
let placeholders = {
    "Youtube": "Place the YouTube link here...",
    "Movies & Show": "Under Process...",
    "Random": "Enter comments separated by ; ...",
};
// funtion to change input placeholder according to dropdown's option
let placehold = function () {
    inputSearch.placeholder = placeholders[displayOpt.textContent] || "Choose any option first...";
};





// Function to handle dropdown option change
function handleDropdownClick(event) {
    let h1 = this.querySelector("h1");
    if (h1) {
        let text = h1.textContent.trim();
        displayOpt.textContent = text;
        inputSearch.value = "";
        placehold();
        resultBox.style.display = "none";

        console.log(text);

        let scaleElements = document.getElementsByClassName("scale");
        Array.from(scaleElements).forEach(el => {
            el.style.display = (text.toLowerCase() === "youtube") ? "block" : "none";
        });
    }
}


content.forEach(li => li.addEventListener("click", handleDropdownClick));



function updateValue(value) {
    document.getElementById("sliderValue").textContent = value; // Update displayed value

    // Call fetchComments() to get updated comments
    fetchComments(value);
}

function updateValue2(value) {
    document.getElementById("sliderValue2").textContent = value; // Update displayed value

    // Call fetchComments() to get updated comments
    fetchComments(value);
}
// Logo setting up 
let iconDiv = document.querySelector(".icon");
iconDiv.style.backgroundSize = "cover";
iconDiv.style.backgroundPosition = "center";


function updateSentimentTable(pos, neg, neu) {
    document.getElementById("posVal").innerText = pos;
    document.getElementById("negVal").innerText = neg;
    document.getElementById("neuVal").innerText = neu;
}



// wroking search button
// Function to handle search
function handleSearch() {
    let inputText = inputSearch.value;
    let choice = displayOpt.textContent;
    let numComments = document.getElementById("slider").value;
    let numComments2 = document.getElementById("slider2").value;
    if (!inputText) {
        alert("Please enter text or a YouTube URL.");
        return;
    }

    resultBox.style.display = "block";

    fetch("/process", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText, option: choice, max_results: parseInt(numComments) ,max_comments:parseInt(numComments2)})
    })
    .then(response => response.json())
    .then(data => {
        console.log("Received list:", data.lines);
        if (data.error) {
            alert("Error: " + data.error);
            return;
        } else {
            updateSentimentTable(data.positive, data.negative, data.neutral);
        }

        if (data.chart) {
            document.getElementById("chart-img").src = data.chart + "?t=" + new Date().getTime(); // Prevent caching issues
        }
    })
    .catch(error => {
        console.error("Error: ", error);
    
        let errorDiv = document.querySelector(".error-message");
        errorDiv.style.display = "block";  
        errorDiv.textContent = "Error: " + error.message;  
    
        // Hide error message after 5 seconds
        setTimeout(() => {
            errorDiv.style.display = "none";
        }, 5000);
    });
    
    
}



// Attach event listener to search button
searchBtn.addEventListener("click", handleSearch);

// Listen for Enter key press in the input field
inputSearch.addEventListener("keypress", function(event) {
    if (event.key === "Enter") { // Check if the key pressed is 'Enter'
        event.preventDefault(); // Prevent form submission if inside a form
        handleSearch(); // Call the search function
    }
});

function closeError() {

    document.querySelector(".error-message").style.display = "none";
}

// fetch("/get_latest")
//     .then(response => response.json())
//     .then(data => {
//         console.log("Latest input:", data.latest_input);
//         console.log("Selected option:", data.selected_option);
//     })
//     .catch(error => console.error("Error:", error));


