const question = document.querySelector(".question");
const submitButton = document.querySelector(".submit");
const answer = document.querySelector(".answer");

function getBotAnswer() {
  if (question.value !== undefined) {
    const apiUrl = '/question';
    const apiData = {
        "question" : question.value
    }
    const other_params = {
        headers : { "content-type" : "application/json"},
        body : JSON.stringify(apiData),
        method : "POST",
    };
    fetch(apiUrl, other_params).then(function(response) {
        return response.json();
      })
      .then(data => {
        var finalData = "";

        data.answer.forEach(data => {
          finalData += `<div class="info-box">
                          <div class="topic-holder">
                            <div>File Name : ${data.fileName}</div>
                            <div>Page Number : ${data.pageNumber}</div>
                          </div>
                          <div class="content-holder">
                            ${data.content}
                          </div>
                        </div><br>`;
        })
        answer.innerHTML = finalData;
      }).catch((error) => {
        answer.innerHTML = 'something went wrong';
    });

  }
}

submitButton.addEventListener("click", getBotAnswer);
