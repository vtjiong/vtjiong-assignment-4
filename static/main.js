document
  .getElementById("search-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    let query = document.getElementById("query").value;
    let resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({
        query: query,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log(data);
        displayResults(data);
        displayChart(data);
      });
  });

function displayResults(data) {
  let resultsDiv = document.getElementById("results");
  resultsDiv.innerHTML = "<h2>Results</h2>";
  for (let i = 0; i < data.documents.length; i++) {
    let docDiv = document.createElement("div");
    docDiv.innerHTML = `<strong>Document ${data.indices[i]}</strong><p>${data.documents[i]}</p><br><strong>Similarity: ${data.similarities[i]}</strong>`;
    resultsDiv.appendChild(docDiv);
  }
}

let chart; // Declare chart globally

function displayChart(data) {
  let ctx = document.getElementById("similarity-chart").getContext("2d");

  // Destroy the existing chart if it exists
  if (chart) {
    chart.destroy();
  }

  // Create a new chart
  chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: data.indices, // X-axis: document indices
      datasets: [
        {
          label: "Cosine Similarity",
          data: data.similarities, // Y-axis: cosine similarity values
          backgroundColor: "rgba(54, 162, 235, 0.2)",
          borderColor: "rgba(54, 162, 235, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      scales: {
        y: {
          beginAtZero: true,
          max: 1, // Assuming similarity values range from 0 to 1
        },
      },
    },
  });
}
