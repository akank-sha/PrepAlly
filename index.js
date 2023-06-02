window.onload = function () {
  document.getElementById("upload").addEventListener("change", (e) => {
    e.preventDefault();
    console.log(e);
    const file = e.target.files[0];
    if (!file) {
      alert("");
    }
    let formData = new FormData();
    formData.append("file", file);
    document.getElementById("btn").innerText = "Uploading...";
    fetch("http://localhost:8000/uploadFile", {
      method: "POST",
      body: formData,
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.errors) {
          console.error(data.errors);
        } else {
          console.log(data);
          const elem = document.getElementById("result");
          elem.innerText = JSON.stringify(data, null, 4);
          elem.style.display = "block";
          document.getElementById("btn").innerText = "UPLOAD FILE";
          formList(data);
        }
      });
  });
};

function formList(data) {
  let node = document.createElement("ol");
  node.type = "1";
  for (let i = 0; i < data.length; i++) {
    const li = document.createElement("li");
    li.innerText = data[i].question.replace("\n", " ");
    let node2 = document.createElement("ol");
    node2.type = "a";
    node.appendChild(li);
    for (let j = 0; j < data[i].choices.length; j++) {
      const li = document.createElement("li");
      li.innerText = data[i].choices[j]["choice"];
      node2.appendChild(li);
    }
    node.appendChild(node2);
  }
  document.getElementById("result").innerText = "";
  document.getElementById("result").appendChild(node);
}
