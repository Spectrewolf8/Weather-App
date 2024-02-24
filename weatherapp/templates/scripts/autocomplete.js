// dummy js autocompletion methods with open cage api
//using specified container
export function initAutocomplete() {
  const input = document.getElementById("place_name");
  const container = document.getElementById("autocomplete-container");
  let timerId = null;

  input.addEventListener("input", () => {
    clearTimeout(timerId); // Clears the timer on input
    timerId = setTimeout(() => {
      // Sets a new timer
      fetch(`/api/autocomplete?q=${input.value}`)
        .then((response) => response.json())
        .then((data) => {
          // Clear the container
          container.innerHTML = "";

          // Create a new HTML element for each suggestion
          data.suggestions.forEach((suggestion) => {
            const element = document.createElement("div");
            element.textContent = suggestion["place"];
            element.classList.add("autocomplete-item");

            // Add a click event listener to the suggestion
            element.addEventListener("click", () => {
              input.value = suggestion["place"]; // Set the input value to the suggestion
              container.innerHTML = ""; // Clear the container
            });

            container.appendChild(element);
          });
        });
    }, 750); // Delay of 750ms
  });
}

// using datalists

export function initAutocomplete() {
  let timeout_length = 500;
  const input = document.getElementById("place_name");
  const datalist = document.getElementById("places");
  let timerId = null;

  input.addEventListener("input", () => {
    clearTimeout(timerId);
    datalist.innerHTML = ""; // Clear the datalist

    // If the input field is empty, return early
    if (!input.value.trim()) {
      return;
    }

    timerId = setTimeout(() => {
      fetch(`/api/autocomplete?q=${input.value}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          data.suggestions.forEach((suggestion) => {
            const option = document.createElement("option");
            option.value = suggestion["place"];
            datalist.appendChild(option);
          });
        })
        .catch((error) => {
          console.error("There was a problem with the fetch operation: ", error);
        });
    }, timeout_length);
  });
}
